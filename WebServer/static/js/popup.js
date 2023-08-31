const openPopupButton = document.getElementById('openPopup');
const closePopupButton = document.getElementById('closePopup');
const popupContainer = document.getElementById('popupContainer');

openPopupButton.addEventListener('click', () => {
    popupContainer.style.display = 'flex';
});

closePopupButton.addEventListener('click', () => {
    popupContainer.style.display = 'none';
});
