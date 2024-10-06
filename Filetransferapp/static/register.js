document.addEventListener('DOMContentLoaded', function() {
    const registerSubmit = document.getElementById('registerSubmit');

    if (registerSubmit) {
        registerSubmit.addEventListener('click', function(event) {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Email validation regex
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            // Password validation regex (at least one capital letter, one symbol, and minimum length of 8)
            const passwordRegex = /^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9]).{8,}$/;

            if (!emailRegex.test(email)) {
                document.getElementById('errorMessage').innerHTML = 'Invalid email format.';
                return;
            }

            if (!passwordRegex.test(password)) {
                document.getElementById('errorMessage').innerHTML = 'Password must contain at least one capital letter, one symbol, and be at least 8 characters long.';
                return;
            }

            fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email, password: password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('errorMessage').innerHTML = data.error;
                } else {
                    window.location.href = '/login';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});
