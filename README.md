# Freebitco.in Autofaucet

This script automates the process of claiming free satoshis from the [freebitco.in](https://freebitco.in/) website. It is a command-line tool designed to be run on a personal computer or a server to claim rewards automatically every hour.

**Important Note:** This is a command-line script, not a mobile application. Creating a mobile app is a significantly more complex task, and this script provides a more direct and achievable solution for automating the process.

## Features

-   Automatically claims free BTC every hour.
-   Calculates the remaining time until the next claim.
-   Uses a browser fingerprint to mimic a real user.
-   Securely stores your credentials using environment variables.

## Prerequisites

-   Python 3.6 or higher
-   The `requests`, `beautifulsoup4`, and `lxml` libraries

## Installation

1.  **Clone the repository or download the files.**

2.  **Install the required libraries:**
    ```bash
    pip install requests beautifulsoup4 lxml
    ```

## Configuration

To use this script, you need to provide your freebitco.in credentials as environment variables. This is a security best practice that avoids hardcoding your sensitive information in the script.

### Why not username and password?

This script uses a cookie-based authentication method instead of a direct login with a username and password. This is because a direct login would trigger a captcha, which is a security measure designed to block bots. Solving the captcha programmatically is a very complex task and is beyond the scope of this script. By using the cookies from an active login session, we can bypass the captcha and automate the claiming process.

The main drawback of this method is that the cookies will eventually expire, and you will need to repeat the process of obtaining them.

### How to get your credentials:

### 1. `FBTC_COOKIE`

Your account's cookie string. To get this:

1.  Log in to [freebitco.in](https://freebitco.in/) in your browser.
2.  Open the developer tools (usually by pressing `F12`).
3.  Go to the **Network** tab.
4.  Refresh the page.
5.  Click on any request in the list (e.g., the first one).
6.  In the **Headers** section, find the **Request Headers** and copy the entire value of the `Cookie` header.

### 2. `FBTC_CSRF_TOKEN`

Your account's Cross-Site Request Forgery (CSRF) token. To get this:

1.  Log in to [freebitco.in](https://freebitco.in/).
2.  Right-click on the page and select **View Page Source**.
3.  Search for `csrf_token` and copy its value.

### 3. `FBTC_USER_ID`

Your unique user ID. To get this:

1.  Log in to [freebitco.in](https://freebitco.in/).
2.  Right-click on the page and select **View Page Source**.
3.  Search for `user_id` and copy its value.

### Setting the Environment Variables

You can set these environment variables in your terminal before running the script.

**On Linux or macOS:**

```bash
export FBTC_COOKIE="your_cookie_string"
export FBTC_CSRF_TOKEN="your_csrf_token"
export FBTC_USER_ID="your_user_id"
```

**On Windows:**

```powershell
$env:FBTC_COOKIE="your_cookie_string"
$env:FBTC_CSRF_TOKEN="your_csrf_token"
$env:FBTC_USER_ID="your_user_id"
```

## Usage

Once you have installed the dependencies and configured your credentials, you can run the script with the following command:

```bash
python autofaucet.py
```

The script will then log in, claim your free BTC, and wait for the appropriate cooldown period before repeating the process.

## Disclaimer

This script is for educational purposes only. The use of bots or automated scripts may be against the terms of service of freebitco.in. Use this script at your own risk.