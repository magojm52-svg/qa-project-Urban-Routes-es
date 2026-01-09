import data
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# Estas son las importaciones clave para conectar tus archivos:
from pages import UrbanRoutesPage
from helpers import retrieve_phone_code

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