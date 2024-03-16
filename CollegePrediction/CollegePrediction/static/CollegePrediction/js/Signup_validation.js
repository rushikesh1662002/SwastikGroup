// static/js/Signup_validation.js

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

    form.addEventListener('submit', function (event) {
        // Validate username
        const usernameInput = document.querySelector('input[name="username"]');
        if (usernameInput.value.trim() === '') {
            alert('Username cannot be empty');
            event.preventDefault();
            return;
        }

        // Validate email
        const emailInput = document.querySelector('input[name="email"]');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailInput.value.trim())) {
            alert('Invalid email format');
            event.preventDefault();
            return;
        }

        // Validate phone number
        const phoneInput = document.querySelector('input[name="phone"]');
        const phoneRegex = /^\d{10}$/; // assuming a 10-digit phone number
        if (!phoneRegex.test(phoneInput.value.trim())) {
            alert('Invalid phone number format');
            event.preventDefault();
            return;
        }

        // Validate password
        const passwordInput = document.querySelector('input[name="password"]');
        if (passwordInput.value.length < 6) {
            alert('Password must be at least 6 characters');
            event.preventDefault();
            return;
        }

        // Validate confirm password
        const confirmPasswordInput = document.querySelector('input[name="confirm_password"]');
        if (confirmPasswordInput.value !== passwordInput.value) {
            alert('Passwords do not match');
            event.preventDefault();
            return;
        }

        // If all validations pass, the form will be submitted
    });
});
