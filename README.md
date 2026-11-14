# Proyecto de Datos Abiertos: COVID-19 en Colombia

## 1. Descripción del proyecto

Este proyecto permite consultar datos abiertos relacionados con los casos de COVID-19 en Colombia mediante una API pública. La información obtenida se procesa y almacena en una base de datos SQL Server.

La aplicación está desarrollada en Python utilizando Flask y una arquitectura organizada por componentes.

## 2. Objetivo general

Desarrollar una aplicación que permita consultar, procesar y almacenar información pública sobre los casos de COVID-19 en Colombia, utilizando una API y una base de datos relacional.

## 3. Tecnologías utilizadas

- Python
- Flask
- SQL Server
- API de datos.gov.co
- HTML
- CSS
- Requests
- PyODBC

## 4. Funcionamiento del proyecto

1. El usuario ingresa a la aplicación web.
2. La aplicación permite solicitar información a la API de datos abiertos.
3. El sistema recibe los registros de COVID-19.
4. Los datos son procesados por el modelo.
5. La información se almacena en SQL Server.
6. Se controlan los registros duplicados para evitar almacenar la misma información varias veces.

## 5. Estructura del proyecto

- api/: contiene el cliente encargado de consultar la API.
- models/: contiene las funciones para procesar y guardar los datos.
- database/: contiene los scripts para crear y configurar la base de datos.
- templates/: contiene las páginas HTML.
- static/: contiene los estilos CSS.
- tests/: contiene las pruebas automatizadas.
- app.py: archivo principal de la aplicación.
- sincronizar.py: permite ejecutar la sincronización desde la terminal.

## 6. Instalación y ejecución

### Requisitos

- Python instalado.
- SQL Server instalado y configurado.
- Controlador ODBC para SQL Server.

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Configurar variables de entorno

Crear un archivo `.env` tomando como referencia `.env.example` y configurar los datos de conexión a SQL Server.

### Crear la base de datos

Ejecutar el script:

`database/crear_base_datos.sql`

### Ejecutar la aplicación

```bash
python app.py
```

Abrir en el navegador:

`http://127.0.0.1:5000`

## 7. Pruebas del proyecto

Para ejecutar las pruebas automatizadas:

```bash
python -m unittest discover -s tests -v
```

## 8. Fuente de información

API de datos abiertos de Colombia:

https://www.datos.gov.co/

Conjunto de datos: Casos positivos de COVID-19 en Colombia.

Identificador del recurso: gt2j-8ykr

## 9. Aportes de los integrantes
La división registrada en el README original era:
- Integrante 1: consumo de API, procesamiento JSON y sincronización.
- Integrante 2: base de datos, persistencia y consultas SQL.
- Trabajo conjunto: integración, interfaz, MVC, pruebas, documentación y presentación.

## 12. Alcance y limitaciones

El proyecto realiza consulta, sincronización básica, almacenamiento y lectura filtrada. No implementa CRUD completo, autenticación de usuarios, edición/eliminación desde la web, despliegue público ni descarga masiva de todo el conjunto. La conexión real a SQL Server depende de la configuración local, el servicio SQL Server y el controlador ODBC instalado, aparte el proyecto académico consulta, procesamiento y almacenamiento de datos abiertos sobre COVID-19 en Colombia.