document.addEventListener('DOMContentLoaded', () => {

const imageUpload = document.getElementById('image-upload');
const openCameraButton = document.getElementById('open-camera');
const cameraPopup = document.getElementById('camera-popup');
const cameraFeed = document.getElementById('camera-feed');
const captureButton = document.getElementById('capture-button');
const uploadMessage = document.getElementById('upload-message');
const uploadedThumbnail = document.getElementById('uploaded-thumbnail');
const capturedThumbnail = document.getElementById('captured-thumbnail');
const sendButton = document.getElementById('send-button'); // Added for the "Send" button

// Function to reset the camera popup and message
function resetCameraPopup() {
    cameraPopup.style.display = 'none';
    cameraFeed.srcObject = null;
    uploadMessage.style.display = 'none';
}

// Function to simulate image upload (replace with your actual upload logic)
function simulateImageUpload(imageData) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(imageData); // Simulated upload completes after 1 second
        }, 1000);
    });
}

// Function to display a success message (you can replace this with your actual success handling logic)
function displaySuccessMessage() {
    // Display a success message or perform other actions.
    alert('Image sent successfully!'); // Replace with your actual success handling.
}

imageUpload.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
  
      reader.onload = function (e) {
        const thumbnailContainer = document.querySelector('.thumbnail-container');
  
        // Display the uploaded image as a thumbnail within the card
        const thumbnailImage = document.createElement('img');
        thumbnailImage.src = e.target.result;
        thumbnailImage.alt = 'Uploaded Image'; // Add alt text for accessibility
        thumbnailContainer.innerHTML = ''; // Clear any previous thumbnail
        thumbnailContainer.appendChild(thumbnailImage);
        thumbnailContainer.style.display = 'block';
  
        // Show the send button
        sendButton.style.display = 'block';
      };
  
      reader.readAsDataURL(file);
    }
});

openCameraButton.addEventListener('click', () => {
    // Show the camera popup
    cameraPopup.style.display = 'block';

    // Use JavaScript to trigger the camera with the main (rear) camera facing mode
    if ('mediaDevices' in navigator && 'getUserMedia' in navigator.mediaDevices) {
        navigator.mediaDevices
            .getUserMedia({ video: { facingMode: 'environment' } })
            .then((mediaStream) => {
                cameraFeed.srcObject = mediaStream;
            })
            .catch((error) => {
                console.error('Error accessing camera:', error);
            });
    } else {
        alert('Camera access is not supported in this browser.');
    }
});


// Inside the captureButton event listener for camera capture
captureButton.addEventListener('click', () => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = cameraFeed.videoWidth;
    canvas.height = cameraFeed.videoHeight;
    context.drawImage(cameraFeed, 0, 0, canvas.width, canvas.height);
  
    const capturedImage = canvas.toDataURL('image/jpeg');
  
    const thumbnailContainer = document.querySelector('.thumbnail-container');
  
    // Display the captured image as a thumbnail within the card
    const thumbnailImage = document.createElement('img');
    thumbnailImage.src = capturedImage;
    thumbnailImage.alt = 'Captured Image'; // Add alt text for accessibility
    thumbnailContainer.innerHTML = ''; // Clear any previous thumbnail
    thumbnailContainer.appendChild(thumbnailImage);
    thumbnailContainer.style.display = 'block';
  
    sendButton.style.display = 'block';
  
    resetCameraPopup();
  
    simulateImageUpload(capturedImage)
      .then(() => {
        uploadMessage.style.display = 'block';
        uploadMessage.textContent = 'Photo uploaded successfully.';
      })
      .catch((error) => {
        console.error('Error uploading image:', error);
      });
  });

// Send button event listener
sendButton.addEventListener('click', () => {
    // Get the captured or uploaded image and send it to another place for processing
    const thumbnailImageSrc = capturedThumbnail.querySelector('img').src || uploadedThumbnail.querySelector('img').src;

    // Here, you can implement your logic to send the image to another place.
    // For example, you can create an AJAX request or use a fetch API to send the image data.

    // After sending, you can display a success message or perform other actions.
    // For demonstration purposes, we'll display a success message.
    displaySuccessMessage(); // Replace with your actual success handling.
});

});
