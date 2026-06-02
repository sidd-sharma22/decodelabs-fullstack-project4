/**
 * ============================================================================
 * ADMIN.JS
 * This file handles all the logic for the Admin Dashboard.
 * It checks if the user is an admin, loads all users, and loads all tasks.
 * ============================================================================
 */

// The base URL for our backend API
const API_URL = "http://127.0.0.1:8000";

// Get the login token from the browser's local storage
const token = localStorage.getItem("token");

// If there is no token, it means the user is not logged in.
// Redirect them back to the login page immediately.
if (!token) {
    window.location.href = "login.html";
}

/**
 * Function to log the user out by removing their security token and redirecting.
 */
function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

// Listen for clicks on the logout button
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
    logoutBtn.addEventListener("click", logout);
}

/**
 * Checks if the currently logged-in user is actually an Admin.
 * If they are just a student, they are kicked back to the normal dashboard.
 */
async function verifyAdmin() {
    try {
        // Ask the backend for the current user's details
        const response = await fetch(`${API_URL}/me`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        // If the token is invalid or expired, log them out
        if (response.status === 401) {
            logout();
            return;
        }

        const user = await response.json();

        // If the user's role is not 'admin', redirect them
        if (user.role !== "admin") {
            window.location.href = "dashboard.html";
        }
    } catch (error) {
        console.error(error);
        window.location.href = "login.html";
    }
}

/**
 * Fetches all registered users from the database and displays them.
 */
async function loadUsers() {
    const container = document.getElementById("users-container");
    
    // Safety check: if the container doesn't exist, stop running the function
    if (!container) return;

    try {
        // Show a loading message while waiting for the backend to reply
        container.innerHTML = `
            <div class="task-card">
                <h3>Loading users...</h3>
            </div>
        `;

        const response = await fetch(`${API_URL}/users`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            logout();
            return;
        }

        if (!response.ok) {
            throw new Error("Failed to load users");
        }

        const users = await response.json();

        // Update the total users counter at the top of the dashboard
        document.getElementById("total-users").textContent = users.length;

        // Clear the loading message
        container.innerHTML = "";

        // Loop through each user and create a visual card for them
        users.forEach(user => {
            const card = document.createElement("div");
            card.classList.add("task-card");
            
            // Inject the user's details into the card
            card.innerHTML = `
                <h3>${user.name}</h3>
                <p>Email: ${user.email}</p>
                <p>Role: ${user.role}</p>
            `;
            container.appendChild(card);
        });

    } catch (error) {
        console.error(error);
        container.innerHTML = "<p>Unable to load users.</p>";
    }
}

/**
 * Fetches all tasks across the entire platform and displays them.
 */
async function loadTasks() {
    const container = document.getElementById("admin-task-container");
    if (!container) return;

    try {
        container.innerHTML = `
            <div class="task-card">
                <h3>Loading tasks...</h3>
            </div>
        `;

        const response = await fetch(`${API_URL}/tasks`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            logout();
            return;
        }

        if (!response.ok) {
            throw new Error("Failed to load tasks");
        }

        const tasks = await response.json();

        // Update the total tasks counter
        document.getElementById("total-tasks").textContent = tasks.length;

        // Calculate completed vs pending tasks by filtering the array
        const completedTasks = tasks.filter(task => task.status === "Completed").length;
        const pendingTasks = tasks.filter(task => task.status === "Pending").length;

        // Update those specific counters on the dashboard
        document.getElementById("completed-tasks").textContent = completedTasks;
        document.getElementById("pending-tasks").textContent = pendingTasks;

        // Clear the loading text
        container.innerHTML = "";

        // Create a card for each task
        tasks.forEach(task => {
            const card = document.createElement("div");
            card.classList.add("task-card");
            card.innerHTML = `
                <h3>${task.title}</h3>
                <p>Status: ${task.status}</p>
                <p>User ID: ${task.user_id}</p>
                <button class="btn btn-outline delete-task-btn" data-id="${task.id}">
                    Delete
                </button>
            `;
            container.appendChild(card);
        });

    } catch (error) {
        console.error(error);
        container.innerHTML = "<p>Unable to load tasks.</p>";
    }
}

/**
 * Deletes a task from the database.
 */
async function deleteTask(taskId) {
    // Ask the admin to confirm before deleting to prevent accidents
    const confirmed = confirm("Are you sure you want to delete this task?");
    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}`, {
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

        // If successful, reload the tasks to update the list and the top counters
        loadTasks();

    } catch (error) {
        console.error(error);
        alert("Failed to delete the task. Please try again.");
    }
}

/**
 * Listens for clicks anywhere on the page and checks if a delete button was clicked.
 * This pattern is called "Event Delegation". It is very helpful when buttons 
 * are created dynamically after the page loads.
 */
document.addEventListener("click", function handleAdminActions(event) {
    // Check if the exact thing we clicked has the class "delete-task-btn"
    if (event.target.classList.contains("delete-task-btn")) {
        // Extract the data-id attribute we attached to the button
        deleteTask(event.target.dataset.id);
    }
});

/**
 * Initializes the admin dashboard by running all necessary functions in order.
 */
async function init() {
    await verifyAdmin(); // Check admin status first
    await loadUsers();   // Then load users
    await loadTasks();   // Finally load tasks
}

// Start the dashboard process
init();