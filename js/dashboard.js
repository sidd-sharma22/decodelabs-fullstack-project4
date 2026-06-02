/**
 * ============================================================================
 * DASHBOARD.JS
 * This file handles the logic for the Student Dashboard.
 * It allows students to load their tasks, create new ones, edit, and delete them.
 * ============================================================================
 */

// The base URL for our backend API
const API_URL = "http://127.0.0.1:8000";

// Get the login token from the browser's local storage
const token = localStorage.getItem("token");

// If there is no token, redirect the user back to the login page
if (!token) {
    window.location.href = "login.html";
}

/**
 * Function to log the user out by removing their token and redirecting.
 */
function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

// Listen for clicks on the logout button
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("token");
        window.location.href = "login.html";
    });
}

/**
 * Fetches the logged-in student's tasks from the database and displays them.
 */
async function loadTasks() {
    const container = document.getElementById("task-container");

    try {
        // Show a loading message while we fetch the tasks
        container.innerHTML = `
            <div class="task-card">
                <h3>Loading...</h3>
            </div>
        `;

        const response = await fetch(`${API_URL}/my-tasks`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        // If the token is invalid or expired, log them out
        if (response.status === 401) {
            logout();
            return;
        }

        if (!response.ok) {
            throw new Error("Failed to load tasks");
        }

        const tasks = await response.json();
        container.innerHTML = "";

        // If the user has no tasks yet, show a friendly welcome message
        if (tasks.length === 0) {
            container.innerHTML = `
                <div class="task-card">
                    <h3>No Tasks Yet</h3>
                    <p>Create your first task to get started.</p>
                </div>
            `;
            return;
        }

        // Loop through the tasks and create a card for each one
        tasks.forEach(task => {
            const card = document.createElement("div");
            card.classList.add("task-card");

            card.innerHTML = `
                <h3>${task.title}</h3>
                <p class="task-status">Status: ${task.status}</p>
                
                <div class="task-actions">
                    <button class="btn btn-outline edit-btn" 
                            data-id="${task.id}" 
                            data-title="${task.title}" 
                            data-status="${task.status}">
                        Edit
                    </button>
                    <button class="btn btn-outline delete-btn" 
                            data-id="${task.id}">
                        Delete
                    </button>
                </div>
            `;
            container.appendChild(card);
        });

    } catch (error) {
        container.innerHTML = `<p>Unable to load tasks.</p>`;
        console.error(error);
    }
}

/**
 * Handles the creation of a brand new task.
 */
async function createTask(event) {
    // Prevent the form from reloading the page
    event.preventDefault();

    const title = document.getElementById("task-title").value;
    const container = document.getElementById("task-container"); // DEBUG FIX: defined container

    try {
        container.innerHTML = `
            <div class="task-card">
                <h3>Loading...</h3>
            </div>
        `;

        const response = await fetch(`${API_URL}/my-tasks`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({
                title,
                status: "Pending" // New tasks are pending by default
            })
        });

        if (response.status === 401) {
            logout();
            return;
        }

        if (!response.ok) {
            throw new Error("Failed to create task");
        }

        // Clear the input field
        document.getElementById("task-form").reset();

        // Reload the task grid to show the newly added task
        loadTasks();

    } catch (error) {
        console.error(error);
    }
}

// Listen for the form submission to create a new task
const taskForm = document.getElementById("task-form");
if (taskForm) {
    taskForm.addEventListener("submit", createTask);
}

/**
 * Deletes a specific task.
 */
async function deleteTask(taskId) {
    const confirmed = confirm("Delete this task?");
    if (!confirmed) {
        return;
    }

    const container = document.getElementById("task-container"); // DEBUG FIX: defined container

    try {
        container.innerHTML = `
            <div class="task-card">
                <h3>Loading...</h3>
            </div>
        `;

        const response = await fetch(`${API_URL}/my-tasks/${taskId}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            logout();
            return;
        }

        if (!response.ok) {
            throw new Error("Failed to delete task");
        }

        // Reload the list after deletion
        loadTasks();

    } catch (error) {
        console.error(error);
    }
}

/**
 * Edits the title of an existing task.
 */
async function editTask(taskId, currentTitle, currentStatus) {
    // Prompt the user to type a new title
    const newTitle = prompt("Edit task title:", currentTitle);

    // If they clicked cancel or left it blank, do nothing
    if (!newTitle) {
        return;
    }

    const container = document.getElementById("task-container"); // DEBUG FIX: defined container

    try {
        container.innerHTML = `
            <div class="task-card">
                <h3>Loading...</h3>
            </div>
        `;

        const response = await fetch(`${API_URL}/my-tasks/${taskId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({
                title: newTitle,
                status: currentStatus
            })
        });

        if (response.status === 401) {
            logout();
            return;
        }

        if (!response.ok) {
            throw new Error("Failed to update task");
        }

        // Reload the list to show the updated title
        loadTasks();

    } catch (error) {
        console.error(error);
    }
}

/**
 * Uses Event Delegation to listen for clicks on dynamically created Edit or Delete buttons.
 */
function handleTaskActions(event) {
    const target = event.target;

    // If the clicked element was a delete button
    if (target.classList.contains("delete-btn")) {
        deleteTask(target.dataset.id);
    }

    // If the clicked element was an edit button
    if (target.classList.contains("edit-btn")) {
        editTask(
            target.dataset.id,
            target.dataset.title,
            target.dataset.status
        );
    }
}

// Attach the event delegation listener to the main container
const taskContainer = document.getElementById("task-container");
if (taskContainer) {
    taskContainer.addEventListener("click", handleTaskActions);
}

// Start everything off by loading the tasks when the script runs
loadTasks();