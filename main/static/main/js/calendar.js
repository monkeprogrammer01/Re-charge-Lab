// ------------------------------
// CALENDAR • TechnoPulse
// ------------------------------

document.addEventListener("DOMContentLoaded", () => {
    // элементы
    const monthLabel = document.getElementById("monthLabel");
    const calendarGrid = document.getElementById("calendarGrid");

    const sideTitle = document.getElementById("sideTitle");
    const sideSub = document.getElementById("sideSub");
    const tasksList = document.getElementById("tasksList");
    const taskInput = document.getElementById("taskInput");
    const addTaskBtn = document.getElementById("addTaskBtn");

    const deleteModal = document.getElementById("deleteModal");
    const cancelDeleteBtn = document.getElementById("cancelDeleteBtn");
    const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");

    // дата
    let currentDate = new Date();
    let selectedDate = new Date();

    // удаление
    let pendingDelete = { dateKey: null, index: null };

    // ------------------------------
    // Функция: ключ даты
    // ------------------------------
    function getDateKey(date) {
        return `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`;
    }


    function loadTasks(date) {
        const key = getDateKey(date);
        const all = JSON.parse(localStorage.getItem("tasks") || "{}");
        return all[key] || [];
    }

    function saveTasks(date, tasks) {
        const key = getDateKey(date);
        const all = JSON.parse(localStorage.getItem("tasks") || "{}");
        all[key] = tasks;
        localStorage.setItem("tasks", JSON.stringify(all));
    }


    function renderTasks() {
        const tasks = loadTasks(selectedDate);
        tasksList.innerHTML = "";

        tasks.forEach((t, index) => {
            const li = document.createElement("li");
            li.className = "task";

            li.innerHTML = `
                <button class="task-toggle">✔</button>
                <span>${t}</span>
                <button class="task-delete">🗑</button>
            `;

            // клик done
            li.querySelector(".task-toggle").addEventListener("click", () => {
                li.classList.toggle("task-done");
            });

            // delete
            li.querySelector(".task-delete").addEventListener("click", () => {
                pendingDelete = {
                    dateKey: getDateKey(selectedDate),
                    index: index
                };
                deleteModal.classList.add("open");
            });

            tasksList.appendChild(li);
        });
    }

    // ------------------------------
    // Рендер календаря
    // ------------------------------
    function renderCalendar() {
        calendarGrid.innerHTML = "";

        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();
        const firstDay = new Date(year, month, 1);
        const startWeekday = (firstDay.getDay() + 6) % 7; // понедельник = 0
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        monthLabel.textContent = currentDate.toLocaleString("en-US", {
            month: "long",
            year: "numeric"
        });

        // пустые клетки
        for (let i = 0; i < startWeekday; i++) {
            const empty = document.createElement("div");
            calendarGrid.appendChild(empty);
        }

        // дни
        for (let day = 1; day <= daysInMonth; day++) {
            const d = new Date(year, month, day);
            const cell = document.createElement("div");
            cell.className = "day";
            cell.textContent = day;

            // today
            const today = new Date();
            if (
                d.getDate() === today.getDate() &&
                d.getMonth() === today.getMonth() &&
                d.getFullYear() === today.getFullYear()
            ) {
                cell.classList.add("day-today");
            }

            // selected
            if (
                d.getDate() === selectedDate.getDate() &&
                d.getMonth() === selectedDate.getMonth() &&
                d.getFullYear() === selectedDate.getFullYear()
            ) {
                cell.classList.add("day-selected");
            }

            // click
            cell.addEventListener("click", () => {
                selectedDate = d;
                updateSidebar();
                renderCalendar();
            });

            calendarGrid.appendChild(cell);
        }
    }

    // ------------------------------
    // Обновление правой панели
    // ------------------------------
    function updateSidebar() {
        sideTitle.textContent = selectedDate.toLocaleDateString("en-US", {
            weekday: "long"
        });

        sideSub.textContent = selectedDate.toLocaleDateString("en-US", {
            day: "numeric",
            month: "long",
            year: "numeric"
        });

        renderTasks();
    }

    // ------------------------------
    // Добавление задачи
    // ------------------------------
    addTaskBtn.addEventListener("click", () => {
        const text = taskInput.value.trim();
        if (!text) return;

        const tasks = loadTasks(selectedDate);
        tasks.push(text);
        saveTasks(selectedDate, tasks);

        taskInput.value = "";
        renderTasks();
    });

    // ------------------------------
    // Модалка удаления
    // ------------------------------
    cancelDeleteBtn.addEventListener("click", () => {
        deleteModal.classList.remove("open");
    });

    confirmDeleteBtn.addEventListener("click", () => {
        const all = JSON.parse(localStorage.getItem("tasks") || "{}");
        const arr = all[pendingDelete.dateKey] || [];

        arr.splice(pendingDelete.index, 1);
        all[pendingDelete.dateKey] = arr;
        localStorage.setItem("tasks", JSON.stringify(all));

        deleteModal.classList.remove("open");
        renderTasks();
    });

    // ------------------------------
    // Переключение месяцев
    // ------------------------------
    document.getElementById("prevMonth").addEventListener("click", () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    document.getElementById("nextMonth").addEventListener("click", () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    // ------------------------------
    // START
    // ------------------------------
    renderCalendar();
    updateSidebar();
});
