-- Development-only seed data. No real personal information.

INSERT INTO roles (name, description) VALUES
('admin', 'Full administrative access'),
('staff', 'Can manage assigned university information'),
('student', 'Student-level access'),
('readonly', 'Read-only access')
ON CONFLICT (name) DO NOTHING;

INSERT INTO universities (name, description, website, email, phone)
VALUES (
    'Example University',
    'Development university for the University Health API.',
    'https://example.edu',
    'info@example.edu',
    '+52 000 000 0000'
)
ON CONFLICT (name) DO NOTHING;

INSERT INTO campuses (university_id, name, address, city, state, postal_code, phone)
SELECT id, 'Main Campus', 'University Avenue 100', 'Hermosillo', 'Sonora', '83000', '+52 000 000 0000'
FROM universities
WHERE name = 'Example University'
AND NOT EXISTS (
    SELECT 1 FROM campuses c
    WHERE c.university_id = universities.id AND c.name = 'Main Campus'
);

INSERT INTO departments (campus_id, name, code, description, email, phone)
SELECT c.id, 'Student Services', 'STU',
       'Development department for student services.',
       'student-services@example.edu', '+52 000 000 0000'
FROM campuses c
JOIN universities u ON u.id = c.university_id
WHERE u.name = 'Example University'
AND c.name = 'Main Campus'
AND NOT EXISTS (
    SELECT 1 FROM departments d
    WHERE d.campus_id = c.id AND d.code = 'STU'
);

INSERT INTO services (department_id, name, description, category, email, phone, website)
SELECT d.id, 'Psychological Support',
       'Example university psychological support service.',
       'Health', 'psychology@example.edu', '+52 000 000 0000',
       'https://example.edu/services/psychology'
FROM departments d
WHERE d.code = 'STU'
AND NOT EXISTS (
    SELECT 1 FROM services s
    WHERE s.department_id = d.id AND s.name = 'Psychological Support'
);
