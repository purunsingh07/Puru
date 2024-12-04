document.getElementById("add-card-btn").addEventListener("click", function() {
    const container = document.getElementById("card-container");

    // Create a new card element
    const newCard = document.createElement("div");
    newCard.classList.add("report-card");

    // Add HTML content for the new card
    newCard.innerHTML = `
        <div class="card-header">
            <img src="https://via.placeholder.com/80" alt="Profile Picture">
            <div class="card-info">
                <h4>User ID: @new_user</h4>
                <p>Account Link: <a href="#" target="_blank">View Profile</a></p>
                <p>Date of Reporting: 2024-12-02</p>
                <p>Social Media Site: Twitter</p>
                <p>Fake Account Type: Impersonation</p>
                <p>Fake Percentage: 92%</p>
                <p>Status: Pending</p>
            </div>
        </div>
        <div class="card-footer">
            <div class="tags">
                <span class="tag">Impersonation</span>
                <span class="tag">Twitter</span>
                <span class="tag">Suspicious</span>
            </div>
            <div class= "btn">
            <button>Update</button>
            <button>Send File</button>
            <button>Done Investigation</button>
            </div>
        </div>
    `;

    // Append the new card to the container
    container.appendChild(newCard);
});
function toggleSidebar() {
      const sidebar = document.querySelector('.sidebar');
      sidebar.classList.toggle('active');
    }

    //toggle button
    document.addEventListener("DOMContentLoaded", () => {
        const themeToggle = document.getElementById("theme-toggle");
      
        // Load the saved theme from localStorage and apply it
        const savedTheme = localStorage.getItem("theme");
        if (savedTheme === "light") {
          document.body.classList.add("light-theme");
          themeToggle.checked = true;
          
        }
      
        // Toggle theme when the switch is clicked
        themeToggle.addEventListener("change", () => {
          document.body.classList.toggle("light-theme");
          const isLightMode = document.body.classList.contains("light-theme");
          localStorage.setItem("theme", isLightMode ? "light" : "dark");
        });
      });
      document.getElementById("cyberhistory").addEventListener('click', function () {
        window.location = "cyberhistory"
      })
      document.getElementById("cyber").addEventListener('click', function () {
        window.location = "cyber"
      })