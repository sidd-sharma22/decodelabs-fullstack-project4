/**
 * ============================================================================
 * Mobile Navigation (Hamburger Menu) Logic
 * ============================================================================
 */

// Select the hamburger button and the navigation menu from the webpage
const hamburger = document.querySelector('.hamburger');
const nav = document.querySelector('.nav');

// DEBUG FIX: We check if the hamburger and nav elements actually exist on this page.
// This prevents errors if this script runs on a page without a header.
if (hamburger && nav) {
  
  // Listen for a click on the hamburger button
  hamburger.addEventListener('click', function () {
    // Toggle the 'open' class to show or hide the menu
    const isOpen = nav.classList.toggle('open');
    
    // Toggle the 'active' class to animate the hamburger into an 'X' shape
    this.classList.toggle('active');
    
    // Update accessibility attributes for screen readers
    this.setAttribute('aria-expanded', isOpen);
  });

  // Find all links inside the mobile navigation menu
  document.querySelectorAll('.nav-links a').forEach(function (link) {
    
    // Listen for a click on any of those links
    link.addEventListener('click', function () {
      // Close the menu and reset the hamburger icon when a link is clicked
      nav.classList.remove('open');
      hamburger.classList.remove('active');
      hamburger.setAttribute('aria-expanded', 'false');
    });
  });

  // Listen for clicks anywhere on the entire webpage
  document.addEventListener('click', function (e) {
    
    // Check if the click happened OUTSIDE the hamburger and OUTSIDE the nav menu
    if (!hamburger.contains(e.target) && !nav.contains(e.target)) {
      // If it was an outside click, close the menu
      nav.classList.remove('open');
      hamburger.classList.remove('active');
      hamburger.setAttribute('aria-expanded', 'false');
    }
  });
}

/**
 * ============================================================================
 * Global API Configuration & Task Fetching
 * ============================================================================
 */

// Store the base URL for the backend API so we don't have to type it repeatedly
const API_URL = "http://127.0.0.1:8000";

/**
 * Fetches all tasks from the backend and renders them onto the webpage.
 */
async function loadTasks() {
  
  // Find the container where we want to display the tasks
  const container = document.getElementById("task-container");

  // DEBUG FIX: If the task-container is not on this page (like on index.html),
  // we stop the function right here. This prevents a "null" error.
  if (!container) {
    return;
  }

  try {
    // Make a GET request to the backend API to fetch tasks
    const response = await fetch(`${API_URL}/tasks`);

    // Check if the server responded with an error (like 404 or 500)
    if (!response.ok) {
      // Throw an error to jump straight to the 'catch' block below
      throw new Error("Failed to fetch tasks");
    }

    // Convert the server response into a JavaScript array (JSON)
    const tasks = await response.json();

    // Clear out any "Loading..." text or old content inside the container
    container.innerHTML = "";

    // Loop through every single task in the array we got from the backend
    tasks.forEach(task => {
      
      // Create a brand new <div> element for this task
      const card = document.createElement("div");

      // Add a CSS class so it looks like a card
      card.classList.add("task-card");

      // Inject the task's title, status, and owner ID directly into the HTML of the card
      card.innerHTML = `
        <h3>${task.title}</h3>
        <p class="task-status">
          Status: ${task.status}
        </p>
        <p>User ID: ${task.user_id}</p>
      `;

      // Attach this newly created card to the main container on the webpage
      container.appendChild(card);
    });

  } catch (error) {
    // If anything fails (network issue, server down, etc.), show a friendly error message
    container.innerHTML = `
      <p>Unable to load tasks.</p>
    `;

    // Log the actual technical error to the developer console for debugging
    console.error(error);
  }
}

// Automatically try to load tasks as soon as this script file runs
loadTasks();