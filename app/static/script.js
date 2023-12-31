document.addEventListener('DOMContentLoaded', function () {
    initializeFaceRecognition();
});

let recognitionActive = false;
let recognitionStartTime = null;

async function initializeFaceRecognition() {
    const video = document.getElementById('video');
    const userId = 1; // Replace with actual user ID
    const imageUrls = await fetchUserImages(userId);

    // Load face-api.js models
    await Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri('/static/models'),
        faceapi.nets.faceLandmark68Net.loadFromUri('/static/models'),
        faceapi.nets.faceRecognitionNet.loadFromUri('/static/models'),
        faceapi.nets.ssdMobilenetv1.loadFromUri('/static/models'),
    ]);

    // Process and label the user's face descriptors
    const labeledFaceDescriptors = await Promise.all(imageUrls.map(async url => {
        const img = await faceapi.fetchImage(url);
        const detections = await faceapi.detectSingleFace(img).withFaceLandmarks().withFaceDescriptor();
        return new faceapi.LabeledFaceDescriptors(userId.toString(), [detections.descriptor]);
    }));

    const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.6);
    startVideo(video, faceMatcher);
}
async function fetchUserImages(userId) {
    try {
        const response = await fetch(`/api/users/user/${userId}/images`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data.images; // Array of image URLs
    } catch (error) {
        console.error("Could not fetch user images:", error);
    }
}

async function startVideo(video, faceMatcher) {
    // Initialize webcam
    navigator.getUserMedia({ video: {} }, stream => {
        video.srcObject = stream;
    }, err => console.error(err));

    video.addEventListener('play', () => {
        // Set up canvas for facial recognition
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

            // Check each detection and match faces
            detections.forEach(detection => {
                const bestMatch = faceMatcher.findBestMatch(detection.descriptor);
                if (bestMatch.label !== 'unknown' && bestMatch.distance < 0.5) {
                    handleSuccessfulRecognition();
                } else {
                    resetRecognition();
                }
            });
        }, 100);
    });
}

function handleSuccessfulRecognition() {
    if (!recognitionActive) {
        recognitionActive = true;
        recognitionStartTime = new Date();
    } else if (new Date() - recognitionStartTime > 5000) { // 10 seconds
        window.location.href = '/vote/vote'; // Redirect to the voting page
    }
}

function resetRecognition() {
    recognitionActive = false;
    recognitionStartTime = null;
}