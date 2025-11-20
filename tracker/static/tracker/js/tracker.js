const csrftoken = document.querySelector('[name=csrf-token]').content;

const now = new Date();
const options = {weekday: 'long', day: 'numeric', month: 'long'};
document.getElementById('current-date').textContent = now.toLocaleDateString('ru-RU', options);

function getMealsState() {
    const meals = {};

    document.querySelectorAll('.meal').forEach(meal => {
        const name = meal.dataset.meal;
        meals[name] = meal.classList.contains('eaten')
    })
    return meals;
}

document.querySelectorAll('.meal').forEach(meal => {
    meal.addEventListener('click', function () {
        this.classList.toggle('eaten');
        const mealsState = getMealsState();

        fetch("/tracker/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({field: "meals", value: mealsState})
        })
            .then(response => response.json())
            .then(data => {
                updateBalance(data.total_points)
            })
            .catch(err => console.error(err))
    });
});

document.querySelectorAll('.glass').forEach((glass, index) => {
    glass.addEventListener('click', function () {
        const glasses = document.querySelectorAll('.glass');
        const currentIndex = Array.from(glasses).indexOf(this);

        glasses.forEach((g, i) => {
            if (i <= currentIndex) {
                g.classList.add('filled');

            } else {
                g.classList.remove('filled');
            }
        });

        const filledCount = document.querySelectorAll('.glass.filled').length;
        const waterTitle = document.querySelector('#tracker-water');
        waterTitle.textContent = `💧 ВОДА (${filledCount}/10)`;
        fetch("/tracker/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({field: "water", value: filledCount})
        })
            .then(response => response.json())
            .then(data => {
                updateBalance(data.total_points);
            })
            .catch(err => console.error(err));
    });
});


document.querySelectorAll('.mood-option').forEach(option => {
    option.addEventListener('click', function () {
        document.querySelectorAll('.mood-option').forEach(opt => {
            opt.classList.remove('selected');
        });
        this.classList.add('selected');
        updateBalance();
    });
});

document.querySelectorAll('.stimulant-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        const buttons = this.parentElement.querySelectorAll('.stimulant-btn');
        const clickedIndex = Array.from(buttons).indexOf(this);

        buttons.forEach((button, index) => {
            if (index <= clickedIndex) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });

        updateBalance();
    });
});

const checkboxes = document.querySelectorAll(".social-checkboxes input[type=checkbox]");

checkboxes.forEach(cb => {
    cb.addEventListener("change", () => {
        const selected = Array.from(checkboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.id);

        fetch("/tracker/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                field: "social_connections",
                value: selected
            })
        })
            .then(response => response.json())
            .then(data => {
                updateBalance(data.total_points);
            })
    });
});




function updateMovement(minutes) {
    const timeDisplay = document.getElementById('movement-time');
    let currentTime = parseInt(timeDisplay.textContent);
    currentTime = Math.max(0, currentTime + minutes);
    currentTime = Math.max(0, currentTime + minutes);
    currentTime = Math.min(30, currentTime);
    timeDisplay.textContent = currentTime + ' мин';

    fetch("/tracker/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            field: "movement_minutes",
            value: currentTime
        })
    })
        .then(response => response.json())
        .then(data => {
            updateBalance(data.total_points);
        })
        .catch(err => console.error(err));
}

function updateRelaxation(minutes) {
    const timeDisplay = document.getElementById('relaxation-time');
    let currentTime = parseInt(timeDisplay.textContent);
    currentTime = Math.max(0, currentTime + minutes);
    currentTime = Math.min(10, currentTime);

    timeDisplay.textContent = currentTime + ' мин';
    fetch("/tracker/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "field": "relaxation_minutes",
            "value": currentTime
        })

    })
        .then(response => response.json())
        .then(data => {
            updateBalance(data.total_points)
        })
}

function completeChallenge() {
    alert('🎉 Отлично! Челлендж выполнен!');
    const challengeButton = document.getElementById("challengeButton");
    challengeButton.disabled = true;
    challengeButton.textContent = "no more clcks pls"
    fetch("/tracker/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            "field": "completed_challenge",
            "value": true
        })
    })
        .then(response => response.json())
        .then(data => {
            updateBalance(data.total_points)
        })
}

function updateBalance(totalPoints) {
    const newBalance = Math.max(0, Math.min(100, totalPoints));

    document.getElementById('balance-score').textContent = newBalance + '%';
    document.getElementById('main-progress').style.width = newBalance + '%';

    const statusElement = document.getElementById('balance-status');
    if (newBalance >= 70) {
        statusElement.textContent = '🟢 Высокий уровень баланса';
    } else if (newBalance >= 40) {
        statusElement.textContent = '🟡 Средний уровень баланса';
    } else {
        statusElement.textContent = '🔴 Низкий уровень баланса';
    }
}

