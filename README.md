# Hash Cracker Pro

Una herramienta moderna para identificación y cracking de hashes criptográficos, construida con Python Flask backend y Vue.js frontend.

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