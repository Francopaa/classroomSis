CREATE DATABASE IF NOT EXISTS classroom;
USE classroom;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol ENUM('profesor', 'alumno') NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    profesor_id INT NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profesor_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS clase_alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clase_id INT NOT NULL,
    alumno_id INT NOT NULL,
    unido_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (clase_id) REFERENCES clases(id),
    FOREIGN KEY (alumno_id) REFERENCES usuarios(id),
    UNIQUE KEY unique_alumno_clase (clase_id, alumno_id)
);

CREATE TABLE IF NOT EXISTS tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    fecha_limite DATETIME NOT NULL,
    clase_id INT NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (clase_id) REFERENCES clases(id)
);

CREATE TABLE IF NOT EXISTS entregas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contenido TEXT,
    archivo VARCHAR(255),
    alumno_id INT NOT NULL,
    tarea_id INT NOT NULL,
    entregado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alumno_id) REFERENCES usuarios(id),
    FOREIGN KEY (tarea_id) REFERENCES tareas(id),
    UNIQUE KEY unique_entrega (alumno_id, tarea_id)
);

CREATE TABLE IF NOT EXISTS calificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nota DECIMAL(5,2) NOT NULL,
    comentario TEXT,
    entrega_id INT NOT NULL UNIQUE,
    calificado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrega_id) REFERENCES entregas(id)
);

-- Usuarios de prueba (contraseña: demo)
INSERT IGNORE INTO usuarios (id, nombre, email, password, rol) VALUES
(1, 'Prof. Garcia', 'profesor@demo.com', 'scrypt:32768:8:1$gw9c6LSv0W9kMGmF$b305686127b9e06d3a9bddf1c1b2b5bf3af1049541ecbd4fcd260501969803a0128c1467c612367f77eacd0d6fb45853968b4439383fa045ad2365812c3c5ba9', 'profesor'),
(2, 'Ana Lopez', 'alumno@demo.com', 'scrypt:32768:8:1$gw9c6LSv0W9kMGmF$b305686127b9e06d3a9bddf1c1b2b5bf3af1049541ecbd4fcd260501969803a0128c1467c612367f77eacd0d6fb45853968b4439383fa045ad2365812c3c5ba9', 'alumno');
