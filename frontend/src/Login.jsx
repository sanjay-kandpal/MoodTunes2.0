import React, { useContext, useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "./firebase";
import { AuthContext } from './AuthContext';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Music, Sun, Cloud, CloudRain, Moon } from 'lucide-react';

const moodColors = {
  happy: "#FFD700",
  calm: "#4169E1",
  sad: "#4682B4",
  energetic: "#FF4500"
};

const moodIcons = {
  happy: Sun,
  calm: Cloud,
  sad: CloudRain,
  energetic: Moon
};

const EnhancedLogin = () => {
  const { setIsLoggedIn } = useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [mood, setMood] = useState("");
  const [recommendation, setRecommendation] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await signInWithEmailAndPassword(auth, email, password);
      toast.success('Login successful! Enjoying your mood music...', {
        position: "top-center",
        autoClose: 3000,
      });

      setTimeout(() => {
        setLoading(false);
        setIsLoggedIn(true);
        navigate("/home");
      }, 3000);

    } catch (error) {
      setLoading(false);
      toast.error(error.message, {
        position: "top-center",
        autoClose: 5000,
      });
    }
  };

  const handleMoodSelection = (selectedMood) => {
    setMood(selectedMood);
    // This is where you would typically fetch a real recommendation
    setRecommendation(getMockRecommendation(selectedMood));
  };

  const getMockRecommendation = (mood) => {
    const recommendations = {
      happy: "Don't Stop Me Now by Queen",
      calm: "Weightless by Marconi Union",
      sad: "Someone Like You by Adele",
      energetic: "Uptown Funk by Mark Ronson ft. Bruno Mars"
    };
    return recommendations[mood] || "Select a mood for a recommendation";
  };

  const MoodButton = ({ moodType }) => {
    const Icon = moodIcons[moodType];
    return (
      <button
        onClick={() => handleMoodSelection(moodType)}
        className={`p-2 rounded-full transition-all ${
          mood === moodType ? 'scale-110' : 'scale-100'
        }`}
        style={{ backgroundColor: moodColors[moodType] }}
      >
        <Icon size={24} color="white" />
      </button>
    );
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-400 via-pink-500 to-red-500">
      <ToastContainer />
      <div className="bg-white p-8 rounded-lg shadow-2xl w-96">
        <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">Welcome to MoodTunes</h2>
        <div className="mb-6">
          <p className="text-center text-gray-600 mb-2">How are you feeling today?</p>
          <div className="flex justify-around">
            <MoodButton moodType="happy" />
            <MoodButton moodType="calm" />
            <MoodButton moodType="sad" />
            <MoodButton moodType="energetic" />
          </div>
        </div>
        {recommendation && (
          <div className="mb-6 p-4 bg-gray-100 rounded-md">
            <p className="text-center text-gray-800">
              <Music className="inline-block mr-2" size={20} />
              {recommendation}
            </p>
          </div>
        )}
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600"
              placeholder="Enter your email"
            />
          </div>
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600"
              placeholder="Enter your password"
            />
          </div>
          <button
            type="submit"
            className={`w-full bg-purple-600 text-white p-2 rounded-md hover:bg-purple-700 transition-colors ${
              loading ? 'opacity-50 cursor-not-allowed' : ''
            }`}
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <p className="mt-4 text-center text-gray-600">
          Don't have an account? <Link to="/signup" className="text-purple-600 hover:underline">Sign Up</Link>
        </p>
      </div>
    </div>
  );
};

export default EnhancedLogin;