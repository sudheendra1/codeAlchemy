import axios from "axios";

const API_BASE_URL = "https://example.com/api";

export const fetchData = () => axios.get(`${API_BASE_URL}/data`);
export const sendData = (payload) =>
  axios.post(`${API_BASE_URL}/data`, payload);
