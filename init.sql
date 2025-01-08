-- Selectează baza de date
USE myapp;

-- Creează tabela pentru utilizatori
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Crează utilizatorul 'admin' și atribuie-i toate privilegiile
CREATE USER 'admin'@'%' IDENTIFIED BY 'admin_password';

GRANT ALL PRIVILEGES ON myapp.* TO 'admin'@'localhost' WITH GRANT OPTION;  -- Atribuie toate privilegiile pe baza de date 'myapp'

-- Aplică modificările
FLUSH PRIVILEGES;

-- Adaugă utilizatorul 'admin' în tabela 'users' cu parola criptată folosind SHA2
INSERT INTO users (username, password) 
VALUES 
    ('admin', SHA2('admin', 256));  -- Parola criptată cu SHA2
