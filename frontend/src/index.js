import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import About from "./About.js";
import Login from "./Login.jsx";
import Garlic from "./Garlic"; // Assuming Garlic is your main page component
import Signup from './Signup.jsx'
import { AuthProvider } from "./AuthContext.jsx";
let root = ReactDOM.createRoot(document.getElementById("root"));

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Garlic />} />
          <Route path="/home"  element={<Garlic />} /> {/* Render Garlic as the homepage */}
          <Route path="/login" element={<Login />} />
          <Route path="/about" element={<About />} />
          <Route path="/signup" element={<Signup />} />      
        </Routes>
      </Router>
    </AuthProvider>

  );
}

root.render(<App />);
