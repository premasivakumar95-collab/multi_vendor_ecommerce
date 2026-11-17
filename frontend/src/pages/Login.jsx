import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await api.post("/auth/login", {
        email,
        password,
      });

      const data = response.data;

      sessionStorage.setItem("access_token", data.access_token);
      sessionStorage.setItem("role", data.user.role);

      const role = data.user.role.toLowerCase();

      if (role === "admin") navigate("/admin");
      else if (role === "vendor") navigate("/vendor");
      else if (role === "customer") navigate("/customer");
      else setError("Unknown user role");

    } catch (err) {
      setError(err.response?.data?.detail || "Invalid credentials");
    }
  };

  return (
    <div className="container">
      <form className="card" onSubmit={handleSubmit}>
        <h2>Login</h2>

        <input type="email" placeholder="Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)} required />

        <input type="password" placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)} required />

        <button type="submit">Login</button>

        {error && <p className="error">{error}</p>}

        <p>New user? <Link to="/register">Register</Link></p>
      </form>
    </div>
  );
}

export default Login;
