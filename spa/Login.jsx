import { useState } from "react";
import { apiFetch } from "./api";

export default function Login({ onLogin }) {
  const [name, setName] = useState("");

  const login = async () => {
    const data = await apiFetch("/login", {
      method: "POST",
      body: JSON.stringify({ name }),
    });

    localStorage.setItem("token", data.token);
    localStorage.setItem("user_id", data.user_id);
    onLogin();
  };

  return (
    <div>
      <h2>Login</h2>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Your name"
      />
      <button onClick={login}>Enter</button>
    </div>
  );
}
