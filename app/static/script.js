document.addEventListener('DOMContentLoaded', function () {
    initializeFaceRecognition();
});

let recognitionActive = false;
let recognitionStartTime = null;

async function initializeFaceRecognition() {
    const video = document.getElementById('video');
    const username = document.body.getAttribute('data-username');

    try {
        await loadModels();
        const imageUrls = await fetchUserImages(username);
        const labeledFaceDescriptors = await createLabeledFaceDescriptors(imageUrls, username);
        const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.6);
        startVideo(video, faceMatcher);
    } catch (error) {
        console.error("Error during face recognition initialization:", error);
    }
}

async function fetchUserImages(username) {
    try {
        const response = await fetch(`/api/users/${username}/images`);
        if (!response.ok) {
            throw new Error(`Failed to fetch images: ${response.statusText}`);
        }
        const { images } = await response.json();
        return images;
    } catch (error) {
        console.error("Error fetching user images:", error);
        throw error; // Rethrow to be caught in the calling function
    }
}

async function loadModels() {
    try {
        await Promise.all([
            faceapi.nets.tinyFaceDetector.loadFromUri('/static/models'),
            faceapi.nets.faceLandmark68Net.loadFromUri('/static/models'),
            faceapi.nets.faceRecognitionNet.loadFromUri('/static/models'),
            faceapi.nets.ssdMobilenetv1.loadFromUri('/static/models'),
        ]);
    } catch (error) {
        console.error("Error loading models:", error);
        throw error; // Rethrow to be caught in the calling function
    }
}

async function createLabeledFaceDescriptors(blobUrls, username) {
    // Load each image from a blob URL and create descriptors
    return Promise.all(blobUrls.map(async (blobUrl) => {
        try {
            const img = await faceapi.fetchImage(blobUrl);
            const detection = await faceapi.detectSingleFace(img).withFaceLandmarks().withFaceDescriptor();
            if (detection) {
                return new faceapi.LabeledFaceDescriptors(username, [detection.descriptor]);
            }
        } catch (error) {
            console.error("Error processing image URL:", blobUrl, error);
            return null; // Return null to filter out this image
        }
    })).then(descriptors => descriptors.filter(descriptor => descriptor !== null)); // Filter out any null descriptors
}

async function startVideo(video, faceMatcher) {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: {} });
        video.srcObject = stream;
        video.onloadedmetadata = () => { video.play(); setupRecognition(video, faceMatcher); };
    } catch (error) {
        console.error("Error starting video:", error);
    }
}

function setupRecognition(video, faceMatcher) {
    const canvas = faceapi.createCanvasFromMedia(video);
    document.body.append(canvas);
    const displaySize = { width: video.width, height: video.height };
    faceapi.matchDimensions(canvas, displaySize);

    setInterval(async () => {
        const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
            .withFaceLandmarks()
            .withFaceDescriptors();
        const resizedDetections = faceapi.resizeResults(detections, displaySize);
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
        faceapi.draw.drawDetections(canvas, resizedDetections);
        faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);

        detections.forEach(detection => {
            const bestMatch = faceMatcher.findBestMatch(detection.descriptor);
            if (bestMatch.label !== 'unknown' && bestMatch.distance < 0.5) {
                handleSuccessfulRecognition();
            } else {
                resetRecognition();
            }
        });
    }, 100);
}

function handleSuccessfulRecognition() {
    if (!recognitionActive) {
        recognitionActive = true;
        recognitionStartTime = new Date();
    } else if (new Date() - recognitionStartTime > 5000) {
        window.location.href = '/vote/vote';
    }
}

function resetRecognition() {
    recognitionActive = false;
    recognitionStartTime = null;
}
