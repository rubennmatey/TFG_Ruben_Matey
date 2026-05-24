# 🔐 IoT Access Control System with NFC, BLE & Blockchain

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-green)
![Blockchain](https://img.shields.io/badge/Blockchain-Ethereum%20\(Ganache\)-orange)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

> An access control system based on Raspberry Pi that combines **NFC**, **Bluetooth Low Energy (BLE)** and **Blockchain** to provide physical authentication, remote management and log integrity verification.

---

# 🧠 Project Overview

This project implements a complete access control system where:

* 🔹 Physical access is performed using **NFC cards**
* 🔹 System management is done via **BLE from a mobile device**
* 🔹 Data is stored locally using **SQLite**
* 🔹 **Blockchain** is used for:

  * recording administrative actions
  * ensuring integrity of access logs through hash anchoring
  * storing credentials

The system follows a hybrid architecture where critical operations run locally, while blockchain provides **auditability and integrity guarantees**.

---

# 🏗️ System Architecture

```
          📱 Mobile (BLE)
                │
                ▼
        ┌─────────────────┐
        │  Raspberry Pi   │
        │                 │
        │  🔹 NFC Reader  │
        │  🔹 BLE Server  │
        │  🔹 Logic       │
        └───────┬─────────┘
                │
        ┌───────▼─────────┐
        │     SQLite      │
        │ (logs & creds)  │
        └───────┬─────────┘
                │
                ▼
        🔗 Blockchain (Ethereum)
        - Admin actions
        - Log batch hashes
        - Credentials
```

---

# 🚀 Key Features

## 🔐 Access Control

* NFC-based authentication
* Local decision-making (fast and offline-capable)
* Access logging in SQLite

## 📡 Remote Management (BLE)

* List credentials
* Enable / disable credentials
* Register new NFC cards
* Retrieve logs

## 🗄️ Local Database

* Credentials
* Access logs
* Administrative actions
* Log batches

## 🔗 Blockchain Integration

### 1. Administrative actions

* Credential registration
* Enable / disable operations
* Immutable storage on blockchain

### 2. Log integrity

* Logs grouped into batches
* SHA-256 hash computation
* Hash anchoring on blockchain
* Integrity verification

### 3. Credentials

* Credentials stored on blockchain
* Credential verification
* Modified credentials 

---

# ⚙️ Installation

## 1. Clone repository

```bash
git clone <repo_url>
cd tfg_access_control
```

---

## 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. System dependencies (Raspberry Pi)

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv bluetooth bluez libbluetooth-dev build-essential libffi-dev libssl-dev libgpiod-dev i2c-tools
```

---

## 5. Enable I2C (NFC)

```bash
sudo raspi-config
```

```
Interface Options → I2C → Enable
```

Reboot:

```bash
sudo reboot
```

---

## 6. Configure Blockchain

Run Ganache on your PC and set:

```python
app/config.py
```

```python
BLOCKCHAIN_RPC_URL = "http://YOUR_IP:7545"
```

---

## 7. Initialize database

```bash
python app/db/migrations/init_schema.py
```

---

# ▶️ Run the system

```bash
python scripts/run_system.py
```

---

# 📱 BLE Usage (nRF Connect)

1. Connect to:

```
TFG_ACCESS
```

2. Use:

* `COMMAND` → write commands
* `RESPONSE` → read output
* `LAST_EVENT` → system events

---

# 📡 BLE Commands

## General

```
PING → PONG
```

## Credentials

```
LIST_CREDENTIALS
GET_CREDENTIAL:<UID>
```

## Management

```
DISABLE_UID:<UID>
ENABLE_UID:<UID>
```

## Enrollment

```
START_ENROLL
STOP_ENROLL
GET_LAST_ENROLL
```

---

# 🔗 Blockchain

## Stored data

### Administrative actions

```
DISABLE_UID
ENABLE_UID
ENROLL_UID
```

### Log batches

```
hash(batch_logs)
```

---

## Synchronization strategy

* ⚡ Immediate synchronization after events
* 🔄 Periodic backup synchronization

---

# 🧪 Integrity verification

```bash
python scripts/blockchain/verify_log_batch_integrity.py <batch_id>
```

## Expected result

✔ No changes:

```
ok: True
```

❌ If tampered:

```
ok: False
```

---

# 📂 Project Structure

```
app/
 ├── ble/
 ├── nfc/
 ├── db/
 ├── services/
 ├── blockchain/

scripts/
 ├── access/
 ├── blockchain/
 ├── db/
 ├── batch/
```

---

# 🧑‍💻 Technologies

* Python
* Raspberry Pi
* NFC (PN532)
* Bluetooth Low Energy (BlueZ + Bluezero)
* SQLite
* Ethereum (Ganache)
* Web3.py

---

# 🎯 Conclusion

This system provides a complete access control solution combining:

* IoT (NFC + Raspberry Pi)
* Wireless communication (BLE)
* Local persistence (SQLite)
* Blockchain as an audit and integrity layer

Resulting in a system that is:

* ⚡ fast (local decisions)
* 🔒 secure (credential control)
* 🔗 verifiable (blockchain integrity)

---

# 👤 Author

Rubén Matey
Bachelor's Thesis - Computer Engineering
