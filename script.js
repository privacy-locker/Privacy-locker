// Show selected section
function showSection(id) {
  document.querySelectorAll("section").forEach(sec => sec.classList.remove("active"));
  document.getElementById(id).classList.add("active");
}

// Toggle password visibility
function togglePassword() {
  const pwd = document.getElementById("password");
  pwd.type = (pwd.type === "password") ? "text" : "password";
}

// Handle login form
document.getElementById("loginForm").addEventListener("submit", e => {
  e.preventDefault();
  showSection("dashboard");
});

// Handle register form
document.getElementById("registerForm").addEventListener("submit", e => {
  e.preventDefault();
  alert("Registration Successful! Please login.");
  showSection("login");
});