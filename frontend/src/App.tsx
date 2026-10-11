import { useEffect, useState } from "react";
import { apiFetch } from "./api";
import { useAuth } from "./context/AuthContext";

interface Service {
  id: number;
  name: string;
  category: string;
  department: string;
  building: string;
  email: string;
  phone: string;
}

export default function App() {
  const { user, isAuthenticated, login, logout } = useAuth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [services, setServices] = useState<Service[]>([]);

  // Servicios por defecto
  const defaultServices: Service[] = [
    {
      id: 1,
      name: "Atención Psicológica UES",
      category: "Salud Mental",
      department: "Psicología",
      building: "Edificio 200",
      email: "psicologia@ues.mx",
      phone: "662-123-4567",
    },
    {
      id: 2,
      name: "Clínica Médica Universitaria",
      category: "Salud General",
      department: "Medicina",
      building: "Edificio 100",
      email: "clinica@ues.mx",
      phone: "662-987-6543",
    },
    {
      id: 3,
      name: "Gimnasio y Actividades Deportivas",
      category: "Deportes",
      department: "Deportes",
      building: "Gimnasio Principal",
      email: "deportes@ues.mx",
      phone: "662-555-0199",
    },
  ];

  // Cargar servicios consumiendo la API
  useEffect(() => {
    if (isAuthenticated) {
      apiFetch("/services")
        .then((res) => {
          if (!res.ok) throw new Error("Error al obtener servicios");
          return res.json();
        })
        .then((data) =>
          setServices(data && data.length > 0 ? data : defaultServices),
        )
        .catch(() => setServices(defaultServices));
    }
  }, [isAuthenticated]);

  // Manejo del Login con payload JSON exacto de Swagger
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      setError("Por favor completa los campos");
      return;
    }

    setError("");
    setLoading(true);

    try {
      // 1. Enviar JSON puro a la API
      const res = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || "Usuario o contraseña incorrectos");
      }

      const data = await res.json();
      const accessToken = data.access_token;

      // 2. Obtener la información del usuario autenticado (/auth/me)
      const userRes = await fetch("http://localhost:8000/api/v1/auth/me", {
        headers: { Authorization: `Bearer ${accessToken}` },
      });

      let userData = { username, role_id: 1 };
      if (userRes.ok) {
        userData = await userRes.json();
      }

      // 3. Guardar en AuthContext
      login(accessToken, userData as any);
      setError("");
    } catch (err: any) {
      setError(err.message || "Error al iniciar sesión");
    } finally {
      setLoading(false);
    }
  };

  const userRoleId = user?.role_id;
  const isAdmin = userRoleId === 1 || userRoleId === 5;
  const isStaff = userRoleId === 2;
  const isStudent = userRoleId === 3 || (!isAdmin && !isStaff);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col font-sans">
      {/* Header */}
      <header className="bg-slate-800 border-b border-slate-700 p-4 flex justify-between items-center shadow-md">
        <h1 className="text-xl font-bold text-amber-500">
          🎓 University Health — UES
        </h1>
        {isAuthenticated ? (
          <div className="flex items-center gap-4">
            <span className="text-sm bg-slate-700 px-3 py-1 rounded-full text-slate-300">
              Usuario:{" "}
              <strong className="text-amber-400">{user?.username}</strong> | Rol
              ID: <strong className="text-amber-400">{user?.role_id}</strong>
            </span>
            <button
              onClick={logout}
              className="bg-red-600 hover:bg-red-700 px-3 py-1 text-sm rounded transition cursor-pointer"
            >
              Cerrar Sesión
            </button>
          </div>
        ) : (
          <span className="text-sm text-slate-400">Acceso No Autenticado</span>
        )}
      </header>

      <main className="flex-1 p-6 max-w-6xl mx-auto w-full">
        {!isAuthenticated ? (
          /* Pantalla de Login */
          <div className="max-w-md mx-auto mt-12 bg-slate-800 p-8 rounded-xl shadow-lg border border-slate-700">
            <h2 className="text-2xl font-bold mb-6 text-center text-white">
              Iniciar Sesión
            </h2>
            {error && (
              <div className="bg-red-500/20 text-red-400 p-3 rounded mb-4 text-sm border border-red-500/30">
                {error}
              </div>
            )}
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">
                  Usuario / Correo
                </label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="ej. admin, medico o estudiante"
                  className="w-full bg-slate-900 border border-slate-700 rounded p-2 focus:outline-none focus:border-amber-500 text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Contraseña
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full bg-slate-900 border border-slate-700 rounded p-2 focus:outline-none focus:border-amber-500 text-white"
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-amber-500 hover:bg-amber-600 text-slate-900 font-bold py-2 rounded transition mt-2 cursor-pointer disabled:opacity-50"
              >
                {loading ? "Cargando..." : "Ingresar"}
              </button>
            </form>
          </div>
        ) : (
          /* Dashboard según Rol */
          <div className="space-y-6">
            <div className="bg-slate-800 p-4 rounded-lg border border-slate-700 flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold text-white">
                  Panel de Información de Servicios
                </h2>
                <p className="text-sm text-slate-400">
                  Consulta de servicios de salud y atención para estudiantes UES
                </p>
              </div>
              {isAdmin && (
                <button className="bg-amber-500 text-slate-900 px-4 py-2 rounded font-semibold text-sm hover:bg-amber-400 cursor-pointer">
                  + Agregar Nuevo Servicio
                </button>
              )}
            </div>

            {/* Banners distintivos */}
            {isAdmin && (
              <div className="bg-purple-900/40 border border-purple-500/50 p-4 rounded-lg text-purple-200 text-sm">
                👑 <strong>Modo Administrador:</strong> Tienes permisos de
                edición y eliminación total sobre la oferta institucional.
              </div>
            )}
            {isStaff && (
              <div className="bg-blue-900/40 border border-blue-500/50 p-4 rounded-lg text-blue-200 text-sm">
                🩺 <strong>Modo Personal Médico / Staff:</strong> Puedes
                gestionar horarios de atención e información de tu departamento.
              </div>
            )}
            {isStudent && (
              <div className="bg-emerald-900/40 border border-emerald-500/50 p-4 rounded-lg text-emerald-200 text-sm">
                🎓 <strong>Modo Estudiante:</strong> Consulta los accesos,
                ubicaciones y datos de contacto de los servicios de la UES.
              </div>
            )}

            {/* Tarjetas de Servicios */}
            <div className="grid md:grid-cols-3 gap-6">
              {services.map((svc) => (
                <div
                  key={svc.id}
                  className="bg-slate-800 p-5 rounded-xl border border-slate-700 flex flex-col justify-between"
                >
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-amber-500 bg-amber-500/10 px-2 py-1 rounded">
                      {svc.category}
                    </span>
                    <h3 className="text-lg font-bold mt-2 text-white">
                      {svc.name}
                    </h3>
                    <p className="text-xs text-slate-400 mt-1">
                      🏢 {svc.building} — {svc.department}
                    </p>
                    <div className="mt-4 space-y-1 text-sm text-slate-300">
                      <p>✉️ {svc.email}</p>
                      <p>📞 {svc.phone}</p>
                    </div>
                  </div>
                  {isAdmin && (
                    <div className="mt-4 pt-3 border-t border-slate-700 flex justify-end gap-2 text-xs">
                      <button className="text-blue-400 hover:underline cursor-pointer">
                        Editar
                      </button>
                      <button className="text-red-400 hover:underline cursor-pointer">
                        Eliminar
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
