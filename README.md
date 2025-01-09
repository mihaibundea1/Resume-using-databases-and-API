# Documentație Detaliată - Sistem Web de Autentificare și Profil Profesional

## 1. Prezentare Generală
Aplicația reprezintă un sistem web modern și complex care îmbină funcționalitățile de autentificare securizată cu prezentarea profesională a profilului utilizatorului. Sistemul este construit pe o arhitectură containerizată modernă, utilizând Docker pentru izolarea și gestionarea serviciilor. Această abordare asigură portabilitatea și scalabilitatea aplicației, permițând dezvoltarea și implementarea consistentă în diverse medii.

Aplicația este structurată în trei componente principale, fiecare rulând în propriul container Docker:
- **Frontend**: Interfață web interactivă și responsivă dezvoltată cu HTML5, CSS3 și JavaScript modern
- **Backend**: Server API RESTful implementat în Python folosind framework-ul Flask
- **Bază de date**: Sistem de stocare MariaDB pentru gestionarea sigură a datelor utilizatorilor

## 2. Arhitectura Sistemului

### 2.1 Componente Detaliate

#### Frontend
Interfața utilizator este construită folosind tehnologii web moderne și oferă:
- Sistem de autentificare cu validare în timp real
- Pagină de profil profesional cu secțiuni interactive
- Animații și tranziții fluide pentru o experiență îmbunătățită
- Integrare cu servicii externe (Google Maps)
- Design adaptiv pentru toate dispozitivele

#### Backend
Serverul API este implementat în Python/Flask și asigură:
- Procesarea securizată a cererilor de autentificare
- Validarea și sanitizarea datelor de intrare
- Gestionarea sesiunilor utilizator
- Comunicare optimizată cu baza de date
- Implementare CORS pentru securitate

#### Baza de date
Sistemul utilizează MariaDB pentru:
- Stocarea securizată a credențialelor utilizator
- Managementul eficient al datelor
- Backup și recuperare automată
- Optimizare pentru performanță

### 2.2 Arhitectura de Rețea
Sistemul utilizează o rețea Docker Bridge dedicată cu următoarea configurație:
- **Rețea**: provedb
- **Subnet**: 10.10.0.0/16
- **Gateway**: 10.10.0.1
- **Containere**:
  - maria-db: 10.10.0.2 (baza de date)
  - python-app: 10.10.0.3 (aplicația backend)

Această configurație asigură:
- Izolare completă a serviciilor
- Comunicare internă securizată
- Expunere controlată a serviciilor către exterior
- Scalabilitate orizontală

## 3. Implementare Backend

### 3.1 Configurare Detaliată Flask
Serverul Flask este configurat cu următoarele caracteristici:

```python
from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS
import hashlib

app = Flask(__name__)
CORS(app)  # Permite accesul cross-origin pentru dezvoltare
```

#### Endpoint-uri API:

1. **Login (/login)**:
   - Metodă: POST
   - Procesare date de autentificare
   - Validare credențiale
   - Generare răspuns JSON

2. **Register (/register)**:
   - Metodă: POST
   - Validare date noi utilizator
   - Verificare duplicat username
   - Criptare parolă
   - Creare cont nou

### 3.2 Securitate Backend
Implementarea include multiple niveluri de securitate:

1. **Criptare Parole**:
   - Utilizare SHA-256
   - Salt unic pentru fiecare utilizator
   - Validare complexitate parolă

2. **Validare Input**:
   - Sanitizare date primite
   - Verificare lungime și format
   - Prevenire SQL injection

3. **Gestionare Erori**:
   - Logging detaliat
   - Răspunsuri de eroare standardizate
   - Recuperare gracioasă din excepții

## 4. Structura și Configurare Bază de Date

### 4.1 Schema Detaliată
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    CONSTRAINT username_min_length CHECK (LENGTH(username) >= 3)
);
```

### 4.2 Indexare și Optimizare
- Index pentru căutare rapidă după username
- Constrângeri pentru integritatea datelor
- Optimizare query-uri frecvente

### 4.3 Backup și Recuperare
- Backup automat zilnic
- Retenție date 30 zile
- Procedură de recuperare documentată

## 5. Containerizare și Deployment

### 5.1 Docker Compose Detaliat
```yaml
services:
  maria-db:
    image: mariadb
    volumes:
      - ./data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    environment:
      MARIADB_ROOT_PASSWORD: pass1234
      MARIADB_DATABASE: myapp
      MARIADB_USER: admin
      MARIADB_PASSWORD: admin_password
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "--silent"]
      interval: 5s
      timeout: 5s
      retries: 10

  python-app:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - maria-db
```

### 5.2 Dockerfile Explicat
```dockerfile
# Imagine de bază optimizată pentru Python
FROM python:3.9-slim

# Directorul de lucru în container
WORKDIR /app

# Copiere fișiere aplicație
COPY . /app

# Creare și activare mediu virtual
RUN python -m venv venv
RUN . venv/bin/activate

# Instalare dependințe
COPY requirements.txt .
RUN . venv/bin/activate && pip install -r requirements.txt

# Expunere port aplicație
EXPOSE 5000

# Comandă pornire aplicație
CMD ["bash", "-c", ". venv/bin/activate && python main.py"]
```

## 6. Funcționalități Frontend Detaliate

### 6.1 Sistem de Autentificare
Implementarea frontend include:
- Validare input în timp real
- Feedback vizual pentru erori
- Animații pentru stări de eroare
- Tranziție fluidă între formulare
- Persistența sesiunii

### 6.2 Pagină de Profil
Profilul utilizatorului include:
- Header cu informații de contact
- Secțiune de competențe cu bare de progres
- Experiență profesională cronologică
- Educație și certificări
- Proiecte cu descrieri detaliate
- Hartă interactivă pentru locație

### 6.3 Integrări JavaScript
```javascript
// Exemplu de inițializare particles.js
particlesJS('particles-js', {
    particles: {
        number: { value: 50, density: { enable: true, value_area: 800 } },
        color: { value: '#4a90e2' },
        shape: { type: 'circle' },
        opacity: { value: 0.5, random: false },
        size: { value: 3, random: true },
        line_linked: { enable: true, distance: 150, color: '#4a90e2', opacity: 0.2 }
    }
});
```

## 7. Ghid de Instalare și Configurare

### 7.1 Cerințe Sistem
- Docker Engine 20.10+
- Docker Compose 2.0+
- 2GB RAM minim
- 10GB spațiu disk

### 7.2 Pași Instalare
1. Clonare repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Configurare variabile mediu:
   ```bash
   cp .env.example .env
   # Editare .env cu valorile dorite
   ```

3. Construire și pornire containere:
   ```bash
   docker-compose up --build
   ```

4. Verificare instalare:
   ```bash
   docker-compose ps
   curl http://localhost:5000/health
   ```

## 8. Monitorizare și Mentenanță

### 8.1 Logging
- Logs aplicație în /var/log/app
- Logs bază de date în /var/log/mysql
- Rotație logs la 7 zile

### 8.2 Monitoring
- Verificare health containere
- Monitorizare utilizare resurse
- Alertare pentru evenimente critice

## 9. Planificare Dezvoltare Viitoare

### 9.1 Îmbunătățiri Planificate
1. Autentificare:
   - Implementare JWT
   - Autentificare două factori
   - Integrare OAuth

2. Performanță:
   - Implementare Redis cache
   - Optimizare queries
   - CDN pentru assets statice

3. Funcționalități:
   - Editor profil
   - Export PDF CV
   - Integrare rețele sociale

## 10. Troubleshooting

### 10.1 Probleme Comune
1. Erori Conexiune DB:
   - Verificare credențiale
   - Testare conectivitate rețea
   - Verificare logs MariaDB

2. Erori Aplicație:
   - Verificare logs container
   - Validare configurație
   - Testare endpoint-uri

### 10.2 Proceduri Recuperare
1. Backup date
2. Restaurare configurație
3. Repornire servicii

## 11. Contact și Suport

Pentru asistență tehnică sau raportare probleme:
- Email: support@example.com
- GitHub Issues: [link repository]
- Documentație API: [link documentație]
