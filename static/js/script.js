let currentSlide = 0;
let slides = [];
let dots = [];
let totalSlides = 0;
let autoSlideInterval;

function showSlide(n) {
  slides.forEach((slide) => slide.classList.remove("active"));
  dots.forEach((dot) => dot.classList.remove("active"));

  slides[n].classList.add("active");
  dots[n].classList.add("active");
}

function nextSlide() {
  if (totalSlides === 0) return;
  currentSlide = (currentSlide + 1) % totalSlides;
  showSlide(currentSlide);
  resetAutoSlide();
}

function prevSlide() {
  if (totalSlides === 0) return;
  currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
  showSlide(currentSlide);
  resetAutoSlide();
}

function goToSlide(n) {
  if (totalSlides === 0) return;
  currentSlide = n;
  showSlide(currentSlide);
  resetAutoSlide();
}

function startAutoSlide() {
  autoSlideInterval = setInterval(() => {
    nextSlide();
  }, 5000); // Auto slide every 5 seconds
}

function resetAutoSlide() {
  clearInterval(autoSlideInterval);
  startAutoSlide();
}

// Mobile Menu Toggle
document.addEventListener("DOMContentLoaded", () => {
  const mobileMenuBtn = document.getElementById("mobile-menu-btn");
  const mobileMenu = document.getElementById("mobile-menu");

  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener("click", () => {
      mobileMenu.classList.toggle("hidden");
    });
  }

  // Wishlist Heart Toggle
  const heartIcons = document.querySelectorAll(".heart-icon");
  heartIcons.forEach((icon) => {
    icon.addEventListener("click", function () {
      this.classList.toggle("active");
    });
  });

  // Initialize carousel with global variables
  slides = document.querySelectorAll(".carousel-slide");
  dots = document.querySelectorAll(".carousel-dot");
  totalSlides = slides.length;

  if (slides.length > 0) {
    showSlide(0);
    startAutoSlide();
  }

  // Cart count is now managed server-side via context processor
});

function showToast(message, type = "info") {
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3000);
}
