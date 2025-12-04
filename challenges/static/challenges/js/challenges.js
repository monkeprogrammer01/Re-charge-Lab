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
        const completed = visibleCards.filter(c => c.dataset.status === "done").length;
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

    function getCSRFToken() {
        return document.querySelector("input[name='csrfmiddlewaretoken']").value;
    }

    async function updateChallengeStatus(challengeId, status) {
        try {
            const response = await fetch(`/challenges/${challengeId}/complete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({status: status})
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error updating challenge status:', error);
            throw error;
        }
    }

    filterButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            filterButtons.forEach(b => b.classList.remove("ch-filter-btn-active"));
            btn.classList.add("ch-filter-btn-active");
            applyFilter();
        });
    });

    searchInput.addEventListener("input", applyFilter);

    list.addEventListener("click", async (e) => {
        if (!e.target.classList.contains("status-toggle")) return;

        const card = e.target.closest(".challenge-card");
        const challengeId = card.dataset.challengeId;
        const badge = card.querySelector(".ch-status-badge");
        const bar = card.querySelector(".ch-progress-bar");

        let newStatus = card.dataset.status;
        let badgeText = "";
        let badgeClass = "";
        let buttonText = "";
        let progressWidth = "";

        // Переводим статусы на бэкенд
        let serverStatus = "";

        if (newStatus === "not-started") {
            newStatus = "in-progress";
            serverStatus = "in-progress";
            badgeText = "In progress";
            badgeClass = "ch-status-badge ch-status-in-progress";
            buttonText = "Mark done";
            progressWidth = "60%";
            bar.classList.remove("ch-progress-completed");
        } else if (newStatus === "in-progress") {
            newStatus = "done";
            serverStatus = "done";
            badgeText = "Completed";
            badgeClass = "ch-status-badge ch-status-completed";
            buttonText = "Again";
            progressWidth = "100%";
            bar.classList.add("ch-progress-completed");
        } else { // done -> not-started
            newStatus = "not-started";
            serverStatus = "not-started";
            badgeText = "Not started";
            badgeClass = "ch-status-badge ch-status-not-started";
            buttonText = "Start";
            progressWidth = "0%";
            bar.classList.remove("ch-progress-completed");
        }

        try {
            await updateChallengeStatus(challengeId, serverStatus);

            // Обновляем UI
            badge.textContent = badgeText;
            badge.className = badgeClass;
            e.target.textContent = buttonText;
            bar.style.width = progressWidth;
            card.dataset.status = newStatus;

            updateStats();
        } catch (error) {
            alert('Failed to update challenge status. Please try again.');
        }
    });

    // Инициализация фильтра и статистики
    applyFilter();
});
