document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const username = document.querySelector('input[name="username"]').value;
    const password = document.querySelector('input[name="password"]').value;

    console.log('Entered Username:', username);
    console.log('Entered Password:', password);

    const response = await fetch('/static/users.json');
    const users = await response.json();

    console.log('Fetched Users:', users);

    const user = users.find(user => user.username === username && user.password === password);

    const messageDiv = document.getElementById('message');
    if (user) {
        messageDiv.textContent = 'Login successful';
        window.location.href = 'main.html'; // Redirect to main.html
    } else {
        messageDiv.textContent = 'Invalid username or password';
    }
});