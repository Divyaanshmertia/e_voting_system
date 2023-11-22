ddocument.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded and parsed');
    initializeFaceRecognition();
});

async function initializeFaceRecognition() {
    console.log('Initializing facial recognition');
    const video = document.getElementById('video');
    const userId = 1; // Replace with actual user ID
    const imageUrls = await fetchUserImages(userId);

    await Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri('/static/models'),
        faceapi.nets.faceLandmark68Net.loadFromUri('/static/models'),
        faceapi.nets.faceRecognitionNet.loadFromUri('/static/models'),
        faceapi.nets.ssdMobilenetv1.loadFromUri('/static/models'),
    ]);

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
        return await response.json().images;
    } catch (error) {
        console.error("Could not fetch user images:", error);
        return [];
    }
}

async function startVideo(video, faceMatcher) {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: {} });
        video.srcObject = stream;
    } catch (err) {
        console.error('Error accessing webcam:', err);
        return;
    }

    video.addEventListener('play', () => {
        const canvas = faceapi.createCanvasFromMedia(video);
        document.body.appendChild(canvas);
        const displaySize = { width: video.width, height: video.height };
        faceapi.matchDimensions(canvas, displaySize);

        setInterval(async () => {
            const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
                .withFaceLandmarks()
                .withFaceDescriptors();
            const resizedDetections = faceapi.resizeResults(detections, displaySize);
            canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
            detections.forEach(detection => {
                const bestMatch = faceMatcher.findBestMatch(detection.descriptor);
                if (bestMatch.label !== 'unknown' && bestMatch.distance < 0.4) {
                    if (!recognitionActive) {
                        recognitionActive = true;
                        recognitionStartTime = new Date();
                    } else {
                        const currentTime = new Date();
                        if (currentTime - recognitionStartTime >= 5000) {
                            enableVoting();
                        }
                    }
                }
            });
            faceapi.draw.drawDetections(canvas, resizedDetections);
            faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
        }, 100);
    });
}

function enableVoting() {
    const voteButtons = document.querySelectorAll('.btn.btn-primary');
    voteButtons.forEach(button => button.disabled = false);
}
