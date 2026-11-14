
IF DB_ID('DatosAbiertosColombia') IS NULL
BEGIN
    CREATE DATABASE DatosAbiertosColombia;
END
GO

USE DatosAbiertosColombia;
GO

IF OBJECT_ID('dbo.CasosCovid', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.CasosCovid (
        id_de_caso BIGINT PRIMARY KEY,
        fecha_reporte_web DATE NULL,
        fecha_de_notificacion DATE NULL,
        departamento VARCHAR(10) NULL,
        departamento_nom NVARCHAR(100) NULL,
        ciudad_municipio VARCHAR(10) NULL,
        ciudad_municipio_nom NVARCHAR(150) NULL,
        edad INT NULL,
        unidad_medida VARCHAR(10) NULL,
        sexo VARCHAR(10) NULL,
        fuente_tipo_contagio NVARCHAR(100) NULL,
        ubicacion NVARCHAR(100) NULL,
        estado NVARCHAR(100) NULL,
        recuperado NVARCHAR(100) NULL,
        fecha_inicio_sintomas DATE NULL,
        fecha_diagnostico DATE NULL,
        fecha_recuperado DATE NULL,
        tipo_recuperacion NVARCHAR(100) NULL,
        per_etn_ VARCHAR(20) NULL,
        json_original NVARCHAR(MAX) NULL
    );
END
GO

IF COL_LENGTH('dbo.CasosCovid', 'json_original') IS NULL
BEGIN
    ALTER TABLE dbo.CasosCovid ADD json_original NVARCHAR(MAX) NULL;
END
GO

SELECT DB_NAME() AS BaseDeDatosCreada;

SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'CasosCovid';
GO
