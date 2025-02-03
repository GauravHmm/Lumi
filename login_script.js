document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const feedbackMessage = document.getElementById('feedback-message');

    feedbackMessage.textContent = '';

    if (username === '' || password === '') {
        feedbackMessage.textContent = 'Please enter your email and password.';
        feedbackMessage.classList.remove('success');
        feedbackMessage.style.opacity = "1";
        return;
    }

    if (username === 'test@example.com' && password === 'password123') {
        feedbackMessage.textContent = 'Login successful!';
        feedbackMessage.classList.add('success');
        feedbackMessage.style.opacity = "1";

        setTimeout(() => {
            window.location.href = 'https://www.apple.com/';
        }, 1500);
    } else {
        feedbackMessage.textContent = 'Incorrect email or password.';
        feedbackMessage.classList.remove('success');
        feedbackMessage.style.opacity = "1";
    }
});

// Signup Modal Logic
const signupModal = document.getElementById("signup-modal");
const openSignup = document.getElementById("open-signup");
const closeSignup = document.querySelector(".close");

openSignup.addEventListener("click", () => {
    signupModal.style.display = "flex";
});

closeSignup.addEventListener("click", () => {
    signupModal.style.display = "none";
});

window.addEventListener("click", (event) => {
    if (event.target === signupModal) {
        signupModal.style.display = "none";
    }
});

