# Sistema Web de Consulta y Análisis de Datos Abiertos de Colombia

## 1. Descripción del proyecto

Aplicación web desarrollada en Python y Flask que permite consultar datos abiertos de casos positivos de COVID-19 en Colombia mediante una API REST, procesarlos en formato JSON, almacenarlos en SQL Server y consultarlos desde el navegador.

## 2. Objetivo general

Desarrollar una aplicación web utilizando Python, Flask, SQL Server y el patrón MVC para consultar, almacenar y analizar información pública de COVID-19 en Colombia.

## 3. Fuente de información

- Conjunto de datos: Casos positivos de COVID-19 en Colombia.
- Portal: https://www.datos.gov.co/
- Identificador del recurso: gt2j-8ykr.
- Endpoint: https://www.datos.gov.co/resource/gt2j-8ykr.json
- Formato de respuesta: JSON.
- Consulta: hasta 100 registros por sincronización.

## 4. Tecnologías utilizadas

- Python 3.10 o superior.
- Flask.
- Requests.
- SQL Server y SSMS.
- pyodbc.
- Microsoft ODBC Driver 18 for SQL Server.
- HTML5 y CSS3.
- python-dotenv.

## 5. Arquitectura MVC

**Modelo:** `models/datos_models.py` realiza las conexiones, inserciones y consultas a SQL Server.

**Vista:** `templates/index.html` presenta los datos y `static/estilos.css` define el diseño.

**Controlador:** `app.py` administra las solicitudes del navegador y coordina las operaciones.

**Cliente API:** `api/api__client.py` consulta los datos externos.

## 6. Funcionamiento

1. El usuario abre la aplicación.
2. Puede sincronizar registros desde la API.
3. Python recibe y procesa los datos JSON.
4. El modelo almacena los registros en SQL Server.
5. Se evita insertar identificadores duplicados.
6. El usuario consulta los registros mediante la página web.
7. Puede buscar por identificador, departamento o municipio.
8. La aplicación muestra indicadores estadísticos básicos.

## 7. Campos utilizados

| Campo | Descripción |
|---|---|
| id_de_caso | Identificador único del caso |
| fecha_reporte_web | Fecha del reporte |
| fecha_de_notificaci_n | Fecha de notificación |
| departamento_nom | Departamento |
| ciudad_municipio_nom | Municipio |
| edad | Edad del paciente |
| sexo | Sexo registrado |
| estado | Estado clínico |
| recuperado | Estado de recuperación |

## 8. Instalación

1. Instalar Python, SQL Server, SSMS y el controlador ODBC correspondiente.
2. Descargar el repositorio.
3. Abrir la carpeta en Visual Studio Code.
4. Crear y activar el entorno virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

5. Instalar las dependencias:

```powershell
python -m pip install -r requirements.txt
```

6. Copiar `.env.example` a un archivo llamado `.env` y configurar SQL Server.
7. Ejecutar `database/crear_base_datos.sql` en SSMS.
8. Iniciar la aplicación:

```powershell
python app.py
```

9. Abrir http://127.0.0.1:5000

## 9. Pruebas

Prueba de la API:

```powershell
python probar_api.py
```

Prueba de SQL Server:

```powershell
python probar_conexion.py
```

Pruebas automatizadas:

```powershell
python -m unittest discover -s tests -v
```

Para comprobar el funcionamiento completo se debe sincronizar, consultar registros, utilizar el filtro y repetir la sincronización para verificar que no se dupliquen identificadores.

## 10. Integrantes y aportes

## Integrantes y aportes al proyecto

### Integrante 1: Jose Miguel Rodriguez Escobar

**Responsabilidades: Consumo de API y procesamiento de datos.**

- Selección del conjunto de datos abiertos de COVID-19 en Colombia.
- Implementación del consumo de la API REST mediante Python y Requests.
- Configuración del endpoint de datos.gov.co.
- Procesamiento y validación de los datos recibidos en formato JSON.
- Desarrollo del módulo `api/api__client.py`.
- Implementación del proceso de sincronización mediante `sincronizar.py`.

### Integrante 2: Kelvin Jose Garcia Peñaloza

**Responsabilidades: Base de datos SQL Server y persistencia.**

- Creación y configuración de la base de datos `DatosAbiertosColombia`.
- Desarrollo del script SQL para crear la tabla `CasosCovid`.
- Implementación de la conexión entre Python y SQL Server mediante pyodbc.
- Desarrollo del módulo `models/datos_models.py`.
- Implementación del almacenamiento de registros y prevención de duplicados.
- Desarrollo de las consultas SQL para búsqueda y obtención de estadísticas.

### Aportes realizados en conjunto

- Integración de los módulos mediante el patrón MVC.
- Desarrollo del controlador Flask (`app.py`).
- Creación de la interfaz web con HTML y CSS.
- Implementación de formularios de búsqueda y sincronización.
- Realización de pruebas de funcionamiento.
- Elaboración de la documentación del proyecto en `README.md`.
- Organización del código fuente para su entrega en GitHub.

## 11. Evidencias

Las capturas del funcionamiento del sistema se encuentran en la carpeta `evidencias/`, incluyendo respuesta JSON, registros en SQL Server, interfaz web, sincronización y búsqueda filtrada.

## 12. Alcance

El proyecto implementa consulta de API, almacenamiento, sincronización, búsqueda y visualización de datos. No incluye CRUD completo, autenticación de usuarios ni despliegue público.

## 13. Seguridad

El archivo `.env` contiene configuración local y no debe publicarse. El repositorio incluye `.env.example` como plantilla sin contraseñas reales.
