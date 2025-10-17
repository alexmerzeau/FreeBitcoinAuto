import requests
import time
import hashlib
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote
import os

# --- Constants and Configuration ---
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

# --- User-specific credentials ---
# To use this script, you need to provide your freebitco.in credentials.
# It is recommended to use environment variables for security.
#
# 1. FBTC_COOKIE: Your account's cookie string.
#    - To get this, log in to freebitco.in in your browser,
#      open the developer tools (F12), go to the "Network" tab,
#      refresh the page, click on any request, and find the "Cookie"
#      header in the request headers.
#
# 2. FBTC_CSRF_TOKEN: Your account's CSRF token.
#    - This can be found in the HTML of the homepage after logging in.
#      Search for "csrf_token".
#
# 3. FBTC_USER_ID: Your user ID.
#    - This can be found in the HTML of the homepage after logging in.
#      Search for "user_id".

COOKIE = os.environ.get('FBTC_COOKIE', '')
CSRF_TOKEN = os.environ.get('FBTC_CSRF_TOKEN', '')
USER_ID = os.environ.get('FBTC_USER_ID', '')


# --- Global Variables ---
headers = {
    'User-Agent': USER_AGENT,
    'Cookie': COOKIE,
    'accept': ACCEPT
}

class ScriptError(Exception):
    """Custom exception for script-related errors."""
    pass

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
            r.raise_for_status()  # Raise an exception for bad status codes
            soup = BeautifulSoup(r.content, 'lxml')
            email_element = soup.find(id="edit_profile_form_email")
            if email_element and email_element.get('value'):
                print(f"Successfully logged in as {email_element.get('value')}")
                return True
            else:
                print("Login failed. Please check your cookies and try again.")
                return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during login verification: {e}")
        return False


def claim_free_btc():
    """
    Claims the free BTC from the website and returns the cooldown period.
    """
    print("Attempting to claim free BTC...")
    try:
        with requests.Session() as s:
            # Get the client seed from the homepage
            r = s.get("https://freebitco.in/?op=home", headers=headers, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, 'lxml')
            client_seed = soup.find(id='next_client_seed')['value']

            # Make the claim request
            data = {
                'csrf_token': CSRF_TOKEN,
                'op': 'free_play',
                'fingerprint': fingerprint(),
                'client_seed': client_seed,
                'fingerprint2': '4036898993',  # This can be a random number
                'pwc': '0',
            }
            roll = s.post('https://freebitco.in/', data=data, headers=headers, timeout=10)
            roll.raise_for_status()

            if roll.text.startswith('s'):
                print("Successfully claimed free BTC!")
            else:
                print("Failed to claim free BTC.")

            # Calculate and return the cooldown period
            try:
                # The response is in the format "s:xxxxxx:xxxxxx", where the second number is the remaining time
                parts = roll.text.split(':')
                if len(parts) > 1 and parts[1].isdigit():
                    remaining_time = int(parts[1]) + 5  # Add a 5-second buffer
                    print(f"Next claim available in {remaining_time // 60} minutes and {remaining_time % 60} seconds.")
                    return remaining_time
                else:
                    raise ValueError("Invalid response format for cooldown.")
            except (IndexError, ValueError) as e:
                print(f"Could not determine the cooldown period: {e}. Defaulting to 1 hour and 5 minutes.")
                return 3900  # 1 hour and 5 minutes in seconds

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while claiming BTC: {e}")
        return 3900
    except (AttributeError, TypeError, KeyError):
        print("Could not find the client seed or other required elements. The website structure may have changed.")
        return 3900


if __name__ == "__main__":
    try:
        if login():
            while True:
                cooldown = claim_free_btc()
                print(f"Waiting for {cooldown} seconds before the next claim...")
                time.sleep(cooldown)
    except ScriptError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")