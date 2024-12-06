function updateGesture() {
    fetch('/get_gesture')
        .then(response => response.json())
        .then(data => {
            document.getElementById('gestureDisplay').textContent = data.gesture;
            if (data.gesture === "gesture_detected") {
                // Trigger mood change or any other action
                console.log("Gesture detected! Change mood.");
            }
        })
        .catch(error => console.error('Error:', error));
}

// Update gesture every second
setInterval(updateGesture, 1000);