/*	1.- BASE DE DATOS Y CARACTERISTICAS (DISEÑO Y MODELADO)	
CREATE DATABASE BIBLIOTECA_U*/
--GO
--USE BIBLIOTECA_U

--CREATE TABLE LIBRO(
--	NOMBRE_LIBRO NVARCHAR(100),
--	AUTOR_LIBRO NVARCHAR(100),
--	ISBN INT,
--	ID_LIBRO INT,
--	FECHA_PUBLICACION_LIBRO DATE,
--	EDITORIAL_LIBRO NVARCHAR(100),
--	NUM_PAGINAS_LIBRO INT)

--CREATE TABLE INVENTARIO(
--	ID_SECCION INT,
--	ID_LIBRO INT,
--	GENERO_SECCION NVARCHAR(100),
--	CANTIDAD INT)

--CREATE TABLE PRESTAMOS(
--	ID_PRESTAMO INT,
--	ID_LIBRO INT,
--	MATRICULA_U NVARCHAR(20),
--	FECHA_PRESTAMO DATE,
--	FECHA_DEVOLUCION DATE,
--	ESTADO NVARCHAR(20))

--CREATE TABLE USUARIOS(
--	MATRICULA_U NVARCHAR(20),
--	NOMBRE_U NVARCHAR(100),
--	CARRERA_U NVARCHAR(100),
--	FACULTAD_U NVARCHAR(100),
--	CAMPUS_U NVARCHAR(100))
	
--CREATE TABLE REGISTROS(
--	NUM_MOVIMIENTO INTEGER,
--	TIPO_MOVIMIENTO NVARCHAR(20),
--	FECHA_MOVIMIENTO DATE,
--	ID_LIBRO INTEGER,
--	MATRICULA_U NVARCHAR(20),
--	USUARIO_AUTORIZO NVARCHAR(100))

/*	2.- Usuarios y Permisos	*/
--CREATE USER 

/*	3.- Contruccion de Dispensadores (Triggers)	*/
--TABLA PRESTAMOS
--CREATE TRIGGER DBO.NUEVO_PRESTAMO --NOMBRE DEL TRIGGER
--ON DBO.PRESTAMOS --NOMBRE DE LA TABLA
--FOR INSERT --EVENTO
--AS
--BEGIN --SENTENCIAS
--	DECLARE @NUM INT;
--	SET @NUM = (SELECT COUNT(*) FROM DBO.REGISTROS) + 1;
--	INSERT INTO DBO.REGISTROS(
--	NUM_MOVIMIENTO,
--	TIPO_MOVIMIENTO,
--	FECHA_MOVIMIENTO,
--	ID_LIBRO,
--	MATRICULA_U,
--	USUARIO_AUTORIZO)
--	SELECT
--		@NUM,
--		'PRESTAMO',
--		GETDATE(),
--		P.ID_LIBRO,
--		P.MATRICULA_U,
--		USER_NAME()
--	FROM PRESTAMOS P
--END

--CREATE TRIGGER DBO.MODIF_PRESTAMO --NOMBRE DEL TRIGGER
--ON DBO.PRESTAMOS --NOMBRE DE LA TABLA
--FOR UPDATE --EVENTO
--AS
--BEGIN --SENTENCIAS
--	DECLARE @NUM INT;
--	SET @NUM = (SELECT COUNT(*) FROM DBO.REGISTROS) + 1;
--	INSERT INTO DBO.REGISTROS(
--	NUM_MOVIMIENTO,
--	TIPO_MOVIMIENTO,
--	FECHA_MOVIMIENTO,
--	ID_LIBRO,
--	MATRICULA_U,
--	USUARIO_AUTORIZO)
--	SELECT
--		@NUM,
--		'PRESTAMO (MODIFICACION)',
--		GETDATE(),
--		P.ID_LIBRO,
--		P.MATRICULA_U,
--		USER_NAME()
--	FROM PRESTAMOS P
--END

--CREATE TRIGGER DBO.BORRA_PRESTAMO --NOMBRE DEL TRIGGER
--ON DBO.PRESTAMOS --NOMBRE DE LA TABLA
--FOR DELETE --EVENTO
--AS
--BEGIN --SENTENCIAS
--	DECLARE @NUM INT;
--	SET @NUM = (SELECT COUNT(*) FROM DBO.REGISTROS) + 1;
--	INSERT INTO DBO.REGISTROS(
--	NUM_MOVIMIENTO,
--	TIPO_MOVIMIENTO,
--	FECHA_MOVIMIENTO,
--	ID_LIBRO,
--	MATRICULA_U,
--	USUARIO_AUTORIZO)
--	SELECT
--		@NUM,
--		'PRESTAMO (ELIMINACION)',
--		GETDATE(),
--		P.ID_LIBRO,
--		P.MATRICULA_U,
--		USER_NAME()
--	FROM PRESTAMOS P
--END

--TABLA LIBRO
--CREATE TRIGGER DBO.NUEVO_LIBRO
--ON DBO.LIBRO 
--FOR INSERT
--AS
--BEGIN 
--	DECLARE @NUM INT;
--	SET @NUM = (SELECT COUNT(*) FROM DBO.REGISTROS) + 1;
--	INSERT INTO DBO.REGISTROS(
--	NUM_MOVIMIENTO,
--	TIPO_MOVIMIENTO,
--	FECHA_MOVIMIENTO,
--	ID_LIBRO,
--	MATRICULA_U,
--	USUARIO_AUTORIZO)
--	SELECT
--		@NUM,
--		'NUEVO LIBRO',
--		GETDATE(),
--		L.ID_LIBRO,
--		'N/A',
--		USER_NAME()
--	FROM LIBRO L
--END

--CREATE TRIGGER DBO.MODIF_LIBRO
--ON DBO.LIBRO 
--FOR UPDATE
--AS
--BEGIN 
--	DECLARE @NUM INT;
--	SET @NUM = (SELECT COUNT(*) FROM DBO.REGISTROS) + 1;
--	INSERT INTO DBO.REGISTROS(
--	NUM_MOVIMIENTO,
--	TIPO_MOVIMIENTO,
--	FECHA_MOVIMIENTO,
--	ID_LIBRO,
--	MATRICULA_U,
--	USUARIO_AUTORIZO)
--	SELECT
--		@NUM,
--		'MODIFICAR LIBRO',
--		GETDATE(),
--		L.ID_LIBRO,
--		'N/A',
--		USER_NAME()
--	FROM LIBRO L
--END

--CREATE TRIGGER DBO.BORRAR_LIBRO
--ON DBO.LIBRO 
--FOR DELETE
--AS
--BEGIN 
--	DECLARE @NUM INT;
--	SET @NUM = (SELECT COUNT(*) FROM DBO.REGISTROS) + 1;
--	INSERT INTO DBO.REGISTROS(
--	NUM_MOVIMIENTO,
--	TIPO_MOVIMIENTO,
--	FECHA_MOVIMIENTO,
--	ID_LIBRO,
--	MATRICULA_U,
--	USUARIO_AUTORIZO)
--	SELECT
--		@NUM,
--		'ELIMINAR LIBRO',
--		GETDATE(),
--		L.ID_LIBRO,
--		'N/A',
--		USER_NAME()
--	FROM LIBRO L
--END

--TABLA USUARIOS
--CREATE TRIGGER DBO.NUEVO_USUARIO
--ON DBO.USUARIOS
--FOR INSERT
--AS
--BEGIN 
--	DECLARE @NUM INT;
--	SET @NUM = (SELECT COUNT(*) FROM DBO.REGISTROS) + 1;
--	INSERT INTO DBO.REGISTROS(
--	NUM_MOVIMIENTO,
--	TIPO_MOVIMIENTO,
--	FECHA_MOVIMIENTO,
--	ID_LIBRO,
--	MATRICULA_U,
--	USUARIO_AUTORIZO)
--	SELECT
--		@NUM,
--		'NUEVO USUARIO',
--		GETDATE(),
--		'N/A',
--		U.MATRICULA_U,
--		USER_NAME()
--	FROM USUARIOS U
--END

--CREATE TRIGGER DBO.MODIF_USUARIO
--ON DBO.USUARIOS
--FOR UPDATE
--AS
--BEGIN 
--	DECLARE @NUM INT;
--	SET @NUM = (SELECT COUNT(*) FROM DBO.REGISTROS) + 1;
--	INSERT INTO DBO.REGISTROS(
--	NUM_MOVIMIENTO,
--	TIPO_MOVIMIENTO,
--	FECHA_MOVIMIENTO,
--	ID_LIBRO,
--	MATRICULA_U,
--	USUARIO_AUTORIZO)
--	SELECT
--		@NUM,
--		'MODIFICAR USUARIO',
--		GETDATE(),
--		'N/A',
--		U.MATRICULA_U,
--		USER_NAME()
--	FROM USUARIOS U
--END

--CREATE TRIGGER DBO.BORRAR_USUARIO
--ON DBO.USUARIOS
--FOR DELETE
--AS
--BEGIN 
--	DECLARE @NUM INT;
--	SET @NUM = (SELECT COUNT(*) FROM DBO.REGISTROS) + 1;
--	INSERT INTO DBO.REGISTROS(
--	NUM_MOVIMIENTO,
--	TIPO_MOVIMIENTO,
--	FECHA_MOVIMIENTO,
--	ID_LIBRO,
--	MATRICULA_U,
--	USUARIO_AUTORIZO)
--	SELECT
--		@NUM,
--		'ELIMINAR USUARIO',
--		GETDATE(),
--		'N/A',
--		U.MATRICULA_U,
--		USER_NAME()
--	FROM USUARIOS U
--END


--TABLA INVENTARIO
--CREATE TRIGGER DBO.LIBRO_NUEVO_INVENTARIO
--ON DBO.USUARIOS
--FOR INSERT
--AS
--BEGIN 
--	DECLARE @NUM INT;
--	SET @NUM = (SELECT COUNT(*) FROM DBO.REGISTROS) + 1;
--	INSERT INTO DBO.REGISTROS(
--	NUM_MOVIMIENTO,
--	TIPO_MOVIMIENTO,
--	FECHA_MOVIMIENTO,
--	ID_LIBRO,
--	MATRICULA_U,
--	USUARIO_AUTORIZO)
--	SELECT
--		@NUM,
--		'NUEVO LIBRO EN EL INVENTARIO',
--		GETDATE(),
--		I.ID_LIBRO,
--		'N/A',
--		USER_NAME()
--	FROM INVENTARIO I
--END

--CREATE TRIGGER DBO.MODIF_INVENTARIO
--ON DBO.USUARIOS
--FOR INSERT
--AS
--BEGIN 
--	DECLARE @NUM INT;
--	SET @NUM = (SELECT COUNT(*) FROM DBO.REGISTROS) + 1;
--	INSERT INTO DBO.REGISTROS(
--	NUM_MOVIMIENTO,
--	TIPO_MOVIMIENTO,
--	FECHA_MOVIMIENTO,
--	ID_LIBRO,
--	MATRICULA_U,
--	USUARIO_AUTORIZO)
--	SELECT
--		@NUM,
--		'MODIFICACION AL INVENTARIO',
--		GETDATE(),
--		I.ID_LIBRO,
--		'N/A',
--		USER_NAME()
--	FROM INVENTARIO I
--END

--CREATE TRIGGER DBO.BORRAR_INVENTARIO

/*	4.- Construcción de Notificaciones	*/
-- Formato exacto de sp_send_dbmail visto en tu diapositiva (Mínimo 3 objetos)

-- Objeto 1: Correo para reportar un nuevo préstamo
CREATE PROCEDURE DBO.NOTIFICAR_NUEVO_PRESTAMO
    @MATRICULA NVARCHAR(20),
    @ID_LIBRO INT
AS
BEGIN
    DECLARE @MENSAJE NVARCHAR(MAX)
    SET @MENSAJE = 'Se ha generado un nuevo prestamo del libro con ID ' + CAST(@ID_LIBRO AS NVARCHAR(10)) + ' asignado al alumno con matricula ' + @MATRICULA

    EXEC msdb.dbo.sp_send_dbmail
        @profile_name = 'Perfil_Biblioteca',
        @recipients = 'control.biblioteca@u.com',
        @subject = 'Alerta: Nuevo Prestamo',
        @body = @MENSAJE
END
GO

-- Objeto 2: Correo para alertar sobre inventario bajo
CREATE PROCEDURE DBO.NOTIFICAR_STOCK_BAJO
    @ID_LIBRO INT,
    @CANTIDAD INT
AS
BEGIN
    DECLARE @MENSAJE NVARCHAR(MAX)
    SET @MENSAJE = 'Alerta de stock: El libro con ID ' + CAST(@ID_LIBRO AS NVARCHAR(10)) + ' tiene pocas unidades en el inventario. Quedan: ' + CAST(@CANTIDAD AS NVARCHAR(10))

    EXEC msdb.dbo.sp_send_dbmail
        @profile_name = 'Perfil_Biblioteca',
        @recipients = 'almacen.biblioteca@u.com',
        @subject = 'Alerta: Inventario Bajo',
        @body = @MENSAJE
END
GO

-- Objeto 3: Correo para confirmar una devolución de libro
CREATE PROCEDURE DBO.NOTIFICAR_DEVOLUCION
    @MATRICULA NVARCHAR(20),
    @ID_LIBRO INT
AS
BEGIN
    DECLARE @MENSAJE NVARCHAR(MAX)
    SET @MENSAJE = 'El sistema registro la devolucion del libro con ID ' + CAST(@ID_LIBRO AS NVARCHAR(10)) + ' por el alumno ' + @MATRICULA

    EXEC msdb.dbo.sp_send_dbmail
        @profile_name = 'Perfil_Biblioteca',
        @recipients = 'control.biblioteca@u.com',
        @subject = 'Confirmacion: Libro Devuelto',
        @body = @MENSAJE
END
GO


/*	5.- Contruccion de Jobs	*/
-- Formato exacto de sp_add_job y sp_add_jobstep visto en tu diapositiva (Mínimo 3 objetos)

USE msdb
GO

-- Objeto 1: Job para actualizar estados vencidos automáticamente
EXEC sp_add_job
    @job_name = 'Job_Vencer_Prestamos'

EXEC sp_add_jobstep
    @job_name = 'Job_Vencer_Prestamos',
    @step_name = 'Paso_Vencer',
    @subsystem = 'TSQL',
    @command = 'UPDATE BIBLIOTECA_U.dbo.PRESTAMOS SET ESTADO = ''VENCIDO'' WHERE FECHA_DEVOLUCION < GETDATE() AND ESTADO = ''ACTIVO'''
GO

-- Objeto 2: Job para eliminar registros viejos de movimientos (Mantenimiento)
EXEC sp_add_job
    @job_name = 'Job_Limpieza_Historico'

EXEC sp_add_jobstep
    @job_name = 'Job_Limpieza_Historico',
    @step_name = 'Paso_Eliminar',
    @subsystem = 'TSQL',
    @command = 'DELETE FROM BIBLIOTECA_U.dbo.REGISTROS WHERE FECHA_MOVIMIENTO < DATEADD(year, -2, GETDATE())'
GO

-- Objeto 3: Job para revisar libros en inventario sin existencias
EXEC sp_add_job
    @job_name = 'Job_Revisar_Inventario_Cero'

EXEC sp_add_jobstep
    @job_name = 'Job_Revisar_Inventario_Cero',
    @step_name = 'Paso_Consultar',
    @subsystem = 'TSQL',
    @command = 'SELECT ID_LIBRO, CANTIDAD FROM BIBLIOTECA_U.dbo.INVENTARIO WHERE CANTIDAD = 0'
GO