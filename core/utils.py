#!/usr/bin/env python3
from typing import Optional
from datetime import datetime


def format_money(amount: float, currency_symbol: str) -> str:
    try:
        return f"{currency_symbol}{float(amount):.2f}"
    except Exception:
        return f"{currency_symbol}0.00"


def format_datetime(dt: Optional[datetime]) -> str:
    if not dt:
        return ""
    try:
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(dt)


def get_currency_symbol(ejecutar_query) -> str:
    """Obtener símbolo de moneda desde la BD usando un callback de ejecución de query."""
    try:
        result = ejecutar_query("SELECT valor FROM configuracion WHERE clave = 'moneda'")
        if result and result[0] and result[0][0]:
            return result[0][0]
    except Exception:
        pass
    return "S/"


