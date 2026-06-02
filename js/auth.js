/**
 * ============================================================================
 * AUTH.JS
 * This file handles user registration and login.
 * It connects the frontend forms to the backend API.
 * ============================================================================
 */

// The base URL for our backend API
const API_URL = "http://127.0.0.1:8000";

/* ======================================
   Registration Logic
====================================== */

// Find the registration form on the page
const registerForm = document.getElementById("register-form");

// If the form exists (meaning we are on the register.html page), listen for when it is submitted
if (registerForm) {
    registerForm.addEventListener("submit", registerUser);
}

/**
 * Function to handle creating a new user account.
 */
async function registerUser(event) {
    // Prevent the page from reloading when the button is clicked
    event.preventDefault();

    // Get the values the user typed into the form
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("message");

    try {
        // Show a loading message
        message.textContent = "Creating account...";
        message.style.color = "black"; // Reset color

        // Send a POST request to the backend API to register the user
        const response = await fetch(`${API_URL}/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, email, password })
        });

        const data = await response.json();

        // Check if the backend gave us an error (like "Email already exists")
        if (!response.ok) {
            throw new Error(data.detail || "Registration failed");
        }

        // Success! Update the message and clear the form
        message.textContent = "Registration successful!";
        message.style.color = "green";
        registerForm.reset();

    } catch (error) {
        // If something goes wrong, show the error message in red
        message.textContent = error.message;
        message.style.color = "red";
    }
}

/* ======================================
   Login Logic
====================================== */

// Find the login form on the page
const loginForm = document.getElementById("login-form");

// If the form exists (meaning we are on the login.html page), listen for when it is submitted
if (loginForm) {
    loginForm.addEventListener("submit", loginUser);
}

/**
 * Function to handle logging in an existing user.
 */
async function loginUser(event) {
    // Prevent the page from reloading
    event.preventDefault();

    // Get the email and password the user typed
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("message");

    try {
        // Show a loading message
        message.textContent = "Logging in...";
        message.style.color = "black";

        // Send a POST request to the backend API to log in
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        // Check if the login failed (wrong password, etc.)
        if (!response.ok) {
            throw new Error(data.detail || "Login failed");
        }

        // Save the secure token in the browser's local storage so they stay logged in
        localStorage.setItem("token", data.access_token);

        // Now, fetch the user's details to see if they are a student or an admin
        const meResponse = await fetch(`${API_URL}/me`, {
            headers: {
                Authorization: `Bearer ${data.access_token}`
            }
        });

        const currentUser = await meResponse.json();

        // Show a success message
        message.textContent = "Login successful!";
        message.style.color = "green";

        // Wait 1 second (1000 milliseconds) so the user can read the success message, then redirect them
        setTimeout(() => {
            if (currentUser.role === "admin") {
                // Send admins to the admin dashboard
                window.location.href = "admin-dashboard.html";
            } else {
                // Send students to the regular dashboard
                window.location.href = "dashboard.html";
            }
        }, 1000);

    } catch (error) {
        // If something goes wrong, show the error message in red
        message.textContent = error.message;
        message.style.color = "red";
    }
}