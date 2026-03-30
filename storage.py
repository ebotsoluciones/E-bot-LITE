"""
storage.py — abstracción de persistencia multi-backend

Backends (STORAGE_BACKEND):
  postgres  →  Railway PostgreSQL (producción)
  memory    →  dict en RAM (pruebas)
  file      →  JSON en disco (desarrollo local)
"""

import json
import os
from config import STORAGE_BACKEND, DATABASE_URL

# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY
# ═══════════════════════════════════════════════════════════════════════════════

_store: dict = {}

def _mem_get(key: str) -> dict:
    return _store.get(key, {})

def _mem_set(key: str, value: dict):
    _store[key] = value


# ═══════════════════════════════════════════════════════════════════════════════
# FILE
# ═══════════════════════════════════════════════════════════════════════════════

def _file_get(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _file_set(path: str, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# POSTGRES
# ═══════════════════════════════════════════════════════════════════════════════

_pg_conn = None

def _get_pg():
    global _pg_conn
    if _pg_conn is None or _pg_conn.closed:
        import psycopg2
        _pg_conn = psycopg2.connect(DATABASE_URL)
        _pg_conn.autocommit = True
        with _pg_conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS kv_store (
                    key  TEXT PRIMARY KEY,
                    val  TEXT NOT NULL
                )
            """)
    return _pg_conn

def _pg_get(key: str) -> dict:
    conn = _get_pg()
    with conn.cursor() as cur:
        cur.execute("SELECT val FROM kv_store WHERE key = %s", (key,))
        row = cur.fetchone()
    return json.loads(row[0]) if row else {}

def _pg_set(key: str, value: dict):
    conn = _get_pg()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO kv_store (key, val) VALUES (%s, %s)
            ON CONFLICT (key) DO UPDATE SET val = EXCLUDED.val
        """, (key, json.dumps(value, ensure_ascii=False)))


# ═══════════════════════════════════════════════════════════════════════════════
# API PÚBLICA
# ═══════════════════════════════════════════════════════════════════════════════

def cargar_json(key: str) -> dict:
    if STORAGE_BACKEND == "postgres":
        return _pg_get(key)
    if STORAGE_BACKEND == "file":
        return _file_get(key)
    return _mem_get(key)

def guardar_json(key: str, data: dict):
    if STORAGE_BACKEND == "postgres":
        _pg_set(key, data)
        return
    if STORAGE_BACKEND == "file":
        _file_set(key, data)
        return
    _mem_set(key, data)
