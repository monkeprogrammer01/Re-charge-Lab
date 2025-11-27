const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

const calendarGrid = document.getElementById("calendarGrid");
const monthLabel = document.getElementById("monthLabel");
const sideTitle = document.getElementById("sideTitle");
const sideSub = document.getElementById("sideSub");

let current = new Date();
let selectedDate = new Date();

function formatISO(d) {
    return d.toISOString().split("T")[0];
}

function pretty(d) {
    return d.toLocaleDateString("en-US", {
        weekday: "long",
        month: "long",
        day: "numeric",
        year: "numeric"
    });
}

function showToast(msg) {
    const toast = document.getElementById("toast");
    toast.textContent = msg;
    toast.style.display = "block";
    setTimeout(() => {
        toast.style.display = "none";
    }, 1300);
}

function renderCalendar(dateObj) {
    calendarGrid.innerHTML = "";

    const year = dateObj.getFullYear();
    const month = dateObj.getMonth();

    monthLabel.textContent = dateObj.toLocaleString("en", {
        month: "long",
        year: "numeric"
    });

    const first = new Date(year, month, 1);
    let start = first.getDay();
    if (start === 0) start = 7;

    for (let i = 1; i < start; i++) {
        calendarGrid.appendChild(document.createElement("div"));
    }

    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const todayISO = formatISO(new Date());

    for (let d = 1; d <= daysInMonth; d++) {
        const btn = document.createElement("button");
        btn.className = "day";
        const iso = `${year}-${String(month + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
        btn.dataset.date = iso;
        btn.textContent = d;

        if (iso === todayISO) btn.classList.add("day-today");
        if (iso === formatISO(selectedDate)) btn.classList.add("day-selected");

        btn.onclick = () => {
            selectedDate = new Date(iso);
            updateSide(selectedDate);
            document.querySelector(".day-selected")?.classList.remove("day-selected");
            btn.classList.add("day-selected");
            renderTasks();
        };
        renderTasks();
        calendarGrid.appendChild(btn);
    }
}

function updateSide(date) {
    sideTitle.textContent = pretty(date);
    sideSub.textContent = formatISO(date);
}

async function getTasks() {
    const response = await fetch(`/calendar/tasks/?date=${formatISO(selectedDate)}`)
    const data = await response.json();
    return data.tasks;
}

async function deleteTask(taskId) {
    await fetch(`/calendar/tasks/delete/${taskId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        }
    })
}

prevMonth.onclick = () => {
    current.setMonth(current.getMonth() - 1);
    renderCalendar(current);
};

nextMonth.onclick = () => {
    current.setMonth(current.getMonth() + 1);
    renderCalendar(current);
};

/* Tasks */


const todoList = document.getElementById("todoList");
const inProgressList = document.getElementById("inProgressList");
const completedList = document.getElementById("completedList");
let draggedTaskId;

async function renderTasks() {
    const tasks = await getTasks(selectedDate);

    todoList.innerHTML = "";
    inProgressList.innerHTML = "";
    completedList.innerHTML = "";
    tasks.forEach(t => {
        const card = document.createElement("div");
        card.draggable = true;
        card.dataset.id = t.id;
        card.className = "task-card";
        card.id = "task-card"
        card.innerHTML = `
    <div class="task-left">
<!--<div class="task-checkbox ${t.status === 'completed' ? 'checked' : ''}"></div>-->
        <div class="task-text">${t.description}</div>
    </div>
    </div>
`;
        card.addEventListener("dragstart", (event) => {
            draggedTaskId = card.dataset.id;
        })
        const actionBtn = document.createElement("button");

        if (t.status === "todo") {
            actionBtn.className = "btn-primary";
            actionBtn.textContent = "Start";
        } else if (t.status === "in_progress") {
            actionBtn.className = "btn-success";
            actionBtn.textContent = "Mark Done";
        } else if (t.status === "completed") {
            actionBtn.className = "btn-danger";
            actionBtn.textContent = "Again";
        }

        actionBtn.onclick = async () => {
            let newStatus;
            if (t.status === "todo") newStatus = "in_progress";
            else if (t.status === "in_progress") newStatus = "completed";
            else if (t.status === "completed") newStatus = "todo";

            await updateTaskStatus(t.id, newStatus);
            await renderTasks();
        };

        card.appendChild(actionBtn);

        const deleteBtn = document.createElement("button");
        deleteBtn.className = "task-delete";
        deleteBtn.innerHTML = `<i class="fas fa-trash"></i>`;
        deleteBtn.onclick = async () => {
            await deleteTask(t.id);
            card.remove();
            updateCounts();
        };
        card.appendChild(deleteBtn);

        card.querySelector(".task-delete").onclick = async () => {
            await deleteTask(t.id);
            card.remove();
            updateCounts();
        };


        if (t.status === "todo") todoList.appendChild(card);
        else if (t.status === "in_progress") inProgressList.appendChild(card);
        else if (t.status === "completed") completedList.appendChild(card);
    });

    updateCounts();
}

const taskColumns = document.getElementsByClassName("kanban-column");
for (let col of taskColumns) {
    col.addEventListener("dragover", async (e) => {
        e.preventDefault();
    })
    col.addEventListener("drop", async (e) => {
        e.preventDefault()
        let newStatus;
        if (e.currentTarget.classList.contains("to-do")) newStatus = "todo";
        if (e.currentTarget.classList.contains("in-progress")) newStatus = "in_progress";
        if (e.currentTarget.classList.contains("completed")) newStatus = "completed";
        await updateTaskStatus(draggedTaskId, newStatus);
        await renderTasks()
    })
}

function updateCounts() {
    document.querySelector(".to-do .count").textContent = todoList.children.length;
    document.querySelector(".in-progress .count").textContent = inProgressList.children.length;
    document.querySelector(".completed .count").textContent = completedList.children.length;
}


async function updateTaskStatus(id, newStatus) {
    console.log(newStatus)
    const response = await fetch(`/calendar/tasks/update/${id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({status: newStatus})
    });

    if (!response.ok) {
        console.error("Update failed");
    }
}

const taskModal = document.getElementById("taskModal");
const saveTaskBtn = document.getElementById("saveTaskBtn");
const cancelTaskBtn = document.getElementById("cancelTaskBtn");
let currentStatus = null;

document.querySelectorAll(".new-page-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const column = btn.closest(".kanban-column");
        currentStatus = column.classList.contains("to-do")
            ? "todo"
            : column.classList.contains("in-progress")
                ? "in_progress"
                : "completed";

        taskModal.classList.add("show");
        document.getElementById("taskDescription").value = "";
        document.getElementById("taskDescription").focus();
    });
});

cancelTaskBtn.onclick = () => taskModal.classList.remove("show");

saveTaskBtn.onclick = async () => {
    const time = document.getElementById("taskTime").value;
    const description = document.getElementById("taskDescription").value.trim();
    const [hours, minutes] = time.split(':');
    const startDate = new Date(selectedDate);
    startDate.setHours(hours, minutes, 0, 0);
    const startDateISO = startDate.toISOString();
    if (!description) return alert("Please enter a task description.");
    if (!time) return alert("Please select a time.");
    const payload = {
        description,
        start_date: startDateISO,
        due_date: null,
        status: currentStatus
    };

    const response = await fetch("/calendar/tasks/add/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        taskModal.classList.remove("show");
        await renderTasks();
    } else {
        alert("Failed to add task.");
    }
};

/* init */
renderCalendar(current);

updateSide(selectedDate);