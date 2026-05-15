from pathlib import Path
import sys
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app.db.credentials_actions import create_credential, list_credentials
from app.blockchain.credential_chain_service import send_credential_event_to_blockchain


def seed():
    sample_credentials = [
        ("49724e06", "Tarjeta Ruben", "admin", 1),
        ("a31d1656", "Tarjeta Invitado", "user", 0),
    ]

    for uid, alias, role, active in sample_credentials:
        try:
            create_credential(uid, alias, role, active)
            print(f"Credencial creada en SQLite: {uid} - {alias}")

            try:
                result = send_credential_event_to_blockchain(
                    uid=uid,
                    action_type="INITIAL_REGISTER",
                    role=role,
                    active=bool(active)
                )

                print(f"Credencial inicial sincronizada en blockchain: {result}")

            except Exception as e:
                print(f"ERROR sincronizando credencial inicial en blockchain {uid}: {e}")

        except sqlite3.IntegrityError:
            print(f"La credencial ya existe en SQLite, no se vuelve a registrar: {uid}")

        except Exception as e:
            print(f"No se pudo crear la credencial {uid}: {e}")

    print("\nCredenciales en la base de datos:")
    for row in list_credentials():
        print(dict(row))


if __name__ == "__main__":
    seed()