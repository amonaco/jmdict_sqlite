const API_URL = "http://127.0.0.1:8000";

export function getToken() {
  return localStorage.getItem("token");
}

export async function apiFetch(path, options = {}) {
  const token = getToken();

  const headers = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
  };

  const res = await fetch(API_URL + path, {
    ...options,
    headers,
  });

  return res.json();
}

