const API_BASE_URL = "http://localhost:8000/api/v1";

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  // 1. Recuperar el token guardado en localStorage
  const token = localStorage.getItem("token");

  // 2. Preparar los encabezados de la solicitud
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  // 3. Petición HTTP a FastAPI
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // 4. Si el token expiró o es inválido (401 Unauthorized), limpiar localStorage y recargar
  if (response.status === 401) {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "/";
  }

  return response;
}
