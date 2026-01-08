# 🚖 Urban Routes Automation Testing Framework

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

Autor: Antonio de Jesús Morales Vázquez
www.linkedin.com/in/antonio-de-jesús-morales-vázquez-1qa
