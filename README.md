# Script de Actualización de Contenido de Interfaces

Este script en Python busca archivos en un directorio específico, procesa su contenido y guarda los archivos actualizados en otro directorio. El procesamiento incluye la adición de comas al final de cada línea de acuerdo con el tipo de archivo.

## Requisitos

- Python 3.x

## Instalación

1. Clona este repositorio en tu máquina local.
2. Asegúrate de tener Python 3.x instalado.
3. Puede generar el archivo `.exe`siguiendo estos pasos:
    1. Instalar la librería `pyinstaller` con el siguiente comando `pip install pyinstaller`
    2. Generar el ejecutable con el comando `pyinstaller --onefile main.py`
    3. Encontrar el archivo en la carpeta `dist`

## Uso

1. Ejecuta el script principal main.py.
2. Ingresa la ubicación de los archivos a actualizar cuando se te solicite.
3. Ingresa la ubicación donde deseas guardar los archivos actualizados.

## Descripción del Código

### Decorador `measure_run_time`

Este decorador mide el tiempo de ejecución de una función y muestra el tiempo transcurrido.

```py
def measure_run_time(func):
    def wrap(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'\t>>> La función {func.__name__}() tardó {end_time - start_time} segundos en ejecución')
        return result
    return wrap
```

### Función `get_files`

Esta función devuelve una lista de archivos en el directorio especificado que tienen extensiones válidas y contienen alguna de las interfaces especificadas en sus nombres.

```py
def get_files():
    is_interface =  lambda file_name: any(interface in file_name for interface in INTERFACES)

    return [
        file for file in os.listdir(SEARCH_DIR) 
        if file.split('.')[-1] in VALID_EXTENSIONS and is_interface(file)
    ]
```

### Función `process_files`

Esta función lee las líneas de los archivos de entrada y las escribe en diferentes archivos de destino según el prefijo del nombre del archivo.

```py
def process_files(files: list[str]):
    for file_name in files:
        original_file = join(SEARCH_DIR, file_name)
        final_file = join(DESTINATION_DIR, file_name)
        
        os.makedirs(os.path.dirname(final_file), exist_ok=True)

        with open(original_file, 'r') as file:
            lines = file.readlines()

        if 'ISEC' in file_name:
            write_lines(lines, final_file, 8)
        elif 'IFXD' in file_name:
            write_lines(lines, final_file, 1)
        elif 'ICUS' in file_name:
            write_lines(lines, final_file, 2)
        else:
            raise ValueError('Archivo no válido')
```

### Función `write_lines`

Esta función toma una lista de cadenas, escribe cada cadena en un archivo con un número especificado de repeticiones de una coma después de cada línea.

```py
def write_lines(original_lines: list[str], final_file: str, n_repetitions: int):
    with open(final_file, 'w') as file:
        for line in original_lines:
            file.write(f"{line.rstrip()}{',' * n_repetitions}\n")
```

### Ejecución Principal

```py
if __name__ == '__main__':
    found_files = get_files()
    process_files(found_files)
```
