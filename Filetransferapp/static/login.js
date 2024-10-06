document.addEventListener('DOMContentLoaded', function() {
    const loginSubmit = document.getElementById('loginSubmit');

    if (loginSubmit) {
        loginSubmit.addEventListener('click', function(event) {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email, password: password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('errorMessage').textContent = data.error;
                } else {
                    document.cookie = "loggedIn=true; path=/";
                    window.location.href = '/';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});
