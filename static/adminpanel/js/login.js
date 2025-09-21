document.addEventListener("DOMContentLoaded", () => {
    console.log("Login page ready ✅");

    // мини-анимация "мигания" кнопки
    const btn = document.querySelector(".btn-neon");
    if (btn) {
        setInterval(() => {
        btn.classList.toggle("pulse");
        }, 2500);
    }
});
