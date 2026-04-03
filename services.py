"""
services.py — lógica de negocio E-BOT LITE 🦙
"""

from datetime import datetime
from storage import cargar_json, guardar_json
from config  import TURNOS_FILE, BLOQUEOS_FILE, MENSAJES_FILE, HORA_INICIO, HORA_FIN, INTERVALO
from notifications import (
    notif_paciente_confirmado,
    notif_paciente_cancelado,
    notif_admin_nuevo_turno,
    notif_admin_cancelado,
)

HISTORIAL_FILE = "historial"

# ═══════════════════════════════════════════════════════════════════════════════
# HORARIOS
# ═══════════════════════════════════════════════════════════════════════════════

def generar_horarios() -> list[str]:
    h_ini = datetime.strptime(HORA_INICIO, "%H:%M")
    h_fin = datetime.strptime(HORA_FIN,    "%H:%M")
    horarios = []
    actual = h_ini
    while actual <= h_fin:
        horarios.append(actual.strftime("%H:%M"))
        from datetime import timedelta
        actual += timedelta(minutes=INTERVALO)
    return horarios

def normalizar_hora(texto: str):
    texto = texto.strip().replace(".", ":").replace("-", ":")
    if ":" not in texto:
        texto += ":00"
    partes = texto.split(":")
    try:
        h, m = int(partes[0]), int(partes[1])
        return f"{h:02d}:{m:02d}"
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# HISTORIAL (todos los turnos, incluso cancelados)
# ═══════════════════════════════════════════════════════════════════════════════

def obtener_historial() -> list[dict]:
    return cargar_json(HISTORIAL_FILE).get("data", [])

def _guardar_historial(datos: list[dict]):
    guardar_json(HISTORIAL_FILE, {"data": datos})


# ═══════════════════════════════════════════════════════════════════════════════
# TURNOS
# ═══════════════════════════════════════════════════════════════════════════════

def obtener_turnos() -> list[dict]:
    return cargar_json(TURNOS_FILE).get("data", [])

def guardar_turnos(turnos: list[dict]):
    guardar_json(TURNOS_FILE, {"data": turnos})

def agregar_turno(nombre: str, telefono: str, fecha: str, hora: str):
    turno = {
        "nombre":    nombre,
        "telefono":  telefono,
        "fecha":     fecha,
        "hora":      hora,
        "creado_en": datetime.now().isoformat(),
    }
    # Guardar en turnos activos
    turnos = obtener_turnos()
    turnos.append(turno)
    guardar_turnos(turnos)
    # Guardar en historial
    historial = obtener_historial()
    historial.append(turno)
    _guardar_historial(historial)
    # Notificaciones
    notif_paciente_confirmado(telefono, nombre, fecha, hora)
    notif_admin_nuevo_turno(nombre, telefono, fecha, hora)

def cancelar_turno(telefono: str, fecha: str, hora: str):
    turnos    = obtener_turnos()
    turno     = next((t for t in turnos if t["telefono"] == telefono and t["fecha"] == fecha and t["hora"] == hora), None)
    restantes = [t for t in turnos if not (t["telefono"] == telefono and t["fecha"] == fecha and t["hora"] == hora)]
    guardar_turnos(restantes)
    if turno:
        notif_paciente_cancelado(telefono, turno["nombre"], fecha, hora)
        notif_admin_cancelado(turno["nombre"], telefono, fecha, hora)

def turnos_usuario(telefono: str) -> list[dict]:
    hoy = datetime.now().date()
    return [
        t for t in obtener_turnos()
        if t["telefono"] == telefono
        and datetime.strptime(t["fecha"], "%d/%m/%Y").date() >= hoy
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUEOS
# ═══════════════════════════════════════════════════════════════════════════════

def _obtener_bloqueos() -> list[dict]:
    return cargar_json(BLOQUEOS_FILE).get("data", [])

def _guardar_bloqueos(bloqueos: list[dict]):
    guardar_json(BLOQUEOS_FILE, {"data": bloqueos})

def horario_bloqueado(fecha: str, hora: str) -> bool:
    return any(b["fecha"] == fecha and b["hora"] == hora for b in _obtener_bloqueos())

def bloquear_horario(fecha: str, hora: str):
    bloqueos = _obtener_bloqueos()
    if not horario_bloqueado(fecha, hora):
        bloqueos.append({"fecha": fecha, "hora": hora})
        _guardar_bloqueos(bloqueos)

def horarios_libres(fecha: str) -> list[str]:
    turnos   = {t["hora"] for t in obtener_turnos()  if t["fecha"] == fecha}
    bloqueos = {b["hora"] for b in _obtener_bloqueos() if b["fecha"] == fecha}
    ocupados = turnos | bloqueos
    return [h for h in generar_horarios() if h not in ocupados]

def horarios_para_bloquear(fecha: str) -> list[str]:
    """Retorna horarios que aún no están bloqueados para esa fecha."""
    bloqueados = {b["hora"] for b in _obtener_bloqueos() if b["fecha"] == fecha}
    return [h for h in generar_horarios() if h not in bloqueados]


# ═══════════════════════════════════════════════════════════════════════════════
# MENSAJES
# ═══════════════════════════════════════════════════════════════════════════════

def guardar_mensaje(nombre: str, telefono: str, mensaje: str):
    data = cargar_json(MENSAJES_FILE)
    data.setdefault("data", []).append({
        "nombre":   nombre,
        "telefono": telefono,
        "mensaje":  mensaje,
        "fecha":    datetime.now().isoformat(),
    })
    guardar_json(MENSAJES_FILE, data)

def limpiar_mensajes():
    guardar_json(MENSAJES_FILE, {"data": []})
