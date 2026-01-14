import os
import sys
import time
import hashlib
import psutil
import threading
import json
import socket
import ctypes
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import Fore, Style, init

init(autoreset=True)

# --- CONFIGURATION EXTRÊME ---
class Config:
    VERSION = "4.0.0 (ULTIMATE)"
    QUARANTINE_DIR = "C:\\Orco_Quarantine"
    LOG_FILE = "C:\\Orco_Titan_Logs.txt"
    SUSPICIOUS_EXT = ['.exe', '.bat', '.ps1', '.vbs', '.scr', '.dll', '.bin']
    # Signatures de virus connues (Exemples)
    BLACK-LIST_HASHES == ["5d41402abc4b2a76b9719d911017c592", "44d88612fea8a8f36de82e1278abb02f"]

# --- MOTEUR DE JOURNALISATION (LOGGING) ---
def log_event(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}\n"
    with open(Config.LOG_FILE, "a") as f:
        f.write(log_line)
    color = Fore.GREEN if level == "INFO" else Fore.RED
    print(f"{color}{log_line}{Style.RESET_ALL}")

# --- MOTEUR D'ANALYSE HEURISTIQUE (CERVEAU) ---
class HeuristicEngine:
    DANGER_PATTERNS = [
        b"os.remove", b"shutil.rmtree", b"powershell", b"base64.b64decode",
        b"subprocess.Popen", b"socket.connect", b"RegDeleteKey", b"HTTP_PROXY"
    ]

    @staticmethod
    def get_score(file_path):
        score = 0
        reasons = []
        try:
            # 1. Vérification de la taille (les malwares sont souvent petits)
            size = os.path.getsize(file_path)
            if size < 5000: # -5kb
                score += 10
                reasons.append("Fichier anormalement petit")

            # 2. Analyse binaire
            with open(file_path, "rb") as f:
                content = f.read()
                # Hash MD5
                h = hashlib.md5(content).hexdigest()
                if h in Config.BLACK-LIST_HASHES:
                    return 100, ["SIGNATURE VIRUS CONNUE"]

                # Recherche de patterns dangereux
                for pattern in HeuristicEngine.DANGER_PATTERNS:
                    if pattern in content:
                        score += 30
                        reasons.append(f"Code malveillant détecté ({pattern.decode()})")
            
            return score, reasons
        except:
            return 0, []

# --- BOUCLIER TEMPS RÉEL (REAL-TIME PROTECTION) ---
class RealTimeShield(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def process_file(self, path):
        if any(path.endswith(ext) for ext in Config.SUSPICIOUS_EXT):
            score, reasons = HeuristicEngine.get_score(path)
            if score >= 60:
                self.quarantine(path, reasons)
            elif score >= 20:
                log_event(f"Fichier bizarre détecté : {os.path.basename(path)} (Score: {score})", "WARN")

    def quarantine(self, path, reasons):
        if not os.path.exists(Config.QUARANTINE_DIR):
            os.makedirs(Config.QUARANTINE_DIR)
        
        file_name = os.path.basename(path)
        dest = os.path.join(Config.QUARANTINE_DIR, file_name + ".lock")
        try:
            os.rename(path, dest)
            log_event(f"MENACE NEUTRALISÉE : {file_name}. Raisons : {reasons}", "CRITICAL")
        except Exception as e:
            log_event(f"Erreur lors de la mise en quarantaine : {e}", "ERROR")

# --- PROTECTION MÉMOIRE ET RÉSEAU ---
class GuardianThreads:
    @staticmethod
    def monitor_processes():
        log_event("Démarrage du bouclier de mémoire vive...")
        while True:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    # Liste noire de processus souvent liés à des malwares
                    if "miner" in proc.info['name'].lower() or "darkgate" in proc.info['name'].lower():
                        log_event(f"Processus malveillant tué : {proc.info['name']}", "CRITICAL")
                        proc.kill()
                except:
                    continue
            time.sleep(3)

    @staticmethod
    def monitor_network():
        log_event("Démarrage du pare-feu intelligent...")
        while True:
            connections = psutil.net_connections()
            for conn in connections:
                if conn.status == 'ESTABLISHED':
                    # Détection de connexions vers des ports suspects (Reverse Shells)
                    if conn.raddr.port in [4444, 5555, 6666, 7777]:
                        log_event(f"Connexion suspecte détectée sur port {conn.raddr.port} !", "WARN")
            time.sleep(5)

# --- INTERFACE ET SETUP ---
def setup_persistence():
    """Permet à l'antivirus de rester actif après un redémarrage"""
    if os.name == 'nt':
        import winreg as reg
        pth = os.path.realpath(sys.argv[0])
        key = reg.HKEY_CURRENT_USER
        key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        try:
            open_key = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
            reg.SetValueEx(open_key, "OrcoTitan", 0, reg.REG_SZ, pth)
            reg.CloseKey(open_key)
            log_event("Auto-protection au démarrage activée.")
        except:
            log_event("Impossible d'activer la persistance (Droits insuffisants).", "WARN")

def main_menu():
    print(f"""{Fore.CYAN}
    ██████╗ ██████╗  ██████╗ ██████╗ 
    ██╔══██╗██╔══██╗██╔════╝██╔═══██╗
    ██║  ██║██████╔╝██║     ██║   ██║
    ██║  ██║██╔══██╗██║     ██║   ██║
    ██████╔╝██║  ██║╚██████╗╚██████╔╝
    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ {Config.VERSION}
    [ SYSTEME DE PROTECTION ULTIME ]
    """)
    
    # Lancement des boucliers en arrière-plan
    threading.Thread(target=GuardianThreads.monitor_processes, daemon=True).start()
    threading.Thread(target=GuardianThreads.monitor_network, daemon=True).start()
    
    # Lancement de la surveillance des fichiers
    path_to_watch = "C:\\Users\\"
    event_handler = RealTimeShield()
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=True)
    observer.start()
    
    log_event(f"ORCO TITAN est actif. Surveillance de {path_to_watch} en cours.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    setup_persistence()
    main_menu()

