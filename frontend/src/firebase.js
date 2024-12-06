// Import the necessary Firebase modules
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyA__DxfjWcS2Uc_iA1SLL9gaO1IWZ0DrqQ",
    authDomain: "dtunes-d2cd8.firebaseapp.com",
    projectId: "dtunes-d2cd8",
    storageBucket: "dtunes-d2cd8.firebasestorage.app",
    messagingSenderId: "394747681934",
    appId: "1:394747681934:web:c4d971a535d6f41ec57ddf",
    measurementId: "G-EPDM9LQ4R2"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { auth, db };
