document.addEventListener("DOMContentLoaded", function () {
    const carousel = document.getElementById("carousel");
    if (!carousel) return;

    const track = carousel.querySelector(".carousel-track");
    const slides = Array.from(carousel.querySelectorAll(".carousel-slide"));
    const prevBtn = carousel.querySelector(".carousel-btn.prev");
    const nextBtn = carousel.querySelector(".carousel-btn.next");
    const dotsContainer = carousel.querySelector(".carousel-dots");

    if (!track || slides.length === 0) return;

    let currentIndex = 0;

    function renderDots() {
        if (!dotsContainer) return;
        dotsContainer.innerHTML = "";

        slides.forEach((_, index) => {
            const dot = document.createElement("button");
            dot.type = "button";
            dot.setAttribute("aria-label", `Ir al slide ${index + 1}`);
            if (index === currentIndex) dot.classList.add("active");
            dot.addEventListener("click", function () {
                currentIndex = index;
                updateCarousel();
            });
            dotsContainer.appendChild(dot);
        });
    }

    function updateCarousel() {
        const slideWidth = slides[0].offsetWidth;
        track.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
        slides.forEach((slide, index) => {
            slide.setAttribute("aria-hidden", index === currentIndex ? "false" : "true");
        });
        renderDots();
    }

    if (nextBtn) {
        nextBtn.addEventListener("click", function () {
            currentIndex = (currentIndex + 1) % slides.length;
            updateCarousel();
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener("click", function () {
            currentIndex = (currentIndex - 1 + slides.length) % slides.length;
            updateCarousel();
        });
    }

    window.addEventListener("resize", updateCarousel);
    updateCarousel();
});