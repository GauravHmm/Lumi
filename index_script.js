document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.getElementById('loginBtn');
    const getStartedBtn = document.getElementById('getStartedBtn');

    loginBtn.addEventListener('click', () => {
        // Redirect to login page
        window.location.href = 'login.html';
    });

    getStartedBtn.addEventListener('click', () => {
        // Redirect to sign up page or start onboarding process
        window.location.href = 'signin.html';
    });
});