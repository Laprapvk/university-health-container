-- Datos de desarrollo para University Health (UES)

-- 1. Roles del sistema
INSERT INTO roles (name, description) VALUES
('ADMIN', 'Acceso administrativo completo'),
('STAFF', 'Personal médico y psicológico'),
('STUDENT', 'Acceso para estudiantes'),
('GUEST', 'Acceso de solo lectura')
ON CONFLICT (name) DO NOTHING;

-- 2. Servicios universitarios
INSERT INTO services (name, description, category, department, building, email, phone, website)
SELECT 'Atención Psicológica UES',
       'Orientación, apoyo emocional y consulta psicológica para estudiantes.',
       'Salud Mental', 'Atención a la Salud y Bienestar', 'Edificio 200',
       'psicologia@ues.mx', '+52 662 259 5902',
       'https://www.ues.mx/servicios/psicologia'
WHERE NOT EXISTS (
    SELECT 1 FROM services WHERE name = 'Atención Psicológica UES'
);

INSERT INTO services (name, description, category, department, building, email, phone, website)
SELECT 'Clínica Médica Universitaria',
       'Consulta de medicina general, primeros auxilios y certificados.',
       'Salud General', 'Atención a la Salud y Bienestar', 'Edificio 100',
       'clinica@ues.mx', '+52 662 259 5903',
       'https://www.ues.mx/servicios/clinica'
WHERE NOT EXISTS (
    SELECT 1 FROM services WHERE name = 'Clínica Médica Universitaria'
);

INSERT INTO services (name, description, category, department, building, email, phone, website)
SELECT 'Gimnasio y Actividades Deportivas',
       'Espacios y programas para la activación física universitaria.',
       'Deportes', 'Deportes', 'Gimnasio Principal',
       'deportes@ues.mx', '+52 662 259 5904',
       'https://www.ues.mx/servicios/deportes'
WHERE NOT EXISTS (
    SELECT 1 FROM services WHERE name = 'Gimnasio y Actividades Deportivas'
);

-- 3. Personal de los servicios
INSERT INTO staff_members (first_name, last_name, position, department, email, phone)
SELECT 'Ana', 'López', 'Psicóloga', 'Atención a la Salud y Bienestar',
       'ana.lopez@ues.mx', '+52 662 259 5910'
WHERE NOT EXISTS (
    SELECT 1 FROM staff_members WHERE email = 'ana.lopez@ues.mx'
);

INSERT INTO staff_members (first_name, last_name, position, department, email, phone)
SELECT 'Carlos', 'Ramírez', 'Médico general', 'Atención a la Salud y Bienestar',
       'carlos.ramirez@ues.mx', '+52 662 259 5911'
WHERE NOT EXISTS (
    SELECT 1 FROM staff_members WHERE email = 'carlos.ramirez@ues.mx'
);

-- 4. Horarios de atención
INSERT INTO schedules (service_id, day_of_week, opening_time, closing_time)
SELECT s.id, 'Lunes', '08:00', '16:00'
FROM services s
WHERE s.name = 'Atención Psicológica UES'
AND NOT EXISTS (
    SELECT 1 FROM schedules h
    WHERE h.service_id = s.id AND h.day_of_week = 'Lunes'
);

INSERT INTO schedules (service_id, day_of_week, opening_time, closing_time)
SELECT s.id, 'Miércoles', '08:00', '16:00'
FROM services s
WHERE s.name = 'Clínica Médica Universitaria'
AND NOT EXISTS (
    SELECT 1 FROM schedules h
    WHERE h.service_id = s.id AND h.day_of_week = 'Miércoles'
);

-- 5. Usuarios de prueba (contraseña: password)
INSERT INTO users (username, email, password_hash, role_id)
SELECT 'admin', 'admin@ues.mx',
       '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW',
       r.id
FROM roles r
WHERE r.name = 'ADMIN'
AND NOT EXISTS (SELECT 1 FROM users WHERE username = 'admin');

INSERT INTO users (username, email, password_hash, role_id)
SELECT 'medico', 'medico@ues.mx',
       '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW',
       r.id
FROM roles r
WHERE r.name = 'STAFF'
AND NOT EXISTS (SELECT 1 FROM users WHERE username = 'medico');

INSERT INTO users (username, email, password_hash, role_id)
SELECT 'estudiante', 'estudiante@ues.mx',
       '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW',
       r.id
FROM roles r
WHERE r.name = 'STUDENT'
AND NOT EXISTS (SELECT 1 FROM users WHERE username = 'estudiante');
