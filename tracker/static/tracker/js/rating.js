// rating.js – sort table by points and fill "Your rating" summary
document.addEventListener("DOMContentLoaded", () => {
  const table = document.getElementById("ratingTable");
  if (!table) return;

  const body = table.querySelector("tbody");
  const rows = Array.from(body.querySelectorAll("tr"));

  // Sort rows by data-points in descending order and update ranks
  rows.sort((a, b) => {
    const pa = Number(a.dataset.points || "0");
    const pb = Number(b.dataset.points || "0");
    return pb - pa;
  });

  rows.forEach((row, index) => {
    row.cells[0].textContent = index + 1;
    body.appendChild(row);
  });

  // Fill summary card from the row marked as "you"
  const youRow = body.querySelector(".rating-row-you");
  if (!youRow) return;

  const cells = youRow.cells;
  const positionEl = document.getElementById("rating-position");
  const pointsEl = document.getElementById("rating-points");
  const completedEl = document.getElementById("rating-completed");
  const easyEl = document.getElementById("rating-easy");
  const mediumEl = document.getElementById("rating-medium");
  const hardEl = document.getElementById("rating-hard");

  if (positionEl) positionEl.textContent = cells[0].textContent;
  if (pointsEl) pointsEl.textContent = cells[2].textContent;
  if (completedEl) completedEl.textContent = cells[3].textContent;
  if (easyEl) easyEl.textContent = cells[4].textContent;
  if (mediumEl) mediumEl.textContent = cells[5].textContent;
  if (hardEl) hardEl.textContent = cells[6].textContent;
});
