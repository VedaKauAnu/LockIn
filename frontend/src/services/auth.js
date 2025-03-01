import api from './api';

// Get the current user token
export const getToken = () => {
  return localStorage.getItem('token');
};

// Check if the user is authenticated
export const isAuthenticated = () => {
  return !!getToken();
};

// Set the authentication token
export const setToken = (token) => {
  localStorage.setItem('token', token);
};

// Remove the authentication token
export const removeToken = () => {
  localStorage.removeItem('token');
};

// Register a new user
export const register = async (username, email, password) => {
  try {
    const response = await api.post('/auth/register', {
      username,
      email,
      password
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

// Login a user
export const login = async (username, password) => {
  try {
    const response = await api.post('/auth/login', {
      username,
      password
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

// Logout the current user
export const logout = () => {
  removeToken();
};