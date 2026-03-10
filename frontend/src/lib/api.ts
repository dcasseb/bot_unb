import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000',
});

export function withAuth(token: string) {
  return axios.create({
    baseURL: api.defaults.baseURL,
    headers: { Authorization: `Bearer ${token}` },
  });
}

export default api;
