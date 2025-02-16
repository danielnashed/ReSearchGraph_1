import React, { useState } from 'react';
import axios from 'axios';
import { API_ENDPOINTS } from '../Endpoints.js';

const Auth = ({ onAuthSuccess, onClustersReceived }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const updateDashboard = async (userId) => {
    try {
        const url = API_ENDPOINTS.GET_CLUSTERS.replace(':userId', userId);
        const response = await axios.get(`${url}`);
        if (response.status === 200) {
            const clusters = response.data.clusters;
            onClustersReceived(clusters);
        } else {
            console.error('Failed to update dashboard');
        }
    } catch (error) {
        console.error('Error updating dashboard:', error);
    }
  };

  const handleLogin = async () => {
    try {
      const response = await axios.post(API_ENDPOINTS.POST_LOGIN, { email, password });
      if (response.status === 200) {
        const userId = response.data.user_id;
        localStorage.setItem('userId', userId);
        // update dashboard
        await updateDashboard(userId);
        onAuthSuccess(userId);
      } else {
        console.error('Failed to login');
      }
    } catch (error) {
      console.error('Error logging in:', error);
    }
  };

  const handleSignup = async () => {
    try {
      const response = await axios.post(API_ENDPOINTS.POST_SIGNUP, { email, password });
      if (response.status === 201) {
        const userId = response.data.user_id;
        localStorage.setItem('userId', userId);
        onAuthSuccess(userId);
      } else {
        console.error('Failed to sign up');
      }
    } catch (error) {
        console.error('Error signing up:', error);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h2 className="text-2xl font-semibold mb-4">Login / Signup</h2>
        <input
          type="email"
          placeholder="Email"
          className="w-full p-2 mb-4 border rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full p-2 mb-4 border rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          onClick={handleLogin}
          className="w-full bg-blue-500 text-white p-2 rounded mb-2"
        >
          Login
        </button>
        <button
          onClick={handleSignup}
          className="w-full bg-green-500 text-white p-2 rounded"
        >
          Signup
        </button>
      </div>
    </div>
  );
};

export default Auth;