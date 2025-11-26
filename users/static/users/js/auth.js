// auth.js – shared logic for Rating link and AI bar
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
      if (e.target === authModal) {
        closeAuthModal();
      }
    });
  }

  // Block Rating link if user is not logged in
  const ratingLink = document.querySelector(".nav-rating-link");
  if (ratingLink && !isLoggedIn) {
    ratingLink.addEventListener("click", (e) => {
      e.preventDefault();
      openAuthModal();
    });
  }

  // Block AI assistant on Home if not logged in
  const aiTextarea = document.getElementById("aiTextarea");
  const aiPlusBtn = document.getElementById("aiPlusBtn");

  function handleAiTrigger(e) {
    if (!isLoggedIn) {
      if (e) e.preventDefault();
      openAuthModal();
      return;
    }
    // Here you can later connect the real AI backend.
  }

  // if (aiTextarea) {
  //   aiTextarea.addEventListener("keydown", (e) => {
  //     if (e.key === "Enter" && !e.shiftKey) {
  //       handleAiTrigger(e);
  //     }
  //   });
  // }

  if (aiPlusBtn) {
    aiPlusBtn.addEventListener("click", handleAiTrigger);
  }
})();
