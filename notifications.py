"""
notifications.py — envío proactivo de mensajes WhatsApp vía Twilio

Notificaciones implementadas:
  - Paciente: turno confirmado
  - Paciente: turno cancelado
  - Admin:    nuevo turno sacado por paciente
  - Admin:    turno cancelado por paciente
"""

from twilio.rest import Client
from config import (
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM,
    NOMBRE_CONSULTORIO, NOMBRE_PROFESIONAL, ADMINS, NOTIF_ADMIN_TEL,
)


def _cliente():
    return Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def _destino_admin() -> str:
    """Retorna el número al que se notifica al admin."""
    if NOTIF_ADMIN_TEL:
        return NOTIF_ADMIN_TEL
    if ADMINS:
        return ADMINS[0]
    return ""


def _enviar(para: str, mensaje: str):
    """Envía un mensaje WhatsApp. Silencia errores para no romper el flujo."""
    if not para:
        return
    try:
        _cliente().messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=para,
            body=mensaje,
        )
    except Exception as e:
        print(f"[NOTIF ERROR] {e}")


def _firma() -> str:
    if NOMBRE_PROFESIONAL:
        return f"{NOMBRE_CONSULTORIO} — {NOMBRE_PROFESIONAL}"
    return NOMBRE_CONSULTORIO


# ── Paciente: turno confirmado ────────────────────────────────────────────────

def notif_paciente_confirmado(telefono: str, nombre: str, fecha: str, hora: str):
    msg = (
        f"✅ *Turno confirmado*\n"
        f"Hola {nombre}, tu turno quedó registrado.\n"
        f"📅 {fecha} a las {hora} hs\n\n"
        f"Ante cualquier consulta respondé este mensaje.\n"
        f"_{_firma()}_"
    )
    _enviar(telefono, msg)


# ── Paciente: turno cancelado ─────────────────────────────────────────────────

def notif_paciente_cancelado(telefono: str, nombre: str, fecha: str, hora: str):
    msg = (
        f"❌ *Turno cancelado*\n"
        f"Hola {nombre}, tu turno del {fecha} a las {hora} hs fue cancelado.\n\n"
        f"Podés sacar un nuevo turno cuando quieras.\n"
        f"_{_firma()}_"
    )
    _enviar(telefono, msg)


# ── Admin: nuevo turno ────────────────────────────────────────────────────────

def notif_admin_nuevo_turno(nombre: str, telefono: str, fecha: str, hora: str):
    destino = _destino_admin()
    msg = (
        f"🔔 *Nuevo turno*\n"
        f"👤 {nombre}\n"
        f"📱 {telefono}\n"
        f"📅 {fecha} a las {hora} hs"
    )
    _enviar(destino, msg)


# ── Admin: turno cancelado ────────────────────────────────────────────────────

def notif_admin_cancelado(nombre: str, telefono: str, fecha: str, hora: str):
    destino = _destino_admin()
    msg = (
        f"🗑 *Turno cancelado*\n"
        f"👤 {nombre}\n"
        f"📱 {telefono}\n"
        f"📅 {fecha} a las {hora} hs"
    )
    _enviar(destino, msg)
