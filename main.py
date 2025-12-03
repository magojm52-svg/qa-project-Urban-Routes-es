import data
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code
    raise Exception("No se pudo obtener el código después de 10 intentos")


class UrbanRoutesPage:

    # --- LOCALIZADORES ---
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    taxi_button = (By.XPATH, "//button[text()='Pedir un taxi']")
    comfort_tariff = (By.XPATH, "//div[contains(text(), 'Comfort')]")
    # Localizadores para número de teléfono
    phone_number_button = (By.XPATH, "//div[contains(text(), 'Número de teléfono')]")
    phone_input = (By.ID, "phone")
    next_button = (By.XPATH, "//button[contains(text(), 'Siguiente')]")
    code_input = (By.ID, "code")
    confirm_button = (By.XPATH, "//button[contains(text(), 'Confirmar')]")
    # Localizadores agregar tarjeta
    payment_method_button = (By.CLASS_NAME, "pp-text")
    add_card_button = (By.CLASS_NAME, "pp-plus-container")
    card_number_field = (By.ID, "number")  # Usado para invisibilidad del campo de tarjeta (Sub-modal)
    cvv_field = (By.XPATH, "//input[@id='code' and @placeholder='12']")
    add_button = (By.XPATH, "//button[text()='Agregar']")
    # Localizador para verificar si el modal de pago está presente
    payment_modal = (By.XPATH, "//div[contains(@class, 'payment-picker')]")
    # Localizador para la 'X' de cerrar el modal de método de pago (Modal principal)
    close_button_modal = (By.XPATH,"//div[contains(@class, 'payment-picker')]//button[contains(@class, 'close-button')]")
    # Localizador para mensaje del conductor
    message_field = (By.ID, "comment")
    # Localizadores para manta y pañuelos
    blanket_label = (By.XPATH, "//div[@class='r-sw-label' and text()='Manta y pañuelos']")
    # Para el contenedor del switch
    blanket_switch_container = (By.XPATH, "//div[@class='r-sw-container']")
    # Para el switch específico (elemento clickeable)
    blanket_switch = (By.XPATH,
                      "//div[text()='Manta y pañuelos']/following-sibling::div[@class='r-sw']//div[@class='switch']")
    # Alternativa más simple para hacer click
    blanket_option = (By.XPATH, "//div[text()='Manta y pañuelos']")
    # Localizadores para helados
    ice_cream_plus_button = (By.CLASS_NAME, "counter-plus")
    ice_cream_counter = (By.CLASS_NAME, "counter-value")
    # Localizador para el botón "Pedir un taxi"
    order_button = (By.CLASS_NAME, "smart-button")
    # Localizador para el modal de búsqueda
    search_modal_header = (By.CLASS_NAME, "order-header-title")
    # Localizador para información del conductor
    driver_info = (By.CLASS_NAME, "driver-info")  # Ajusta según el HTML real
    def __init__(self, driver):
        self.driver = driver


    # --- MÉTODOS DE RUTA ---
    def set_from(self, from_address):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.to_field)
        ).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.from_field)
        ).send_keys(address_from)

        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.to_field)
        ).send_keys(address_to)

    def click_taxi_button(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.taxi_button)
        ).click()

    # --- MÉTODOS DE TARIFA ---
    def select_comfort(self):
        # Esperar a que el elemento sea clickeable
        element = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(self.comfort_tariff)
        )
        # Hacer scroll al elemento para asegurar que esté visible
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        # Pequeña pausa para que termine el scroll
        time.sleep(0.5)
        element.click()

    # --- MÉTODOS DE AUTENTICACIÓN ---
    def click_phone_field(self):
        self.driver.find_element(*self.phone_number_button).click()

    def enter_phone_number(self, phone):
        self.driver.find_element(*self.phone_input).send_keys(phone)

    def click_next_button(self):
        self.driver.find_element(*self.next_button).click()

    def enter_code(self, code):
        self.driver.find_element(*self.code_input).send_keys(code)

    def click_confirm_button(self):
        self.driver.find_element(*self.confirm_button).click()

    def set_phone_number(self, phone, code):
        self.click_phone_field()
        self.enter_phone_number(phone)
        self.click_next_button()
        self.enter_code(code)
        self.click_confirm_button()

    # --- MÉTODOS DE PAGO/TARJETA ---
    def click_payment_method(self):
        wait = WebDriverWait(self.driver, 10)
        payment_button = wait.until(
            EC.element_to_be_clickable(self.payment_method_button)
        )
        payment_button.click()

    def click_add_card(self):
        wait = WebDriverWait(self.driver, 10)
        add_card_button = wait.until(
            EC.element_to_be_clickable(self.add_card_button)
        )
        add_card_button.click()

    def fill_card_data(self, card_number, card_code):
        # Usar Espera Explícita para el número de tarjeta
        card_number_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.card_number_field)
        )
        # PASO 3: Llenar número de tarjeta
        card_number_element.send_keys(card_number)

        # Usar Espera Explícita para el CVV
        cvv_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.cvv_field)
        )
        # PASO 3: Llenar CVV
        cvv_element.send_keys(card_code)

        # PASO 3/4: Forzar la pérdida de enfoque para activar el botón "Agregar"
        cvv_element.send_keys(Keys.TAB)

    def get_payment_method(self):
        return self.driver.find_element(*self.payment_method_button).text

    def click_link_card(self):
        # PASO 4: Clic en el botón "Agregar"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_button)
        ).click()

    def click_close_modal(self):
        wait = WebDriverWait(self.driver, 10)
        close_button = wait.until(
            EC.presence_of_element_located(self.close_button_modal)
        )
        print("✓ Botón X encontrado")
        self.driver.execute_script("arguments[0].click();", close_button)
        print("✓ Clic en X ejecutado")

    def is_payment_modal_closed(self):
        """Verifica si el modal de pago está cerrado (no visible)."""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.payment_modal)
            )
            return True
        except TimeoutException:
            return False  # El modal sigue visible después del timeout

    def set_message_for_driver(self, message):
        message_element = self.driver.find_element(*self.message_field)
        message_element.clear()  # Limpiar el campo antes de escribir
        message_element.send_keys(message)

    # Método para activar manta
    def set_blanket(self):
        # Usar el switch específico
        switch_element = self.driver.find_element(*self.blanket_switch)
        switch_element.click()
        print("✅ Manta activada")
        time.sleep(1)  # Esperar animación

    # Método para activar pañuelos
    def set_tissues(self):
        # Hacer scroll hacia arriba
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        # Scroll adicional para asegurar visibilidad
        self.driver.execute_script("window.scrollBy(0, -200);")
        time.sleep(2)

        try:
            element = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.blanket_switch)  # ¡Usar el MISMO localizador!
            )
            element.click()
            print("✅ Pañuelos activados exitosamente")
        except Exception as e:
            print(f"❌ Error al activar pañuelos: {e}")

    # Método para verificar si manta está seleccionada
    def is_blanket_selected(self):
        # Probar el contenedor del switch
        container = self.driver.find_element(*self.blanket_switch_container)
        slider = container.find_element(By.CSS_SELECTOR, ".slider")
        background_color = slider.value_of_css_property("background-color")
        print(f"Color del slider en container: {background_color}")

        return background_color == "rgba(0, 126, 255, 1)"

    # --- MÉTODOS DE HELADOS ---
    def scroll_to_ice_cream(self):
        """Hacer scroll para ver el contador de helados"""
        ice_cream_element = self.driver.find_element(*self.ice_cream_plus_button)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", ice_cream_element)
        time.sleep(0.5)  # Esperar que termine el scroll

    def add_ice_cream(self):
        """Hacer clic en el botón + para agregar helado"""
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.ice_cream_plus_button)
        ).click()

    def get_ice_cream_count(self):
        """Obtener el número actual de helados"""
        counter_element = self.driver.find_element(*self.ice_cream_counter)
        return int(counter_element.text)

    def set_ice_cream_quantity(self, quantity):
        """Establecer la cantidad específica de helados"""
        self.scroll_to_ice_cream()

        for i in range(quantity):
            self.add_ice_cream()
            time.sleep(0.5)  # Pequeña pausa entre clics

    # Método para hacer clic en "Pedir un taxi"
    def click_order_button(self):
        self.driver.find_element(*self.order_button).click()

    # Método para verificar que aparece el modal
    # Método para verificar que aparece el modal
    def wait_for_search_modal(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.search_modal_header)
        )

    def verify_search_modal_appears(self):
        modal_title = self.driver.find_element(*self.search_modal_header)
        assert modal_title.text == "Buscar automóvil"

    # Método para esperar información del conductor
    def wait_for_driver_info(self):
        WebDriverWait(self.driver, 40).until(
            expected_conditions.visibility_of_element_located(self.driver_info)
        )


class TestUrbanRoutes:
    driver = None
    routes_page = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)  # Añadir espera implícita para mayor robustez

        cls.routes_page = UrbanRoutesPage(cls.driver)
        # 1. Establecer ruta
        cls.routes_page.driver.get(data.urban_routes_url)
        cls.routes_page.set_route(data.address_from, data.address_to)
        cls.routes_page.click_taxi_button()
        cls.routes_page.select_comfort()

        # 2. Realizar autenticación (una sola vez en setup_class)
        cls.routes_page.click_phone_field()
        cls.routes_page.enter_phone_number(data.phone_number)
        cls.routes_page.click_next_button()
        code = retrieve_phone_code(cls.driver)
        cls.routes_page.enter_code(code)
        cls.routes_page.click_confirm_button()

        # 3. Esperar a que el modal de código desaparezca antes de continuar
        WebDriverWait(cls.driver, 10).until(
            EC.invisibility_of_element_located(cls.routes_page.code_input)
        )
        # Se asegura que la página de pago/opciones esté visible
        WebDriverWait(cls.driver, 10).until(
            EC.visibility_of_element_located(cls.routes_page.payment_method_button)
        )

    def test_set_route(self):
        # Esta prueba verifica la ruta establecida en setup_class
        address_from = data.address_from
        address_to = data.address_to
        assert self.routes_page.get_from() == address_from
        assert self.routes_page.get_to() == address_to

    def test_select_comfort_tariff(self):
        # Esta prueba verifica la tarifa seleccionada en setup_class
        comfort_tariff = self.driver.find_element(*self.routes_page.comfort_tariff)
        assert comfort_tariff.is_displayed()

    def test_set_phone_number(self):
        # Esta prueba verifica el resultado de la autenticación realizada en setup_class
        phone = data.phone_number
        phone_display = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "np-text"))
        )
        assert phone in phone_display.text

    def test_add_credit_card(self):
        # Usar los métodos que SÍ existen
        self.routes_page.click_payment_method()
        print("✓ Modal de pago abierto")

        self.routes_page.click_add_card()
        print("✓ Formulario de tarjeta abierto")

        self.routes_page.fill_card_data(data.card_number, data.card_code)
        print("✓ Datos de tarjeta llenados")

        self.routes_page.click_link_card()
        print("✓ Botón 'Agregar' clickeado")

        # Agregar una pequeña espera antes de cerrar
        time.sleep(2)

        self.routes_page.click_close_modal()
        print("✓ Botón cerrar clickeado")

        # Agregar otra espera para que el modal se cierre completamente
        time.sleep(2)

        # Verificar que el modal se cerró
        modal_closed = self.routes_page.is_payment_modal_closed()
        print(f"¿Modal cerrado? {modal_closed}")
        assert modal_closed

    def test_set_options(self):
        """5. Prueba para ingresar el mensaje al conductor y activar el interruptor."""
        message = data.message_for_driver

        # Ingresar mensaje
        self.routes_page.set_message_for_driver(message)

        # Verificación del mensaje
        actual_message = self.driver.find_element(*self.routes_page.message_field).get_property('value')
        assert actual_message == message

    # Y el test correspondiente:
    def test_set_message_for_driver(self):
        """Test para verificar que se puede escribir mensaje al conductor"""
        message = data.message_for_driver

        # Escribir mensaje
        self.routes_page.set_message_for_driver(message)

        # Verificar que el mensaje se escribió correctamente
        actual_message = self.driver.find_element(*self.routes_page.message_field).get_property('value')
        assert actual_message == message, f"Mensaje esperado: {message}, mensaje actual: {actual_message}"

    def test_set_blanket_and_tissues(self):
        """Test para verificar que se pueden activar manta y pañuelos"""

        # Activar manta y pañuelos (es la MISMA acción)
        self.routes_page.set_blanket()

        # Verificar que está seleccionada
        assert self.routes_page.is_blanket_selected(), "La manta y pañuelos no se activaron correctamente"

    def test_order_ice_cream(self):
        """Test para pedir 2 helados"""
        # Establecer 2 helados
        self.routes_page.set_ice_cream_quantity(2)

        # Verificar que el contador muestre 2
        ice_cream_count = self.routes_page.get_ice_cream_count()
        assert ice_cream_count == 2, f"Se esperaban 2 helados, pero se encontraron {ice_cream_count}"

    def test_request_taxi_modal(self):
        # Usar la instancia existente (ya configurada en setup_class)
        # Paso 8: Modal de búsqueda (los pasos 1-7 ya se completaron)
        self.routes_page.click_order_button()
        self.routes_page.wait_for_search_modal()
        self.routes_page.verify_search_modal_appears()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()