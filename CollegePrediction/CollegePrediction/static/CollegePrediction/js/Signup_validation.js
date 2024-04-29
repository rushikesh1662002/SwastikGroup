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
        const password = passwordInput.value;

        // Regular expressions to match the criteria
        const symbolRegex = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/;
        const numberRegex = /\d/g;
        const capitalLetterRegex = /[A-Z]/;

        if (password.length < 8) {
            alert('Password must be at least 8 characters');
            event.preventDefault();
            return;
        }

        if (!symbolRegex.test(password)) {
            alert('Password must contain at least 1 symbol');
            event.preventDefault();
            return;
        }

        if ((password.match(numberRegex) || []).length < 2) {
            alert('Password must contain at least 2 numbers');
            event.preventDefault();
            return;
        }

        if (!capitalLetterRegex.test(password)) {
            alert('Password must contain at least 1 capital letter');
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
