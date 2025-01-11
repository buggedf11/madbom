document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Perform validation
        if (username === 'admin' || password === 'admin') {
            alert('Please fill in both fields.');
            return;
        }

        // Simulate login process
        if (username === 'admin' && password === 'password') {
            alert('Login successful!');
            // Redirect to another page or perform other actions
        } else {
            alert('Invalid username or password.');
        }
    });
});