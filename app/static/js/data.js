// Path to the JSON file (dynamic based on user input)
let username;

document.getElementById('btnStart').addEventListener('click', () => {
    username = document.getElementById('socialUsername').value;
    
    // Construct the dynamic file path
    const jsonFilePath = `/${username}/${username}_profile/profile_data.json`;

    // Call the fetch_data function with retry logic
    fetch_data(jsonFilePath);
});

// Define global variables
let Username, Name, Bio, Followers, Following, NumberOfPosts, Verified, AccountPrivacy;

function fetch_data(jsonFilePath, retryCount = 5, retryInterval = 2000) {
    // Fetch the data
    fetch(jsonFilePath)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Assign the JSON data to global variables
            ({
                Username,
                Name,
                Bio,
                Followers,
                Following,
                NumberOfPosts,
                Verified,
                AccountPrivacy
            } = data);

            // Log to verify
            console.log("Username:", Username);
            console.log("Name:", Name);
            console.log("Bio:", Bio);
            console.log("Followers:", Followers);
            console.log("Following:", Following);
            console.log("Number of Posts:", NumberOfPosts);
            console.log("Verified:", Verified);
            console.log("Account Privacy:", AccountPrivacy);
        })
        .catch(error => {
            console.error(`Error fetching the JSON file: ${error.message}`);
            
            if (retryCount > 0) {
                console.log(`Retrying... Attempts left: ${retryCount}`);
                setTimeout(() => fetch_data(jsonFilePath, retryCount - 1, retryInterval), retryInterval);
            } else {
                console.error("Max retry attempts reached. Could not fetch the JSON file.");
            }
        });
}
