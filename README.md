# Project name
## Admin me Store

## Version 

Versión en desarrollo v.0.5

## Description

Webapp escrita en python, Flask con conexion a una base de datos alojada en mariadb esta webapp se puede realizar lo siguiente:
Gestion usuarios
Control de usuarios
Registro de Proveedor
	contactos proveedor 
Registro de Compras
Registro de Articulos

Registro de Clientes
Registro de Ventas, personas, vehiculos, oficiales y infracciones.

## Requerimientos e instalación 

Se recomienda un entorno virtual. 

## configurando el entorno virtual 

```bash
python -m virtualenv venv
```

## activando el entorno virtual en windows (cmd)

```bash
.\venv\Scripts\activate.bat
```

## activando el entorno virtual en windows (powershell)

```bash
.\venv\Scripts\Activate.ps1
```

## activando el entorno virtual en linux

```bash
source ./venv/bin/activate
```

## instalado las dependencias

```bash
pip install -r requirements.txt
```

## iniciando la webapp 

```bash
python src/main.py
```

> [!NOTE]
> Esta api está configurada con el puerto 5000 para la webapp y el puerto 3006 para el servidor de mariadb.


```bash
docker-compose up
```

### en siguiente url muesta la vista del login 

http://localhost:5000/main

> [!TIP] 
> verificar que la webapp esta en ejecucion 

### Documentación adicional 

> [!TIP] 
> en desarrollo 
