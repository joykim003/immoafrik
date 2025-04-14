document.addEventListener('DOMContentLoaded', function() {
    
        const signupForm = document.getElementById('signup-form');
        const loginForm = document.getElementById('login-form');
        const signupLink = document.getElementById('signup-link');
        const loginLink = document.getElementById('login-link');
        const errorMessage = document.getElementById('error-message');
        const errorText = document.getElementById('error-text');

        const passwordInputSignup = document.getElementById('password');
        const passwordToggleSignup = document.getElementById('toggle-password-signup');
        const password2InputSignup = document.getElementById('password2');
        const password2ToggleSignup = document.getElementById('toggle-password2-signup');

        const passwordInputLogin = document.getElementById('login_password');
        const passwordToggleLogin = document.getElementById('toggle-password-login');


        function displayErrorMessage(message) {
            errorMessage.style.display = 'block';
            errorText.textContent = message;
        }

        function hideErrorMessage() {
            errorMessage.style.display = 'none';
            errorText.textContent = ''; // Clear message
        }

        loginLink.addEventListener('click', (event) => {
            event.preventDefault();
            signupForm.style.display = 'none';
            loginForm.style.display = 'block';
            hideErrorMessage(); // Hide error message when switching forms
        });

        signupLink.addEventListener('click', (event) => {
            event.preventDefault();
            loginForm.style.display = 'none';
            signupForm.style.display = 'block';
            hideErrorMessage(); // Hide error message when switching forms
        });

        document.getElementById('signup-form-content').addEventListener('submit', (event) => {
            event.preventDefault();

            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const password2 = document.getElementById('password2').value;

            // Simple validation (you should have more robust validation on the server)
            if (password !== password2) {
                displayErrorMessage("Les mots de passe ne correspondent pas.");
                return;
            }
            if (password.length < 8) {
                displayErrorMessage("Le mot de passe doit contenir au moins 8 caractères.");
                return;
            }
             if (!email.includes('@')) {
                displayErrorMessage("L'adresse email n'est pas valide.");
                return;
            }

            // Simulate a successful signup (replace with your actual signup logic)
            console.log('Signup Form Submitted:', { username, email, password, password2 });
            alert('Inscription réussie! (Simulé).  Consultez la console pour les données.'); // Keep for debugging
            // In a real app, you'd redirect to the login page or a success page.
            loginForm.style.display = 'block';
            signupForm.style.display = 'none';
            hideErrorMessage();
        });

        document.getElementById('login-form-content').addEventListener('submit', (event) => {
            event.preventDefault();

            const username = document.getElementById('login_username').value;
            const password = document.getElementById('login_password').value;

            // Simulate a successful login (replace with your actual login logic)
            console.log('Login Form Submitted:', { username, password });
            alert('Connexion réussie! (Simulé). Consultez la console pour les données.');  // Keep for debugging
            // In a real app, you'd redirect to the dashboard or home page.
            // For this example, we'll just clear the form and show a message.
            document.getElementById('login_username').value = '';
            document.getElementById('login_password').value = '';
        });

        passwordToggleSignup.addEventListener('click', () => {
            const type = passwordInputSignup.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInputSignup.setAttribute('type', type);
            passwordToggleSignup.classList.toggle('fa-eye-slash');
            passwordToggleSignup.classList.toggle('fa-eye');
        });

        password2ToggleSignup.addEventListener('click', () => {
            const type = password2InputSignup.getAttribute('type') === 'password' ? 'text' : 'password';
            password2InputSignup.setAttribute('type', type);
            password2ToggleSignup.classList.toggle('fa-eye-slash');
            password2ToggleSignup.classList.toggle('fa-eye');
        });

        passwordToggleLogin.addEventListener('click', () => {
            const type = passwordInputLogin.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInputLogin.setAttribute('type', type);
            passwordToggleLogin.classList.toggle('fa-eye-slash');
            passwordToggleLogin.classList.toggle('fa-eye');
        });
});