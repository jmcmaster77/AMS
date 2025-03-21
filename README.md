# Project name
## Admin me Store
Stanalone Project
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
> Antes de ejecutar la webapp se debe crear una base de datos llamada ams y agregar y restaurar los datos del siguiente backup
> el parametro -p se utiliza para colocar la contraseña en caso de que el usuaro root la tenga configurada de lo contrario e puede omitir

Desde una consola de comandos de windows 
```bash
mariadb -u root -p ams < ams240804_0322.sql
```

Desde una consola de powershell
```bash
Get-Content ams240705.db | mariadb -u root -p ams
```

> [!NOTE]
> La ip por la cual se puede acceder a la web app es la del servidor el puerto 5000 y el puerto 3006 para el servidor de mariadb.


```bash
ejemplo 10.0.0.3:5000
```
![image](https://github.com/user-attachments/assets/34ad6139-6414-46d9-8a88-a2a1cbdbc626)

### en siguiente url muesta la vista del login 

http://10.0.0.3:5000/main

![image](https://github.com/user-attachments/assets/d6410b61-ded4-40eb-ac80-d57a0a2778eb)


> [!TIP] 
> verificar que la webapp esta en ejecucion 

### Documentación adicional 

En el siguiente apartado, se puede ver la documentacion mas detallada de la WEBAPP.

[Documentación detallada](DETAILS.md)
