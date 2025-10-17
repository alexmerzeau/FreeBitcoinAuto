import requests
import time
import hashlib
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote
import os
import random

# --- Constants and Configuration ---
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

# --- User-specific credentials ---
COOKIE = os.environ.get('FBTC_COOKIE', '')
CSRF_TOKEN = os.environ.get('FBTC_CSRF_TOKEN', '')
USER_ID = os.environ.get('FBTC_USER_ID', '')

# --- Telegram Configuration ---
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')


# --- Global Variables ---
headers = {
    'User-Agent': USER_AGENT,
    'Cookie': COOKIE,
    'accept': ACCEPT
}

class ScriptError(Exception):
    """Custom exception for script-related errors."""
    pass

def send_telegram_message(message):
    """Sends a message to the specified Telegram chat."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram token or chat ID not set. Skipping notification.")
        return

    # The 'quote' function is used to URL-encode the message
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={quote(message)}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to send Telegram message. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending Telegram message: {e}")


def fingerprint():
    """
    Generates a browser fingerprint similar to the one used by the website.
    """
    md5 = hashlib.md5()
    md5.update(('###'.join([USER_AGENT,
                            'x'.join(['1024', '1280', '24']),'-420','true','true',
                            '::'.join(['BookReader', '',
                                       'application/epub+zip~epub,application/x-fictionbook+xml~fb2,application/x-zip-compressed-fb2~fb2.zip;Chromium PDF Plugin',
                                       'Portable Document Format', 'application/x-google-chrome-pdf~;Chromium PDF Viewer', '', 'application/pdf~pdf;Native Client','',
                                       'application/x-nacl~,application/x-pnacl~;Shockwave Flash',
                                       'Shockwave Flash 32.0 r0::application/x-shockwave-flash~swf,application/futuresplash~spl'
                                        ])])).encode('utf-8'))
    return md5.hexdigest()


def login():
    """
    Verifies that the user is logged in by checking for their email on the homepage.
    """
    print("Verifying login status...")
    if not all([COOKIE, CSRF_TOKEN, USER_ID]):
        raise ScriptError("Please set the FBTC_COOKIE, FBTC_CSRF_TOKEN, and FBTC_USER_ID environment variables.")

    try:
        with requests.Session() as s:
            r = s.get("https://freebitco.in/?op=home", headers=headers, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, 'lxml')
            email_element = soup.find(id="edit_profile_form_email")
            if email_element and email_element.get('value'):
                user_email = email_element.get('value')
                print(f"Successfully logged in as {user_email}")
                send_telegram_message(f"✅ Bot iniciado y logueado como {user_email}")
                return True
            else:
                print("Login failed. Please check your cookies and try again.")
                send_telegram_message("❌ ERROR: El login ha fallado. Revisa tus cookies.")
                return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during login verification: {e}")
        send_telegram_message(f"❌ ERROR: No se pudo conectar con Freebitco.in durante el login.\nError: {e}")
        return False


def claim_free_btc():
    """
    Claims the free BTC and returns True on success, False on failure.
    """
    print("Attempting to claim free BTC...")
    try:
        with requests.Session() as s:
            r = s.get("https://freebitco.in/?op=home", headers=headers, timeout=10)
            r.raise_for_status()
            if not r.text.find('free_play_form_button'):
                 print("Claim is not available yet. Waiting for the next cycle.")
                 return False

            soup = BeautifulSoup(r.content, 'lxml')
            client_seed = soup.find(id='next_client_seed')['value']

            data = {
                'csrf_token': CSRF_TOKEN,
                'op': 'free_play',
                'fingerprint': fingerprint(),
                'client_seed': client_seed,
                'fingerprint2': str(random.randint(1000000000,9999999999)),
                'pwc': '0',
            }
            roll = s.post('https://freebitco.in/', data=data, headers=headers, timeout=10)
            roll.raise_for_status()

            if roll.text.startswith('s'):
                print("Successfully claimed free BTC!")
                # Get updated balance to include in the notification
                balance_response = s.get('https://freebitco.in/?op=get_current_address_and_balance', headers=headers)
                new_balance = balance_response.text.split(':')[2]
                send_telegram_message(f"🎉 ¡Reclamación exitosa!\nNuevo saldo: {new_balance} BTC")
                return True
            else:
                print("Failed to claim free BTC. The button might not be ready.")
                return False

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while claiming BTC: {e}")
        send_telegram_message(f"⚠️ Alerta: Ocurrió un error de red al intentar reclamar.\nError: {e}")
        return False
    except (AttributeError, TypeError, KeyError):
        print("Could not find required elements. The website structure may have changed.")
        send_telegram_message("❌ ERROR: No se pudieron encontrar los elementos necesarios en la página. ¿Ha cambiado la web?")
        return False


if __name__ == "__main__":
    try:
        if login():
            while True:
                success = claim_free_btc()
                if success:
                    cooldown = random.randint(61 * 60, 67 * 60)
                    print(f"Claim successful. Waiting for a random interval.")
                else:
                    cooldown = 5 * 60
                    print(f"Claim failed or not available. Retrying in 5 minutes.")

                minutes = cooldown // 60
                seconds = cooldown % 60
                print(f"Next attempt in {minutes} minutes and {seconds} seconds.")
                time.sleep(cooldown)
    except ScriptError as e:
        print(f"Error: {e}")
        send_telegram_message(f"🛑 ERROR CRÍTICO: {e}")
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
        send_telegram_message("🔌 Bot detenido manualmente.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        send_telegram_message(f"🛑 ERROR INESPERADO: El bot se ha detenido.\nError: {e}")