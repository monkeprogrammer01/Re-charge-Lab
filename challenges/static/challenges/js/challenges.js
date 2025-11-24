document.addEventListener("DOMContentLoaded", function () {
    const cards = Array.from(document.querySelectorAll(".challenge-card"));
    const totalEl = document.getElementById("stat-total");
    const progressEl = document.getElementById("stat-progress");
    const completedEl = document.getElementById("stat-completed");
    const filterButtons = document.querySelectorAll(".ch-filter-btn");
    const searchInput = document.getElementById("challenge-search");
    const list = document.getElementById("challenge-list");

    function updateStats() {
        const visibleCards = cards.filter(c => !c.classList.contains("ch-hidden"));
        const total = visibleCards.length;
        const progress = visibleCards.filter(c => c.dataset.status === "in-progress").length;
        const completed = visibleCards.filter(c => c.dataset.status === "completed").length;
        totalEl.textContent = total;
        progressEl.textContent = progress;
        completedEl.textContent = completed;
    }

    function applyFilter() {
        const activeFilterBtn = document.querySelector(".ch-filter-btn-active");
        const diffFilter = activeFilterBtn ? activeFilterBtn.dataset.filter : "all";
        const term = searchInput.value.toLowerCase().trim();
        cards.forEach(card => {
            const diff = card.dataset.difficulty;
            const title = card.querySelector(".challenge-title").textContent.toLowerCase();
            const desc = card.querySelector(".challenge-desc").textContent.toLowerCase();
            const matchesDiff = diffFilter === "all" || diff === diffFilter;
            const matchesSearch = !term || title.includes(term) || desc.includes(term);

            if (matchesDiff && matchesSearch) {
                card.classList.remove("ch-hidden");
            } else {
                card.classList.add("ch-hidden");
            }
        });

        updateStats();
    }

    filterButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            filterButtons.forEach(b => b.classList.remove("ch-filter-btn-active"));
            btn.classList.add("ch-filter-btn-active");
            applyFilter();
        });
    });

    searchInput.addEventListener("input", applyFilter);

    // смена статуса
    list.addEventListener("click", e => {
        if (!e.target.classList.contains("status-toggle")) return;
        const card = e.target.closest(".challenge-card");
        const badge = card.querySelector(".ch-status-badge");
        const bar = card.querySelector(".ch-progress-bar");

        let state = card.dataset.status;
        if (state === "not-started") {
            state = "in-progress";
            badge.textContent = "In progress";
            badge.className = "ch-status-badge ch-status-in-progress";
            e.target.textContent = "Mark done";
            bar.style.width = "60%";
        } else if (state === "in-progress") {
            state = "completed";
            badge.textContent = "Completed";
            badge.className = "ch-status-badge ch-status-completed";
            e.target.textContent = "Again";
            bar.style.width = "100%";
            bar.classList.add("ch-progress-completed");
        } else {
            state = "not-started";
            badge.textContent = "Not started";
            badge.className = "ch-status-badge ch-status-not-started";
            e.target.textContent = "Start";
            bar.style.width = "0%";
            bar.classList.remove("ch-progress-completed");
        }

        card.dataset.status = state;
        updateStats();
    });

    applyFilter();
});
