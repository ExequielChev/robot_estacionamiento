import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
from PIL import Image
from PIL import ImageTk


BASE_PATH = os.path.join(os.getcwd())


def ejecutar_script(script_seleccionado, aviso_label, scripts_disponibles, cancelar_var):
    try:
        # Mostrar aviso de ejecución
        aviso_label.config(text="Ejecutando script...", fg="blue")
        aviso_label.update()

        # Obtén la ruta del script seleccionado
        ruta_script = scripts_disponibles.get(script_seleccionado)

        if ruta_script and os.path.exists(ruta_script):
            # Determinar la extensión del archivo
            _, extension = os.path.splitext(ruta_script)

            if extension.lower() == '.py':
                # Para archivos .py
                proceso = subprocess.Popen(["python", ruta_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # Esperar a que termine o se cancele
                while proceso.poll() is None and not cancelar_var.get():
                    pass

                # Verificar si se canceló
                if cancelar_var.get():
                    proceso.terminate()
                    messagebox.showinfo("Cancelación", "Ejecución cancelada.")
                    return

                # Obtener resultado
                resultado = proceso.communicate()[0]
            elif extension.lower() == '.robot':
                # Para archivos .robot (puede necesitar instalación de robotframework)
                resultado = subprocess.check_output(["robot", ruta_script], text=True)
            else:
                # Extensión no compatible
                raise ValueError(f"Extensión de archivo no compatible: {extension}")

            # Muestra el resultado en una ventana de mensaje
            messagebox.showinfo("Ejecución Exitosa", f"Resultado:\n\n{resultado}")
        else:
            messagebox.showerror("Error", "Script no encontrado.")

    except subprocess.CalledProcessError as e:
        # Captura errores específicos al ejecutar el script
        messagebox.showerror("Error", f"Error durante la ejecución:\n\n{e.output.decode()}")

    except Exception as e:
        # Muestra un mensaje de error si la ejecución falla
        messagebox.showerror("Error", f"Error durante la ejecución:\n\n{str(e)}")

    finally:
        # Ocultar aviso después de ejecución
        aviso_label.config(text="")
        aviso_label.update()

def cancelar_ejecucion(cancelar_var):
    # Configura la variable de cancelación en True
    cancelar_var.set(True)

def redimensionar_imagen(ruta_imagen, nuevo_ancho, nuevo_alto):
    # Redimensiona la imagen y devuelve el objeto ImageTk
    imagen = Image.open(ruta_imagen)
    imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto))
    return ImageTk.PhotoImage(imagen_redimensionada)


def crear_interfaz(scripts_disponibles):

    
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Ejecución de Script")
     # Establecer el tamaño de la ventana
    largo = 400
    ancho = 350
    ventana.geometry(f"{largo}x{ancho}")

    ruta_icono = os.path.join(BASE_PATH, "bot.ico")  # Reemplaza con la ruta correcta de tu ícono
    if os.path.exists(ruta_icono):
        ventana.iconbitmap(ruta_icono)

    # Configurar la imagen de fondo
    ruta_imagen = os.path.join(BASE_PATH, "muni.png")
    nueva_ancho = 220  # Ajusta según tus necesidades
    nueva_alto = 200   # Ajusta según tus necesidades
    fondo_imagen = redimensionar_imagen(ruta_imagen, nueva_ancho, nueva_alto)
    
    # Etiqueta para la imagen de fondo (como logotipo)



    # Lista de scripts
    combobox_scripts = ttk.Combobox(ventana, values=list(scripts_disponibles.keys()), font=('Arial', 12))
    combobox_scripts.set("Seleccione robot")
    combobox_scripts.pack(pady=10)
    # for script in scripts_disponibles:
    #     lista_scripts.insert(tk.END, script)
    # lista_scripts.pack(pady=10)

    
    # Etiqueta para el aviso de ejecución
    aviso_label = tk.Label(ventana, text="", fg="blue")
    aviso_label.pack()

    logo_label = tk.Label(ventana, image=fondo_imagen)
    logo_label.pack()

    # Botón de ejecución
    # boton_ejecutar = ttk.Button(ventana, text="Ejecutar Script Seleccionado", command=lambda: ejecutar_script_seleccionado(lista_scripts, aviso_label, scripts_disponibles))
    # boton_ejecutar.pack(pady=20)


       # Variable para el botón de alternar

    # Variable para la cancelación de la ejecución
    cancelar_var = tk.BooleanVar(value=False)

    boton_ejecutar = ttk.Button(ventana, text="Ejecutar Script Seleccionado", command=lambda: ejecutar_script_seleccionado(combobox_scripts, aviso_label, scripts_disponibles, cancelar_var))

    boton_ejecutar.pack(pady=20)

 
    ventana.configure(bg="Lightblue")  # Fondo oscuro
    logo_label.config(bg="Lightblue")   # Fondo oscuro para la etiqueta del logotipo
    aviso_label.config(bg="Lightblue")  # Fondo oscuro para la etiqueta de aviso
    # Fondo oscuro

    # Crear y configurar el estilo
    style = ttk.Style()

    # Utiliza el tema personalizado
    style.theme_use("clam")


    ventana.mainloop()
    
# Función para ejecutar el script seleccionado
def ejecutar_script_seleccionado(combobox_scripts, aviso_label, scripts_disponibles, cancelar_var):
    cancelar_var.set(False)
    script_seleccionado = combobox_scripts.get()
    ejecutar_script(script_seleccionado, aviso_label, scripts_disponibles, cancelar_var)

# Lista de scripts disponibles
scripts_disponibles = {
    "Iniciar Major": os.path.join(BASE_PATH, "Iniciar", "inicio.py"),
    "Robot Compromiso": os.path.join(BASE_PATH, "compromisoestacionamiento", "ejecutacomproest.py"),
    "Ocr Comprobantes": os.path.join(BASE_PATH, "Captura_compr.py"),
    "Robot Devengados": os.path.join(BASE_PATH, "devengadoestacionamiento", "ejecutadevest.py"),
}

# Ejecutar la creación de la interfaz
crear_interfaz(scripts_disponibles)