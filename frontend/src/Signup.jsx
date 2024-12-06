import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { auth, db } from "./firebase";
import { createUserWithEmailAndPassword, sendEmailVerification } from "firebase/auth";
import { doc, setDoc } from "firebase/firestore";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Music, Sun, Cloud, CloudRain, Moon, Eye, EyeOff } from 'lucide-react';

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

const EnhancedSignUp = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [clientId, setClientId] = useState("");
  const [clientSecret, setClientSecret] = useState("");
  const [loading, setLoading] = useState(false);
  const [mood, setMood] = useState("");
  const [recommendation, setRecommendation] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleSignUp = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      await sendEmailVerification(userCredential.user);
      await setDoc(doc(db, "users", userCredential.user.uid), {
        email,
        clientId,
        clientSecret,
        mood
      });
      toast.success('Sign up successful! Please check your email for verification.', {
        position: "top-center",
        autoClose: 5000,
      });
      setTimeout(() => {
        setLoading(false);
        navigate("/login");
      }, 5000);
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
    setRecommendation(getMockRecommendation(selectedMood));
  };

  const getMockRecommendation = (mood) => {
    const recommendations = {
      happy: "Walking on Sunshine by Katrina and The Waves",
      calm: "Clair de Lune by Claude Debussy",
      sad: "Everybody Hurts by R.E.M.",
      energetic: "Can't Stop the Feeling! by Justin Timberlake"
    };
    return recommendations[mood] || "Select a mood for a recommendation";
  };

  const MoodButton = ({ moodType }) => {
    const Icon = moodIcons[moodType];
    return (
      <button
        type="button"
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
        <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">Join MoodTunes</h2>
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
        <form onSubmit={handleSignUp} className="space-y-4">
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
            <div className="relative">
              <input
                id="password"
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600"
                placeholder="Enter your password"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5"
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
          </div>
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="clientId">
              Client ID
            </label>
            <input
              id="clientId"
              type="text"
              value={clientId}
              onChange={(e) => setClientId(e.target.value)}
              required
              disabled={loading}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600"
              placeholder="Enter your Client ID"
            />
          </div>
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="clientSecret">
              Client Secret
            </label>
            <input
              id="clientSecret"
              type="password"
              value={clientSecret}
              onChange={(e) => setClientSecret(e.target.value)}
              required
              disabled={loading}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600"
              placeholder="Enter your Client Secret"
            />
          </div>
          <button
            type="submit"
            className={`w-full bg-purple-600 text-white p-2 rounded-md hover:bg-purple-700 transition-colors ${
              loading ? 'opacity-50 cursor-not-allowed' : ''
            }`}
            disabled={loading}
          >
            {loading ? 'Signing up...' : 'Sign Up'}
          </button>
        </form>
        <p className="mt-4 text-center text-gray-600">
          Already have an account? <Link to="/login" className="text-purple-600 hover:underline">Login</Link>
        </p>
      </div>
    </div>
  );
};

export default EnhancedSignUp;