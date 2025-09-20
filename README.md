# Hash Cracker Pro

Una herramienta moderna para identificación y cracking de hashes criptográficos, construida con Python Flask backend y Vue.js frontend.
Se actualizara de manera constante agregando nuevos metodos de hashes, esto con la intencion de facilitar en la participacion de CTF´s.
Este programa es para fines educativos y muestra técnicas reales de pentesting. 
Para cracking profesional, se recomienda usar herramientas como Hashcat o John the Ripper con hardware especializado.

# Es importante tener descargados los siguientes documentos para facilitar el uso del programa:
- rockyou.txt (14 millones de contraseñas)  
wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt

- Wordlists adicionales  
wget https://github.com/danielmiessler/SecLists/archive/master.zip

- unzip master.zip

## Características

- **Identificación automática** de tipos de hash (MD5, SHA-1, SHA-256, SHA-512, etc.)
- **Cracking con diccionario** de contraseñas comunes
- **Interfaz web moderna** con Element Plus
- **API RESTful** con Flask
- **Procesamiento multi-hilo** para mejor performance
- **Detección en tiempo real** del progreso de cracking

## Tecnologías

- **Backend**: Python 3, Flask, Flask-CORS
- **Frontend**: Vue.js 3, Element Plus, Axios
- **Hashing**: hashlib (MD5, SHA-1, SHA-256, SHA-512)

## Instalación

### Prerrequisitos
- Python 3.8+
- Node.js 14+
- npm o yarn

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py

### Frontend
cd fronted
npm install
npm run serve
