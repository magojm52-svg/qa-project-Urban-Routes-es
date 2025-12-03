# Proyecto de Automatización de Pruebas - Urban Routes

## Descripción del Proyecto
Este proyecto contiene pruebas automatizadas para la aplicación Urban Routes, una plataforma de solicitud de taxis. Las pruebas cubren el flujo completo de solicitud de un taxi, desde la configuración de direcciones hasta la confirmación del viaje.

## Tecnologías y Técnicas Utilizadas
- **Python**: Lenguaje de programación principal
- **Selenium WebDriver**: Para la automatización de navegadores web
- **pytest**: Framework de testing
- **Localizadores web**: Para identificar elementos en la página
- **Patrón Page Object Model**: Para organizar el código de las pruebas

## Funcionalidades Probadas
Las pruebas automatizadas cubren los siguientes escenarios:
- Configuración de direcciones de origen y destino
- Selección de tarifa Comfort
- Ingreso de número de teléfono
- Agregado de tarjeta de crédito
- Envío de mensaje al conductor
- Solicitud de manta y pañuelos
- Solicitud de helados
- Verificación del modal de búsqueda de taxi

## Instrucciones para Ejecutar las Pruebas

### Prerrequisitos
- Python 3.x instalado
- Navegador web (Chrome recomendado)
- Conexión a internet

### Pasos para ejecutar
1. Clona el repositorio en tu máquina local
2. Instala las dependencias necesarias
3. Actualiza la URL del servidor en el archivo `data.py`
4. Ejecuta las pruebas con el comando: `pytest main.py`

## Estructura del Proyecto
- `main.py`: Contiene las pruebas automatizadas y la clase UrbanRoutesPage
- `data.py`: Almacena los datos de configuración y URLs
- `README.md`: Documentación del proyecto

## Autor
Antonio de Jesús Morales Vázquez

## Notas Adicionales
- Las pruebas están diseñadas para ejecutarse en un entorno de testing específico
- Asegúrate de tener la URL correcta del servidor antes de ejecutar las pruebas

