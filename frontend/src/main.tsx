import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./App.css"; // Importa estilos adicionales si existen
import { AuthProvider } from "./context/AuthContext";
import "./index.css"; // Importa las directivas de Tailwind / CSS global

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>,
);
