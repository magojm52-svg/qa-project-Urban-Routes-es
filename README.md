<img width="1366" height="768" alt="resultado_test" src="https://github.com/user-attachments/assets/4863063b-2ba1-43b3-b9e9-fe354e0653ee" />﻿# 🚖 Urban Routes Automation Testing Framework
![Uploading resultado_test.png…]()

![QA Automation](https://img.shields.io/badge/Role-QA_Automation_Engineer-blue)
![Python](https://img.shields.io/badge/Python-3.x-green)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-orange)

## 📝 Descripción del Proyecto
Este proyecto desarrolla un framework de pruebas automatizadas de extremo a extremo (E2E) para la plataforma **Urban Routes**. La suite de pruebas valida el flujo crítico de negocio: desde la entrada de direcciones hasta la asignación de un conductor, asegurando la integridad de las integraciones de pago y servicios adicionales.

## 🛠️ Tecnologías y Arquitectura
* **Lenguaje:** Python
* **Automatización:** Selenium WebDriver
* **Framework de Pruebas:** Pytest
* **Patrón de Diseño:** **Page Object Model (POM)**
    * *Beneficio:* Separación de la lógica de negocio de los selectores, facilitando el mantenimiento y la escalabilidad del código.

## 🧪 Escenarios de Prueba (Coverage)
El proyecto automatiza con éxito las siguientes acciones:
1.  **Configuración de Ruta:** Direcciones de origen y destino.
2.  **Lógica de Tarifas:** Selección del modo 'Comfort'.
3.  **Registro de Usuario:** Ingreso de teléfono y validación dinámica vía SMS (intercepción de logs).
4.  **Gestión de Pagos:** Registro de tarjeta de crédito (manejo de pérdida de foco en CVV).
5.  **Requerimientos Especiales:** Escritura de mensajes al conductor y selección de artículos (mantas y helados).
6.  **Validación de UI:** Verificación de modales de búsqueda y asignación de conductor.

## 📂 Estructura del Proyecto
```text
├── main.py          # Clase TestUrbanRoutes (Scripts de prueba)
├── pages.py         # Clase UrbanRoutesPage (Lógica y localizadores)
├── data.py          # Diccionario de datos de prueba y configuración
└── README.md        # Documentación del framework

🚀 Instalación y Ejecución
Prerrequisitos
• Python 3.x
• Google Chrome & ChromeDriver



Pasos
1. Clonar el repositorio:
Bash
git clone [https://github.com/tu-usuario/urban-routes-automation.git](https://github.com/tu-usuario/urban-routes-automation.git)
cd urban-routes-automation
2. Instalar dependencias:
Bash
pip install selenium pytest
3. Configuración: Actualiza la URL del servidor en el archivo data.py con el entorno activo.
4. Ejecutar pruebas:
Bash
pytest main.py


📊 Resultados de Ejecución
Las pruebas se ejecutaron utilizando Pytest, validando la estabilidad y velocidad del framework.
Resumen de la Suite:
• Tests Totales: 9 escenarios de extremo a extremo (E2E).
• Estado: 100% Pass (Éxito).
• Tiempo de Ejecución: 15.99 segundos (Optimizado con esperas explícitas).
Log de Consola:
Plaintext
main.py::TestUrbanRoutes::test_set_route PASSED
main.py::TestUrbanRoutes::test_select_comfort_tariff PASSED
main.py::TestUrbanRoutes::test_set_phone_number PASSED
main.py::TestUrbanRoutes::test_add_credit_card PASSED
main.py::TestUrbanRoutes::test_set_options PASSED
main.py::TestUrbanRoutes::test_set_message_for_driver PASSED
main.py::TestUrbanRoutes::test_set_blanket_and_tissues PASSED
main.py::TestUrbanRoutes::test_order_ice_cream PASSED
main.py::TestUrbanRoutes::test_request_taxi_modal PASSED

================ 9 passed in 15.99s ================
Evidencias Técnicas Observadas:
• Intercepción de Red: Se recuperó con éxito el código de confirmación SMS desde los logs de rendimiento del navegador mediante la herramienta helpers.py.
• Manejo de UI Dinámica: Se validó el cierre de modales de pago y la activación de elementos tipo switch con validación de propiedades CSS (background-color).
• Estabilidad Asíncrona: El modal de búsqueda de automóvil se gestionó mediante esperas inteligentes, evitando falsos negativos por carga lenta.

<img width="1366" height="768" alt="resultado_test" src="https://github.com/user-attachments/assets/f83ec828-0cf9-45d2-83a8-01c7e55f129f" />



Autor: Antonio de Jesús Morales Vázquez
www.linkedin.com/in/antonio-de-jesús-morales-vázquez-1qa
