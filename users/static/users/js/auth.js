(function () {
    const isLoggedIn = Boolean(window.isLoggedIn);
    const authModal = document.getElementById("authModal");
    const authCancelBtn = document.getElementById("authCancelBtn");

    function openAuthModal() {
        if (!authModal) return;
        authModal.classList.add("open");
    }

    function closeAuthModal() {
        if (!authModal) return;
        authModal.classList.remove("open");
    }

    if (authCancelBtn) {
        authCancelBtn.addEventListener("click", closeAuthModal);
    }

    if (authModal) {
        authModal.addEventListener("click", (e) => {
            if (e.target === authModal) closeAuthModal();
        });
    }

    const ratingLink = document.querySelector(".nav-rating-link");
    if (ratingLink && !isLoggedIn) {
        ratingLink.addEventListener("click", (e) => {
            e.preventDefault();
            openAuthModal();
        });
    }

    const aiTextarea = document.getElementById("aiTextarea");
    const aiPlusBtn = document.getElementById("aiPlusBtn");

    function handleAiTrigger(e) {
        if (!isLoggedIn) {
            e?.preventDefault();
            openAuthModal();
        }
    }

    if (aiPlusBtn) {
        aiPlusBtn.addEventListener("click", handleAiTrigger);
    }

    const burger = document.getElementById("burger-menu");
    const navLinks = document.querySelector(".nav-links");

    if (burger && navLinks) {
        navLinks.classList.remove("active");
        burger.classList.remove("open");

        burger.addEventListener("click", (e) => {
            e.stopPropagation(); // Предотвращаем всплытие
            navLinks.classList.toggle("active");
            burger.classList.toggle("open");
        });

        // Закрытие при клике вне меню
        document.addEventListener("click", (e) => {
            if (navLinks.classList.contains("active") &&
                !navLinks.contains(e.target) &&
                !burger.contains(e.target)) {
                navLinks.classList.remove("active");
                burger.classList.remove("open");
            }
        });

        const navLinksItems = navLinks.querySelectorAll('a');
        navLinksItems.forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove("active");
                burger.classList.remove("open");
            });
        });
    }
})();