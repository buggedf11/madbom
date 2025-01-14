document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const username = document.querySelector('input[name="username"]').value;
    const password = document.querySelector('input[name="password"]').value;

    const response = await fetch('/static/users.json');
    const users = await response.json();

    const user = users.find(user => 
        (user.username1 === username && user.password1 === password) || 
        (user.username2 === username && user.password2 === password)
    );

    const messageDiv = document.getElementById('message');
    if (user) {
        messageDiv.textContent = 'Login successful';
        window.location.href = 'main.html'; // Redirect to main.html
    } else {
        messageDiv.textContent = 'Invalid username or password';
    }
});