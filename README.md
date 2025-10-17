# Autofaucet para Freebitco.in con Notificaciones de Telegram

Este script automatiza el proceso de reclamar satoshis gratis del sitio web [freebitco.in](https://freebitco.in/) y te notifica sobre su estado a través de un bot de Telegram. Es una herramienta de línea de comandos diseñada para ser ejecutada 24/7 en un servidor o en un ordenador de bajo consumo.

**Nota Importante:** Este es un script de línea de comandos, no una aplicación móvil. Integrarlo con Telegram te da la ventaja de recibir notificaciones en tu móvil, que es la solución más práctica y eficiente para monitorear el proceso.

## Características

-   Reclama BTC gratis automáticamente.
-   Espera un **intervalo de tiempo aleatorio** (entre 61 y 67 minutos) para simular un comportamiento humano y evitar ser detectado.
-   **Te notifica por Telegram** cuando:
    -   El bot se inicia correctamente.
    -   La reclamación de BTC es exitosa (incluyendo tu nuevo saldo).
    -   Ocurre un error o fallo.
-   Almacena tus credenciales de forma segura usando variables de entorno.

## Prerrequisitos

-   Python 3.6 o superior.
-   Las librerías `requests`, `beautifulsoup4` y `lxml`.

## Instalación

1.  **Clona el repositorio o descarga los archivos.**

2.  **Instala las librerías requeridas:**
    ```bash
    pip install requests beautifulsoup4 lxml
    ```

## Configuración

Para usar este script, necesitas proporcionar tus credenciales como variables de entorno.

### Parte 1: Credenciales de Freebitco.in

#### ¿Por qué no usar usuario y contraseña?

Este script utiliza un método de autenticación basado en cookies porque un inicio de sesión directo activaría un captcha (un test para diferenciar humanos de bots), que es muy difícil de automatizar. Usando las cookies de una sesión activa, evitamos este problema. La única desventaja es que las cookies expiran con el tiempo y tendrás que obtenerlas de nuevo.

#### Cómo obtener las credenciales de Freebitco.in:

1.  **`FBTC_COOKIE`**:
    -   Inicia sesión en [freebitco.in](https://freebitco.in/) en tu navegador.
    -   Abre las herramientas de desarrollador (`F12`), ve a la pestaña **Network** (o **Red**), y refresca la página.
    -   Haz clic en cualquier solicitud, ve a la sección de **Request Headers** (o **Encabezados de la solicitud**) y copia el valor completo del campo `Cookie`.

2.  **`FBTC_CSRF_TOKEN`**:
    -   En la página de [freebitco.in](https://freebitco.in/), haz clic derecho y selecciona **Ver código fuente de la página**.
    -   Busca (`Ctrl+F`) `csrf_token` y copia su valor.

3.  **`FBTC_USER_ID`**:
    -   En el código fuente de la página, busca `user_id` y copia su valor.

### Parte 2: Credenciales del Bot de Telegram

#### Cómo crear tu bot y obtener las credenciales:

1.  **`TELEGRAM_BOT_TOKEN`**:
    -   Abre Telegram y busca a un bot llamado **`@BotFather`** (es el bot oficial de Telegram para crear otros bots).
    -   Inicia una conversación con él y envíale el comando `/newbot`.
    -   Sigue sus instrucciones: te pedirá un nombre para tu bot y luego un "username" (que debe terminar en `bot`).
    -   Al final, te dará un **token de acceso HTTP API**. Cópialo. Ese es tu `TELEGRAM_BOT_TOKEN`.

2.  **`TELEGRAM_CHAT_ID`**:
    -   Busca a otro bot en Telegram llamado **`@userinfobot`**.
    -   Inicia una conversación con él y te enviará un mensaje con tu información.
    -   Copia el número que aparece junto a **`Id:`**. Ese es tu `TELEGRAM_CHAT_ID`.
    -   Ahora, busca el bot que creaste en el paso anterior e inicia una conversación con él (envíale cualquier mensaje). Esto es necesario para que tu bot pueda enviarte mensajes.

### Parte 3: Configurar las Variables de Entorno

**En Linux o macOS:**
```bash
export FBTC_COOKIE="tu_cadena_de_cookie"
export FBTC_CSRF_TOKEN="tu_token_csrf"
export FBTC_USER_ID="tu_id_de_usuario"
export TELEGRAM_BOT_TOKEN="tu_token_de_telegram"
export TELEGRAM_CHAT_ID="tu_id_de_chat_de_telegram"
```

**En Windows:**
```powershell
$env:FBTC_COOKIE="tu_cadena_de_cookie"
$env:FBTC_CSRF_TOKEN="tu_token_csrf"
$env:FBTC_USER_ID="tu_id_de_usuario"
$env:TELEGRAM_BOT_TOKEN="tu_token_de_telegram"
$env:TELEGRAM_CHAT_ID="tu_id_de_chat_de_telegram"
```

## Uso

Una vez configurado todo, ejecuta el script:
```bash
python autofaucet.py
```
El script se ejecutará en un bucle infinito, reclamando y notificándote. Para que corra 24/7, te recomiendo usarlo en un servidor (VPS) o una Raspberry Pi.

## Descargo de Responsabilidad

Este script es solo para fines educativos. El uso de bots puede estar en contra de los términos de servicio de freebitco.in. Úsalo bajo tu propio riesgo.