from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
edge_options = webdriver.EdgeOptions()
edge_options.binary_location = edge_path
edge_driver_path = r"C:\Users\User\Downloads\edgedriver_win64\msedgedriver.exe"
driver = webdriver.Edge(
    service=Service(edge_driver_path),
    options=edge_options
)

capture_folder = r"C:\Users\User\Desktop\AutoNav-Selenium\Pruebas"
if not os.path.exists(capture_folder):
    os.makedirs(capture_folder)

test_results = []

def generate_report():
    report_path = os.path.join(capture_folder, "test_report.html")
    with open(report_path, "w") as f:
        f.write("<html><head><title>Test Report</title></head><body>")
        f.write("<h1>Reporte de Pruebas</h1>")
        f.write("<table border='1' style='border-collapse: collapse; width: 100%;'>")
        f.write("<tr><th>Nombre de la Prueba</th><th>Estado</th><th>Tiempo (s)</th></tr>")
        for result in test_results:
            f.write(f"<tr><td>{result['name']}</td><td>{result['status']}</td><td>{result['time']}</td></tr>")
        f.write("</table></body></html>")
    print(f"Reporte generado en: {report_path}")

def execute_test(test_name, test_function):
    start_time = time.time()
    try:
        test_function()
        status = "PASSED"
    except Exception as e:
        print(f"Error en {test_name}: {e}")
        status = "FAILED"
    finally:
        elapsed_time = round(time.time() - start_time, 2)
        test_results.append({"name": test_name, "status": status, "time": elapsed_time})

def login_test(username, password, expected_result):
    driver.get("https://sigeiacademico.itla.edu.do/account/login")

    username_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    username_field.clear()
    username_field.send_keys(username)
    password_field.clear()
    password_field.send_keys(password)
    login_button = driver.find_element(By.ID, "btnLogin")
    login_button.click()

    wait = WebDriverWait(driver, 15)

    if expected_result == "failure":
        try:
            wait.until(EC.presence_of_element_located((By.ID, "kt_body")))
            raise AssertionError("Accedió al Dashboard con credenciales incorrectas")
        except Exception:
            print("Acceso denegado como se esperaba: Test PASSED")
    elif expected_result == "success":
        try:
            wait.until(EC.presence_of_element_located((By.ID, "kt_body")))
            print("Acceso exitoso como se esperaba: Test PASSED")
        except Exception as e:
            print("Error: No se accedió a SIGEI. Revisar credenciales o tiempo de espera.")
            raise AssertionError("No se accedió a SIGEI con credenciales correctas") from e

def test_click_on_perfil():
    div_button = driver.find_element(By.CSS_SELECTOR, ".content-button .button.color-sass")
    ActionChains(driver).move_to_element(div_button).click().perform()
    time.sleep(7)

def test_click_on_config():
    config_button = driver.find_element(By.ID, "dropdownConfigButton")
    ActionChains(driver).move_to_element(config_button).click().perform()
    time.sleep(7)
def test_click_on_lobby():
    lobby_button = driver.find_element(By.XPATH, "//h6[text()='Volver al Lobby']")
    ActionChains(driver).move_to_element(lobby_button).click().perform()
    time.sleep(5)

def test_click_on_transporte():
    salir_button = driver.find_element(By.CSS_SELECTOR, "div.button.color-vuejs")
    ActionChains(driver).move_to_element(salir_button).click().perform()
    time.sleep(5)

try:
    print("Caso 1: Login fallido")
    execute_test("Login Fallido", lambda: login_test("email_failed", "pass_failed", "failure"))
    time.sleep(7)
    driver.save_screenshot(os.path.join(capture_folder, "login_failed_outside.png"))

    print("Caso 2: Login exitoso")
    execute_test("Login Exitoso", lambda: login_test("ruizsanchezyael@gmail.com", "25102004YtAz", "success"))
    time.sleep(7)
    driver.save_screenshot(os.path.join(capture_folder, "login_success_outside.png"))

    print("Caso 3: Click en Perfil")
    execute_test("Clic en Perfil", test_click_on_perfil)
    time.sleep(5)
    driver.save_screenshot(os.path.join(capture_folder, "perfil_clicked.png"))

    print("Caso 4: Click en Config")
    execute_test("Clic en Configuración", test_click_on_config)
    time.sleep(5)
    driver.save_screenshot(os.path.join(capture_folder, "config_clicked.png"))

    print("Caso 5: Click en Volver al Lobby")
    execute_test("Clic en Volver al Lobby", test_click_on_lobby)
    time.sleep(5)
    driver.save_screenshot(os.path.join(capture_folder, "lobby_clicked.png"))

    print("Caso 6: Click en Transporte")
    execute_test("Clic en Transporte", test_click_on_transporte)
    time.sleep(5)
    driver.save_screenshot(os.path.join(capture_folder, "transporte_clicked.png"))

finally:
    generate_report()
    driver.quit()