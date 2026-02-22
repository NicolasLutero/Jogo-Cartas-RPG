# auxiliares.py
from flask import session
from datetime import datetime, timezone, timedelta


# -----------------------------------------------
# AUXILIAR
# -----------------------------------------------
def verificar_sessao():
    if "usuario" not in session:
        return False

    data_login = datetime.fromtimestamp(session["usuario"]["timestamp"], timezone.utc)
    agora = datetime.now(timezone.utc)

    if agora - data_login > timedelta(hours=12):
        session.clear()
        return False

    return True
