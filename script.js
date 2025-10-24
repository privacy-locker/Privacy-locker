<script>
  // Check login state (using localStorage for demo)
  function updateNavbar() {
    const navLinks = document.getElementById("navLinks");
    const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";

    // Remove old login/logout if exists
    const existingAuthLink = document.querySelector("#authLink");
    if (existingAuthLink) existingAuthLink.remove();

    // Add new Login or Logout
    const li = document.createElement("li");
    li.id = "authLink";

    if (isLoggedIn) {
      li.innerHTML = '<a href="#" onclick="logout()">Logout</a>';
    } else {
      li.innerHTML = '<a href="index.html">Login</a>';
    }

    navLinks.appendChild(li);
  }

  function logout() {
    localStorage.removeItem("isLoggedIn");
    alert("You have been logged out!");
    window.location.href = "index.html";
  }

  // Call on page load
  updateNavbar();
</script>
