
![STREAMCHECK 1 1](https://github.com/user-attachments/assets/a41d9b5a-e94a-4b09-b80d-c3ba651a76dd)

NOTAS DE VERSION 1.1

SE ELIMINARON LOS CHECKERS DE HBO Y PRIME
SE AGREGARON CHECKERS DE INSTAGRAM, KOGAMA Y IPVANISH
SE ARREGLO EL BUG LOGIN DE DISNEY PLUS
SE AGREGO UNA FUNCION DE CAPTURAS DE PANTALLAS PARA CUENTAS VALIDAS

CHECKER BY NOCTAMBULO
Este script checkea cuentas de 

°NETFLIX
°HBO
°PRIME 
°DISNEY PLUS

Antes de iniciar el script, instala el requirements.txt

pip install -r requirements.txt

para comenzar a usarlo, vamos a los txt de la carpeta "cuentas"

EL CHECKER LEE LAS LINEAS DEL TXT EN EL SIGUIENTE FORMATO
--------------------------
USUARIO:CONTRASEÑA 

![image](https://github.com/user-attachments/assets/3fd3412a-826b-46ce-ad41-b4a5fbbec3b7)

--------------------------

dejar siempre los : sin separar nada, si se separa no funcionara

| las carpetas tienen que tener el siguiente formato para que el script pueda leerlas

![image](https://github.com/user-attachments/assets/8e45af5e-89d3-482c-ac47-f5d150e0af2d)

-----------------------------------------------------------------------
Guía para actualizar ChromeDriver en StreamCheck

Este documento explica cómo actualizar ChromeDriver en el script de StreamCheck para evitar problemas de compatibilidad con nuevas versiones de Google Chrome.

1. Revisar la Versión de Chrome

Antes de actualizar ChromeDriver, verifica qué versión de Google Chrome está instalada en tu sistema.

En Windows, abre una terminal (cmd) y ejecuta:

chrome --version

En Linux/Mac, usa:

google-chrome --version

Anota el número de versión (ejemplo: 124.0.6350.0).

2. Descargar la Versión Correcta de ChromeDriver

Si ChromeDriver deja de funcionar, descarga manualmente la versión compatible desde:

🔗 https://sites.google.com/chromium.org/driver/

Busca la versión que coincida con la de Google Chrome.

Descarga el archivo correspondiente a tu sistema operativo.

Extrae el ejecutable chromedriver.exe (Windows) o chromedriver (Linux/Mac).

Guarda el archivo en la misma carpeta que el script o en un directorio accesible.

3. Cambios en el Código

Si usas una versión específica de ChromeDriver, debes modificar esta línea en tu código:

Código Actual:

from webdriver_manager.chrome import ChromeDriverManager
...
service = Service(ChromeDriverManager().install())

Código Modificado (usando un ChromeDriver específico):

service = Service("ruta/al/chromedriver")

Ejemplo en Windows:

service = Service("C:/Users/TuUsuario/Descargas/chromedriver.exe")

Ejemplo en Linux/Mac:

service = Service("/usr/local/bin/chromedriver")

4. Actualización Automática con WebDriver Manager

Si prefieres actualizar ChromeDriver automáticamente, mantén la línea actual:

service = Service(ChromeDriverManager().install())

Pero asegúrate de tener instalada la versión correcta de webdriver_manager ejecutando:

pip install -U webdriver-manager

5. Prueba y Verificación

Después de actualizar, ejecuta el script nuevamente para verificar que ChromeDriver funciona correctamente.

Si encuentras errores, revisa:

Que la versión de Chrome y ChromeDriver coincidan.

Que la ruta del chromedriver sea correcta si lo descargaste manualmente.

Que webdriver_manager esté actualizado.

6. Solución de Problemas

Error: selenium.common.exceptions.SessionNotCreatedException

Esto indica que ChromeDriver no es compatible con tu versión de Chrome. Descarga la versión correcta.

Error: Permission Denied

En Linux/Mac, da permisos de ejecución con:

chmod +x /ruta/al/chromedriver

Error: ModuleNotFoundError: No module named 'selenium'

Instala Selenium con:

pip install selenium



Si el chromedriver te llegase a dar problemas, verifica la version de tu chrome y actualiza el chromedrive.
intenta mantenerlo siempre dentro de la carpeta raiz del checker.

--------------------
Si hay problemas, contactame: https://t.me/NoctaPaste
--------------------

actualmente esta en prueba, asi que en el futuro mejorare la velocidad y agregare mas...
