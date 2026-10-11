import { useEffect, useState } from "react";
import { apiFetch } from "../api";

interface Service {
  id: number;
  name: string;
  description: string;
}

export const ServicesList = () => {
  const [services, setServices] = useState<Service[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchServices = async () => {
      try {
        // Usa apiFetch que adjunta automáticamente el Authorization: Bearer <token>
        const res = await apiFetch("/services");
        if (!res.ok) throw new Error("Error al cargar los servicios de salud");
        const data = await res.json();
        setServices(data);
      } catch (err: any) {
        setError(err.message);
      }
    };

    fetchServices();
  }, []);

  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div>
      <h3>Servicios de Salud Disponibles</h3>
      <ul>
        {services.map((s) => (
          <li key={s.id}>
            <strong>{s.name}</strong>: {s.description}
          </li>
        ))}
      </ul>
    </div>
  );
};
