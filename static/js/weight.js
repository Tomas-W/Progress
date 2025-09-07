// Apply dynamic colors
document.addEventListener('DOMContentLoaded', function() {
    const coloredElement = document.querySelector('.guess-weight-colored');
    if (coloredElement) {
        const color = coloredElement.getAttribute('data-color');
        coloredElement.style.color = color;
    }
});
