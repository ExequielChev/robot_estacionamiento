import subprocess

def ejecutar_script(nombre_script):
    subprocess.run(nombre_script, shell=True)

if __name__ == "__main__":
    # Scripts a ejecutar
    scripts = [

        "robot C:\\Users\\zcheveste\\Desktop\\robot_estacionamiento\\devengadoestacionamiento\\tasks.robot",

    ]

    # Ejecutar el primer script normalmente (OCR CARGA DE FACTURAS)
    ejecutar_script(scripts[0])