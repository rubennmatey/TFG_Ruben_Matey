import time
import threading

from app.nfc.NFCReader import NFCReader
from app.core.access_controller import check_access
from app.ble.BLEServer import BLEServer
from app.services.enrollment_service import EnrollmentService
from app.services.batch_service import create_logs_batch
from app.services.log_batch_sync_service import (
    sync_one_log_batch,
    sync_all_log_batches,
)
from app.services.admin_action_sync_service import (
    sync_one_pending_admin_action,
    sync_all_pending_admin_actions,
)
from app.config import SYNC_BACKUP_INTERVAL_SECONDS, LOG_BATCH_SIZE


class AccessControlSystem:
    # Initializes the access control system components (NFC, BLE, enrollment)
    def __init__(self):
        self.reader = NFCReader()
        self.enrollment_service = EnrollmentService()
        self.ble = BLEServer(enrollment_service=self.enrollment_service)
        self.running = True

    # Starts the BLE server in a background daemon thread
    def start_ble(self):
        ble_thread = threading.Thread(target=self.ble.start, daemon=True)
        ble_thread.start()

    # Starts the periodic backup sync loop in a background daemon thread
    def start_periodic_backup_sync(self):
        backup_thread = threading.Thread(target=self._periodic_backup_sync_loop, daemon=True)
        backup_thread.start()

    # Sync all pending actions after 30 SECS (backup)
    def _periodic_backup_sync_loop(self):
        while self.running:
            try:
                print("[BACKUP_SYNC] Revisando acciones admin pendientes...")
                admin_result = sync_all_pending_admin_actions()
                print(f"[BACKUP_SYNC] Admin result: {admin_result}")

                print("[BACKUP_SYNC] Revisando lotes pendientes...")
                batch_result = sync_all_log_batches()
                print(f"[BACKUP_SYNC] Batch result: {batch_result}")

            except Exception as e:
                print(f"[BACKUP_SYNC] Error general en sincronización de respaldo: {e}")

            time.sleep(SYNC_BACKUP_INTERVAL_SECONDS)

    # Sync with blockchain after an action
    def _try_immediate_admin_sync(self):
        try:
            result = sync_one_pending_admin_action()
            print(f"[IMMEDIATE_SYNC][ADMIN] {result}")
        except Exception as e:
            print(f"[IMMEDIATE_SYNC][ADMIN] Error: {e}")

    # Creation and sync of batch with blockchain
    def _try_create_and_sync_log_batch(self):
        try:
            batch_id, logs = create_logs_batch(batch_size=LOG_BATCH_SIZE)

            if batch_id is None:
                return

            print(f"[BATCH] Lote creado automáticamente: {batch_id}")

            result = sync_one_log_batch()
            print(f"[IMMEDIATE_SYNC][BATCH] {result}")

        except Exception as e:
            print(f"[IMMEDIATE_SYNC][BATCH] Error: {e}")

    # Main loop
    def run(self):
        self.start_ble()
        self.start_periodic_backup_sync()

        print("Sistema principal iniciado. Esperando tarjetas...")

        while self.running:
            uid = self.reader.read_uid()

            if uid:
                print(f"\nTarjeta detectada: {uid}")

                enroll_result = self.enrollment_service.handle_nfc_for_enrollment(uid)
                if enroll_result is not None:
                    print(f"[ENROLL] {enroll_result}")
                    self.ble.update_value(enroll_result)

                    # alta de credencial -> acción admin -> intentar sync inmediata
                    if enroll_result.startswith("ENROLLED:"):
                        self._try_immediate_admin_sync()

                    time.sleep(2)
                    continue

                result = check_access(uid)
                print(result)

                message = f"{result['result']}:{uid}"
                self.ble.update_value(message)

                # tras cada acceso: intentar crear lote y sincronizarlo si toca
                self._try_create_and_sync_log_batch()

                time.sleep(2)