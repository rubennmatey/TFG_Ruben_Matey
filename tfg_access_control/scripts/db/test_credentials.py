from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.db.credentials_actions import create_credential
from app.db.credentials_actions import list_credentials


def create():
    examples = [("49724e06", "Tarjeta Ruben", "admin", 1), ("a31d1656", "Tarjeta Invitado", "user", 0)]

    for uid, alias, role, active in examples:
        try:
            create_credential(uid, alias, role, active)
            print(f"Credencial creada: {uid} - {alias}")
        except Exception as e:
            print(f"No se pudo crear {uid}: {e}")
    
    print("\nCredenciales en la base de datos: ")
    for row in list_credentials():
        print(dict(row))
    
if __name__ == "__main__":
    create()