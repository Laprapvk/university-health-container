-- Development-only seed data for Universidad Estatal de Sonora (UES)

-- 1. Insertar Roles del Sistema (Formato Mayúsculas para RBAC Guard)
INSERT INTO roles (name, description) VALUES
('ADMIN', 'Full administrative access for IT and System Management'),
('STAFF', 'Medical and Psychological staff members with management access'),
('STUDENT', 'Student-level access for appointment requests and service viewing'),
('GUEST', 'Read-only access for unauthenticated visitors')
ON CONFLICT (name) DO NOTHING;

-- 2. Insertar Universidad (UES)
INSERT INTO universities (name, description, website, email, phone)
VALUES (
    'Universidad Estatal de Sonora',
    'Plataforma Institucional de Servicios de Salud y Atención Estudiantil UES.',
    'https://www.ues.mx',
    'contacto@ues.mx',
    '+52 662 259 5900'
)
ON CONFLICT (name) DO NOTHING;

-- 3. Insertar Campus Hermosillo
INSERT INTO campuses (university_id, name, address, city, state, postal_code, phone)
SELECT id, 'Unidad Académica Hermosillo', 'Ley Federal del Trabajo S/N, Col. Aleyda', 'Hermosillo', 'Sonora', '83100', '+52 662 259 5900'
FROM universities
WHERE name = 'Universidad Estatal de Sonora'
AND NOT EXISTS (
    SELECT 1 FROM campuses c
    WHERE c.university_id = universities.id AND c.name = 'Unidad Académica Hermosillo'
);

-- 4. Insertar Departamentos
INSERT INTO departments (campus_id, name, code, description, email, phone)
SELECT c.id, 'Atención a la Salud y Bienestar', 'SALUD',
       'Departamento encargado de servicios médicos y salud mental universitaria.',
       'salud@ues.mx', '+52 662 259 5901'
FROM campuses c
JOIN universities u ON u.id = c.university_id
WHERE u.name = 'Universidad Estatal de Sonora'
AND c.name = 'Unidad Académica Hermosillo'
AND NOT EXISTS (
    SELECT 1 FROM departments d
    WHERE d.campus_id = c.id AND d.code = 'SALUD'
);

-- 5. Insertar Servicios Institucionales
INSERT INTO services (department_id, name, description, category, email, phone, website)
SELECT d.id, 'Atención Psicológica UES',
       'Orientación, apoyo emocional y consulta psicológica para estudiantes.',
       'Salud Mental', 'psicologia@ues.mx', '+52 662 259 5902',
       'https://www.ues.mx/servicios/psicologia'
FROM departments d
WHERE d.code = 'SALUD'
AND NOT EXISTS (
    SELECT 1 FROM services s
    WHERE s.department_id = d.id AND s.name = 'Atención Psicológica UES'
);

INSERT INTO services (department_id, name, description, category, email, phone, website)
SELECT d.id, 'Clínica Médica Universitaria',
       'Consulta de medicina general, primeros auxilios y expedición de certificados.',
       'Salud General', 'clinica@ues.mx', '+52 662 259 5903',
       'https://www.ues.mx/servicios/clinica'
FROM departments d
WHERE d.code = 'SALUD'
AND NOT EXISTS (
    SELECT 1 FROM services s
    WHERE s.department_id = d.id AND s.name = 'Clínica Médica Universitaria'
);

-- 6. Insertar Usuarios de Prueba (Asignados mediante role_id)
-- Contraseña temporal para pruebas de desarrollo hash/bcrypt
INSERT INTO users (username, email, password_hash, role_id)
SELECT 'admin', 'admin@ues.mx', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', r.id
FROM roles r WHERE r.name = 'ADMIN'
AND NOT EXISTS (SELECT 1 FROM users WHERE username = 'admin');

INSERT INTO users (username, email, password_hash, role_id)
SELECT 'medico', 'medico@ues.mx', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', r.id
FROM roles r WHERE r.name = 'STAFF'
AND NOT EXISTS (SELECT 1 FROM users WHERE username = 'medico');

INSERT INTO users (username, email, password_hash, role_id)
SELECT 'estudiante', 'estudiante@ues.mx', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', r.id
FROM roles r WHERE r.name = 'STUDENT'
AND NOT EXISTS (SELECT 1 FROM users WHERE username = 'estudiante');