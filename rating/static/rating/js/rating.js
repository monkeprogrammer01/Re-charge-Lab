// rating.js – заполняет "Your rating summary" из строки "you"
// и показывает модалку, если пользователь не залогинен

document.addEventListener("DOMContentLoaded", () => {
  const table = document.getElementById("ratingTable");
  if (!table) return;

  const body = table.querySelector("tbody");
  if (!body) return;

  // Находим строку текущего пользователя
  const youRow = body.querySelector(".rating-row-you");

  if (youRow) {
    const cells = youRow.cells;

    const positionEl = document.getElementById("rating-position");
    const pointsEl = document.getElementById("rating-points");
    const completedEl = document.getElementById("rating-completed");
    const easyEl = document.getElementById("rating-easy");
    const mediumEl = document.getElementById("rating-medium");
    const hardEl = document.getElementById("rating-hard");

    // Берём данные из таблицы и подставляем в левую карточку
    if (positionEl) positionEl.textContent = `#${cells[0].textContent.trim()}`;
    if (pointsEl) pointsEl.textContent = cells[2].textContent.trim();
    if (completedEl) completedEl.textContent = cells[3].textContent.trim();
    if (easyEl) easyEl.textContent = cells[4].textContent.trim();
    if (mediumEl) mediumEl.textContent = cells[5].textContent.trim();
    if (hardEl) hardEl.textContent = cells[6].textContent.trim();
  }

  // ====== Логика модалки авторизации ======
  const modal = document.getElementById("authModal");
  const cancelBtn = document.getElementById("authCancelBtn");

  // window.isLoggedIn ты задаёшь в шаблоне:
  // window.isLoggedIn = true / false
  if (modal && typeof window.isLoggedIn !== "undefined" && !window.isLoggedIn) {
    modal.classList.add("open");
  }

  if (cancelBtn && modal) {
    cancelBtn.addEventListener("click", () => {
      modal.classList.remove("open");
    });
  }
});