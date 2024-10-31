import os
import time

from os.path import join


def measure_run_time(func):
    """
    The `measure_run_time` function is a Python decorator that measures the execution time of a given
    function.
    
    :param func: The `func` parameter in the `measure_run_time` function is a function that you want to
    measure the execution time of. The `measure_run_time` function is a decorator that calculates the
    time taken for the provided function to execute and prints out the duration in seconds after the
    function has completed its
    :return: The `measure_run_time` function is returning the `wrap` function, which is a wrapper
    function that measures the execution time of the input function `func`.
    """
    def wrap(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'\t>>> La función {func.__name__}() tardó {end_time - start_time} segundos en ejecución')
        return result
    return wrap



SEARCH_DIR = input("Por favor, ingrese la ubicación de los archivos a actualizar: ").replace('/', '\\')
DESTINATION_DIR = input("Por favor, ingres la ubicación donde desea guardar los archivos actualizados: ").replace('/', '\\')
VALID_EXTENSIONS = ('txt', 'csv')
INTERFACES = ['ISEC', 'IFXD', 'ICUS']


@measure_run_time
def get_files():
    """
    This function returns a list of files in a specified directory that have valid extensions and
    contain any of the specified interfaces in their names.
    :return: A list of files in the SEARCH_DIR directory that have valid extensions and contain any of
    the interfaces specified in the INTERFACES list.
    """
    is_interface =  lambda file_name: any(interface in file_name for interface in INTERFACES)

    return [
        file for file in os.listdir(SEARCH_DIR) 
        if file.split('.')[-1] in VALID_EXTENSIONS and is_interface(file)
    ]


@measure_run_time
def process_files(files: list[str]):
    """
    The function `process_files` reads lines from input files and writes them to different destination
    files based on the file name prefix.
    
    :param files: The `process_files` function takes a list of file names as input. It then processes
    each file based on certain conditions in the file name. Depending on whether the file name contains
    'ISEC', 'IFXD', or 'ICUS', it calls the `write_lines` function with a specific
    :type files: list[str]
    """
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
    

@measure_run_time
def write_lines(original_lines: list[str], final_file: str, n_repetitions: int):
    """
    The function `write_lines` takes a list of strings, writes each string to a file with a specified
    number of repetitions of a comma after each line.
    
    :param original_lines: A list of strings representing the lines of text that you want to write to
    the final file
    :type original_lines: list[str]
    :param final_file: The `final_file` parameter is a string that represents the file path where the
    modified lines will be written to. This function takes a list of original lines, repeats each line
    by adding a specified number of commas at the end, and writes the modified lines to the specified
    file
    :type final_file: str
    :param n_repetitions: The `n_repetitions` parameter specifies the number of times a comma should be
    added at the end of each line in the `final_file`
    :type n_repetitions: int
    """
    with open(final_file, 'w') as file:
        for line in original_lines:
            file.write(f"{line.rstrip()}{',' * n_repetitions}\n")
    

if __name__ == '__main__':
    found_files = get_files()
    process_files(found_files)
