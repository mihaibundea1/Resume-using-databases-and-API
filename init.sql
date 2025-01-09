-- Selectează baza de date
USE myapp;

-- Creează tabela pentru utilizatori
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Verifică dacă utilizatorul 'admin' există și, dacă nu, creează-l
CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'admin_password';

-- Atribuie toate privilegiile pe baza de date 'myapp' pentru utilizatorul 'admin'
GRANT ALL PRIVILEGES ON myapp.* TO 'admin'@'%' WITH GRANT OPTION;

-- Permite conectarea de pe orice host
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' IDENTIFIED BY 'admin_password' WITH GRANT OPTION;

-- Aplică modificările
FLUSH PRIVILEGES;

-- Adaugă utilizatorul 'admin' în tabela 'users' cu parola criptată folosind SHA2
INSERT INTO users (username, password) 
VALUES 
    ('admin', SHA2('admin', 256));  -- Parola criptată cu SHA2
