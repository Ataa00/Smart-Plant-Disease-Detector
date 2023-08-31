
const closePopupCamButton = document.getElementById('closePopupCam');
const popupCamContainer = document.getElementById('camera-popup');
const cameraPopup = document.getElementById('camera-popup');
const cameraFeed = document.getElementById('camera-feed');

function resetCameraPopup() {
    cameraPopup.style.display = 'none';
    cameraFeed.srcObject = null;
}


closePopupCamButton.addEventListener('click', () => {
    resetCameraPopup();
    popupCamContainer.style.display = 'none';
});