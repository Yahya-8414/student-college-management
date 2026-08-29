// scripts.js

// Function to validate login and registration forms
function validateForm(form) {
    const username = form.username.value.trim();
    const password = form.password.value.trim();
    
    if (username === "" || password === "") {
        alert("Please fill in all fields.");
        return false;
    }
    
    // Additional validation can be added here (e.g., password strength)
    return true;
}

// Event listener for login form submission
const loginForm = document.querySelector('form[action="/login"]');
if (loginForm) {
    loginForm.addEventListener('submit', function(event) {
        if (!validateForm(loginForm)) {
            event.preventDefault(); // Prevent form submission if validation fails
        }
    });
}

// Event listener for registration form submission
const registerForm = document.querySelector('form[action="/register"]');
if (registerForm) {
    registerForm.addEventListener('submit', function(event) {
        if (!validateForm(registerForm)) {
            event.preventDefault(); // Prevent form submission if validation fails
        }
    });
}

// Example function to handle button clicks (e.g., for adding a new batch)
document.querySelector('.add-batch-button')?.addEventListener('click', function() {
    alert("Add New Batch functionality to be implemented.");
});

// Example function to handle editing a batch
document.querySelector('.edit-batch-button')?.addEventListener('click', function() {
    alert("Edit Batch functionality to be implemented.");
});

// Example function to handle deleting a batch
document.querySelector('.delete-batch-button')?.addEventListener('click', function() {
    alert("Delete Batch functionality to be implemented.");
});

// Example function to show a confirmation alert before deleting a user
function confirmDelete(username) {
    return confirm(`Are you sure you want to delete ${username}? This action cannot be undone.`);
}

// Attach this function to delete buttons in the user management section
document.querySelectorAll('.delete-user-button').forEach(button => {
    button.addEventListener('click', function(event) {
        const username = this.getAttribute('data-username');
        if (!confirmDelete(username)) {
            event.preventDefault(); // Prevent the default action if the user cancels
        }
    });
});

fetch('/api/data')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });

    function debounce(func, delay) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    }