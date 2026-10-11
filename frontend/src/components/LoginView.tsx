import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";

export const LoginView = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      // 1. Enviar datos en formato x-www-form-urlencoded (estándar OAuth2 de FastAPI)
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const res = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || "Usuario o contraseña incorrectos");
      }

      const data = await res.json();
      const token = data.access_token;

      // 2. Obtener los datos del usuario autenticado
      const userRes = await fetch("http://localhost:8000/api/v1/auth/me", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!userRes.ok)
        throw new Error("Error al cargar la información del usuario");

      const userData = await userRes.json();

      // 3. Guardar estado en el AuthContext
      login(token, userData);
    } catch (err: any) {
      setError(err.message || "Error al conectar con el servidor");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-[80vh] items-center justify-center p-4">
      <div className="w-full max-w-md rounded-xl bg-slate-800/80 p-8 shadow-2xl backdrop-blur-md border border-slate-700">
        <h2 className="mb-6 text-center text-2xl font-bold text-white">
          Iniciar Sesión
        </h2>

        {error && (
          <div className="mb-4 rounded-lg bg-red-500/20 border border-red-500/50 p-3 text-sm text-red-300">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-300">
              Usuario / Correo
            </label>
            <input
              type="text"
              placeholder="ej. admin, medico o estudiante"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full rounded-lg bg-slate-900/90 border border-slate-700 px-4 py-2.5 text-white placeholder-slate-500 focus:border-amber-500 focus:outline-none focus:ring-1 focus:ring-amber-500 transition-colors"
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-300">
              Contraseña
            </label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full rounded-lg bg-slate-900/90 border border-slate-700 px-4 py-2.5 text-white placeholder-slate-500 focus:border-amber-500 focus:outline-none focus:ring-1 focus:ring-amber-500 transition-colors"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full cursor-pointer rounded-lg bg-amber-500 py-3 font-semibold text-slate-950 transition-colors hover:bg-amber-400 active:bg-amber-600 disabled:opacity-50"
          >
            {loading ? "Cargando..." : "Ingresar"}
          </button>
        </form>
      </div>
    </div>
  );
};
