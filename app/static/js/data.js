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




// /fetch the open ai data remain
// let riskpercentage =51
// if (riskpercentage > 50) {
//     btn.classList.remove('none');
//   } else {
//     btn.classList.add('none');
//   }
import { initializeApp} from "https://www.gstatic.com/firebasejs/9.17.2/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-auth.js";
import { getFirestore, doc, setDoc, getDocs, collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyBuNvUaahEA1efQ2S3Wg_-yzesWIIZsrcg",
  authDomain: "fake-social-media-detect-ae562.firebaseapp.com",
  projectId: "fake-social-media-detect-ae562",
  storageBucket: "fake-social-media-detect-ae562.firebasestorage.app",
  messagingSenderId: "984530461675",
  appId: "1:984530461675:web:f7213840d97c9bf868efae"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

document.getElementById("btnreport").addEventListener('click' ,async(e) =>{
    e.preventDefault();
    try {
          await addDoc(collection(db, "reportedAccounts"), {
            
            Username : Username ,
            Name : Name,
            Bio : Bio,
            Followers : Followers,
            Following : Following,
            NumberOfPosts : NumberOfPosts,
            Verified : Verified,
            AccountPrivacy: AccountPrivacy,
            timestamp: serverTimestamp(),
            status: "Pending",
          });
          alert("Account reported successfully!");
      } catch (error) {
        console.error("Error reporting account:", error);
        alert("Failed to report the account.");
      }

});








