document.getElementById('whole').addEventListener('click', async () => {
    const username = document.getElementById('dp').value.trim();
    const message = document.getElementById('message');
    const table = document.getElementById('dataTable');
    const tableBody = document.getElementById('dataTableBody');

    if (!username) {
        message.style.display = "block";
        message.textContent = "Username can't be Empty ⚠️";
        table.style.display = "none";
        return;
    }

    try {
        const response = await fetch('/wholeinstaFetch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username })
        });


        // const result = await response.json();
        // if (result.error) {
        //     message.style.display = "block";
        //     message.textContent = result.error;
        //     table.style.display = "none";
        //     return;
        // }


        let prof_data;
      
            let update1 = document.createElement('p');
            update1.className = 'progressStyle';
    
            fetch(`Wholedata/multiuserdata.json`)
                .then(response => response.json())
                .then(data => {
    
                    prof_data = data;
                    console.log(prof_data)
                })
                .catch(error => console.error('Error fetching data:', error));




        const users = result.data; // Assuming API returns 'data' with user array
        tableBody.innerHTML = ""; // Clear previous results
        if (users.length === 0) {
            message.style.display = "block";
            message.textContent = "No results found.";
            table.style.display = "none";
        } else {
            users.forEach((user, index) => {
                const row = `<tr>
                    <td>${index + 1}</td>
                    <td><img src="${user.profile_pic_url}" alt="Profile Picture" class="profile-pic" onerror="this.src='/static/default_placeholder.jpg';"></td>
                    <td>${user.full_name || 'N/A'}</td>
                    <td>${user.username || 'N/A'}</td>
                    <td>${user.id || 'N/A'}</td>
                    <td>${user.is_private ? 'Yes' : 'No'}</td>
                    <td>${user.is_verified ? 'Yes' : 'No'}</td>
                </tr>`;
                tableBody.innerHTML += row;
            });

            message.style.display = "none";
            table.style.display = "table";
        }
    } catch (error) {
        message.style.display = "block";
        message.textContent = "An error occurred. Please try again.";
        console.error("Error:", error);
    }
});
