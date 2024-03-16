// validation.js
function validateForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Add your custom validation logic here
    if (username === "") {
        alert("Username must be filled out");
        return false;
    }

    if (password === "") {
        alert("Password must be filled out");
        return false;
    }
    if (password.length < 5) {
        alert("Password must be at least 8 characters long");
        return false;
    }

    // Add more validation rules as needed

    return true;
}
