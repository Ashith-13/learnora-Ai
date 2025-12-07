import axiosInstance from '../axios';

export const authService = {
  // Register new user
  register: async (userData) => {
    try {
      console.log("🚀 Sending registration data:", userData);
      const response = await axiosInstance.post('/auth/register', userData);
      console.log("✅ Registration response:", response.data);
      
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
      return response.data;
    } catch (error) {
      console.error("❌ Registration error:", error.response?.data || error);
      throw error.response?.data || error;
    }
  },

  // Login user
  login: async (credentials) => {
    try {
      console.log("🚀 Sending login data:", credentials);
      const response = await axiosInstance.post('/auth/login', credentials);
      console.log("✅ Login response:", response.data);
      
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
      return response.data;
    } catch (error) {
      console.error("❌ Login error:", error.response?.data || error);
      throw error.response?.data || error;
    }
  },

  // ... rest of your code
};
