import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // Increased to 60 seconds
  headers: {
    "Content-Type": "application/json",
  },
});

export const getHealth = async () => {
  const response = await api.get("/api/health");
  return response.data;
};

export const getClients = async () => {
  const response = await api.get("/api/clients");
  return response.data;
};

export const getCase = async (clientId) => {
  const response = await api.get(`/api/cases/${clientId}`);
  return response.data;
};

export const getHandover = async (clientId) => {
  const response = await api.get(`/api/handover/${clientId}`);
  return response.data;
};

export const getDashboard = async () => {
  const response = await api.get("/api/dashboard");
  return response.data;
};

export default api;