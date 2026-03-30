import os

# ── Identidad del bot ─────────────────────────────────────────────────────────
NOMBRE_CONSULTORIO = os.getenv("NOMBRE_CONSULTORIO", "Consultorio")
NOMBRE_PROFESIONAL = os.getenv("NOMBRE_PROFESIONAL", "")

# ── Modo ──────────────────────────────────────────────────────────────────────
MODO_TEST = os.getenv("MODO_TEST", "false").lower() == "true"

# ── Admins ────────────────────────────────────────────────────────────────────
# Formato: whatsapp:+5491100000000,whatsapp:+5491199999999
_admins_raw = os.getenv("ADMINS", "")
ADMINS = [a.strip() for a in _admins_raw.split(",") if a.strip()]

# ── Notificaciones ────────────────────────────────────────────────────────────
# Por ahora usa el mismo número del bot (TWILIO_WHATSAPP_FROM)
# Para cambiar a número separado: setear NOTIF_ADMIN_TEL=whatsapp:+549XXXXXXXXXX
NOTIF_ADMIN_TEL = os.getenv("NOTIF_ADMIN_TEL", "")  # vacío = usa ADMINS[0]

# ── Twilio ────────────────────────────────────────────────────────────────────
TWILIO_ACCOUNT_SID   = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN    = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

# ── Storage ───────────────────────────────────────────────────────────────────
# postgres  →  Railway PostgreSQL (producción)
# memory    →  RAM (pruebas)
# file      →  JSON local (desarrollo)
STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "postgres")
DATABASE_URL     = os.getenv("DATABASE_URL", "")

# ── Claves de storage ─────────────────────────────────────────────────────────
ESTADO_KEY   = "estados_usuarios"
TURNOS_FILE   = "turnos"
BLOQUEOS_FILE = "bloqueos"
MENSAJES_FILE = "mensajes"

# ── Horarios ──────────────────────────────────────────────────────────────────
HORA_INICIO = os.getenv("HORA_INICIO", "09:00")
HORA_FIN    = os.getenv("HORA_FIN",    "19:00")
INTERVALO   = int(os.getenv("INTERVALO_MIN", "60"))  # minutos
