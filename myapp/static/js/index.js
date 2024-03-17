document.addEventListener("DOMContentLoaded", function () {
  const loginBtn = document.getElementById("login-btn");
  const signupBtn = document.getElementById("signup-btn");
  const loginForm = document.getElementById("login-form");
  const signupForm = document.getElementById("signup-form");

  // Show login form by default
  loginBtn.classList.add("active");
  loginForm.classList.remove("hidden");

  // Switch to login form
  loginBtn.addEventListener("click", function () {
    loginBtn.classList.add("active");
    signupBtn.classList.remove("active");
    loginForm.classList.remove("hidden");
    signupForm.classList.add("hidden");
  });

  // Switch to signup form
  signupBtn.addEventListener("click", function () {
    signupBtn.classList.add("active");
    loginBtn.classList.remove("active");
    signupForm.classList.remove("hidden");
    loginForm.classList.add("hidden");
  });
});
