# Autofaucet para Freebitco.in

Este script automatiza el proceso de reclamar satoshis gratis del sitio web [freebitco.in](https://freebitco.in/). Es una herramienta de línea de comandos diseñada para ser ejecutada en un ordenador personal o en un servidor para reclamar recompensas automáticamente cada hora.

**Nota Importante:** Este es un script de línea de comandos, no una aplicación móvil. Crear una aplicación móvil es una tarea significativamente más compleja, y este script proporciona una solución más directa y factible para automatizar el proceso.

## Características

-   Reclama BTC gratis automáticamente cada hora.
-   Calcula el tiempo restante hasta la próxima reclamación.
-   Utiliza una huella digital de navegador (fingerprint) para simular ser un usuario real.
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

Para usar este script, necesitas proporcionar tus credenciales de freebitco.in como variables de entorno. Esta es una buena práctica de seguridad que evita escribir tu información sensible directamente en el script.

### ¿Por qué no usar usuario y contraseña?

Este script utiliza un método de autenticación basado en cookies en lugar de un inicio de sesión directo con usuario y contraseña. La razón es que un inicio de sesión directo activaría un captcha, que es una medida de seguridad diseñada para bloquear bots. Resolver el captcha de forma programada es una tarea muy compleja y está fuera del alcance de este script. Al usar las cookies de una sesión de inicio de sesión activa, podemos evitar el captcha y automatizar el proceso de reclamación.

La principal desventaja de este método es que las cookies eventualmente expirarán, y necesitarás repetir el proceso para obtenerlas de nuevo.

### Cómo obtener tus credenciales:

#### 1. `FBTC_COOKIE`

Es el texto que contiene las cookies de tu cuenta. Para obtenerlo:

1.  Inicia sesión en [freebitco.in](https://freebitco.in/) en tu navegador.
2.  Abre las herramientas de desarrollador (normalmente con la tecla `F12`).
3.  Ve a la pestaña **Network** (o **Red**).
4.  Refresca la página.
5.  Haz clic en cualquier solicitud de la lista (por ejemplo, la primera).
6.  En la sección de **Headers** (o **Encabezados**), busca los **Request Headers** (o **Encabezados de la solicitud**) y copia el valor completo del campo `Cookie`.

#### 2. `FBTC_CSRF_TOKEN`

Es tu token de seguridad CSRF. Para obtenerlo:

1.  Inicia sesión en [freebitco.in](https://freebitco.in/).
2.  Haz clic derecho en la página y selecciona **Ver código fuente de la página**.
3.  Busca `csrf_token` y copia su valor.

#### 3. `FBTC_USER_ID`

Es tu ID de usuario único. Para obtenerlo:

1.  Inicia sesión en [freebitco.in](https://freebitco.in/).
2.  Haz clic derecho en la página y selecciona **Ver código fuente de la página**.
3.  Busca `user_id` y copia su valor.

### Cómo configurar las Variables de Entorno

Puedes configurar estas variables en tu terminal antes de ejecutar el script.

**En Linux o macOS:**

```bash
export FBTC_COOKIE="tu_cadena_de_cookie"
export FBTC_CSRF_TOKEN="tu_token_csrf"
export FBTC_USER_ID="tu_id_de_usuario"
```

**En Windows:**

```powershell
$env:FBTC_COOKIE="tu_cadena_de_cookie"
$env:FBTC_CSRF_TOKEN="tu_token_csrf"
$env:FBTC_USER_ID="tu_id_de_usuario"
```

## Uso

Una vez que hayas instalado las dependencias y configurado tus credenciales, puedes ejecutar el script con el siguiente comando:

```bash
python autofaucet.py
```

El script iniciará sesión, reclamará tus BTC gratis y esperará el período de enfriamiento adecuado antes de repetir el proceso.

## Descargo de Responsabilidad

Este script es solo para fines educativos. El uso de bots o scripts automatizados puede estar en contra de los términos de servicio de freebitco.in. Usa este script bajo tu propio riesgo.