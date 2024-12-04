// Sample data for the history table
const historyData = [
    {
      date: "13-03-2004",
      userId: "_PRATIKSHA_",
      accLink: "www.instagram.com",
      status: "Resolved",
      platform: "Instagram",
    },
    {
      date: "21-02-2004",
      userId: "_jiyaa_21",
      accLink: "www.facebook.com",
      status: "Pending",
      platform: "Facebook",
    },
    {
      date: "15-05-2004",
      userId: "fake_acc_123",
      accLink: "www.twitter.com",
      status: "Under Review",
      platform: "Twitter",
    },
  ];
  
  // Dynamically populate the table
  const tableBody = document.getElementById("history-data");
  
  historyData.forEach((data) => {
    const row = document.createElement("tr");
  
    row.innerHTML = `
      <td>${data.date}</td>
      <td>${data.userId}</td>
      <td><a href="https://${data.accLink}" target="_blank">${data.accLink}</a></td>
      <td>${data.status}</td>
      <td>${data.platform}</td>
    `;
  
    tableBody.appendChild(row);
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
  document.getElementById("cyberreport").addEventListener('click', function () {
    window.location = "cyberreport"
  })
  document.getElementById("cyber").addEventListener('click', function () {
    window.location = "cyber"
  })