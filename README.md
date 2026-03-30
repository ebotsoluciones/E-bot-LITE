# 🦙 E-BOT LITE
### *"Llama que llama... por wasap"*

Bot de gestión de turnos por WhatsApp, construido con Twilio + Flask + Railway + PostgreSQL.

---

## ¿Qué hace?

Permite a un profesional independiente gestionar su agenda de turnos 100% desde WhatsApp — tanto el paciente como el profesional operan desde la misma aplicación que ya usan todos los días.

### Paciente puede:
- Sacar un turno eligiendo fecha y horario disponible
- Consultar sus turnos próximos
- Enviar un mensaje al consultorio
- Ver número de urgencias y horario de atención

### Profesional (admin) puede:
- Ver turnos del día y próximos turnos
- Cargar un turno manualmente
- Cancelar un turno
- Bloquear horarios o días completos
- Leer mensajes recibidos

### Notificaciones automáticas:
- ✅ Paciente recibe confirmación al sacar turno
- ❌ Paciente recibe aviso al cancelarse su turno
- 🔔 Admin recibe aviso cuando un paciente saca turno
- 🗑 Admin recibe aviso cuando se cancela un turno

---

## Stack

| Capa | Tecnología |
|------|-----------|
| Mensajería | Twilio WhatsApp API |
| Backend | Python + Flask |
| Deploy | Railway |
| Base de datos | PostgreSQL (Railway plugin) |

---

## Estructura del proyecto

```
ebot-lite/
├── app.py              # Servidor Flask + webhook Twilio
├── handlers.py         # Lógica conversacional del bot
├── services.py         # Turnos, bloqueos, mensajes
├── notifications.py    # Notificaciones WhatsApp proactivas
├── storage.py          # Abstracción multi-backend (postgres/memory/file)
├── config.py           # Variables de entorno
├── requirements.txt
├── Procfile
├── railway.toml
└── .env.example
```

---

## Deploy en Railway

### 1. Clonar y subir a GitHub
```bash
git clone https://github.com/tu-usuario/ebot-lite
```

### 2. Crear proyecto en Railway
- Nuevo proyecto → Deploy from GitHub repo
- Conectar el repo

### 3. Agregar PostgreSQL
- En el proyecto → **+ New** → **Database** → **PostgreSQL**
- Railway inyecta `DATABASE_URL` automáticamente

### 4. Configurar variables de entorno
En Railway → Variables → Raw Editor:

```
NOMBRE_CONSULTORIO=Consultorio Ejemplo
NOMBRE_PROFESIONAL=Dr. Juan Pérez
MODO_TEST=false
ADMINS=whatsapp:+5491100000000
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
STORAGE_BACKEND=postgres
HORA_INICIO=09:00
HORA_FIN=19:00
INTERVALO_MIN=60
```

### 5. Configurar webhook en Twilio
En Twilio Console → Messaging → WhatsApp Sandbox:
```
https://tu-dominio.up.railway.app/webhook
```
Método: **HTTP POST**

---

## Variables de entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `NOMBRE_CONSULTORIO` | Nombre que aparece en el menú | `Consultorio San Martín` |
| `NOMBRE_PROFESIONAL` | Nombre del profesional (opcional) | `Dra. García` |
| `ADMINS` | Números admin separados por coma | `whatsapp:+5491100000000` |
| `MODO_TEST` | `true` activa acceso admin con "adm" | `false` |
| `TWILIO_ACCOUNT_SID` | Credencial Twilio | `ACxxx...` |
| `TWILIO_AUTH_TOKEN` | Credencial Twilio | `xxx...` |
| `TWILIO_WHATSAPP_FROM` | Número WhatsApp del bot | `whatsapp:+14155238886` |
| `STORAGE_BACKEND` | `postgres` / `memory` / `file` | `postgres` |
| `NOTIF_ADMIN_TEL` | Número para notificaciones admin (opcional, default: ADMINS[0]) | `whatsapp:+5491199999999` |
| `HORA_INICIO` | Primer horario del día | `09:00` |
| `HORA_FIN` | Último horario del día | `19:00` |
| `INTERVALO_MIN` | Duración de cada turno en minutos | `60` |

---

## Uso desde WhatsApp

**Paciente:** escribir `menu` para iniciar  
**Admin:** el número configurado en `ADMINS` entra automáticamente al panel

---

## Licencia

Producto comercial — E-BOT 🦙 *"Llama que llama... por wasap"*
