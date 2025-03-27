
let index = 0;
const totalPages = 3;
function moveSlide(step) {
    index += step;
    if (index >= totalPages) index = 0;
    if (index < 0) index = totalPages - 1;
    document.querySelector(".carousel").style.transform = `translateX(${-index * 33}%)`;
}
setInterval(() => moveSlide(1), 5000); // Scorrimento automatico ogni 3s
