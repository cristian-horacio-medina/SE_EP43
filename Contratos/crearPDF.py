import os
import jinja2
import pdfkit

def crea_pdf(info, rutacss=''):
    # Obtener la ruta donde se ejecuta el script
    ruta_template = os.path.dirname(os.path.abspath(__file__))
    
    # Buscar el archivo HTML en el directorio de templates
    try:
        nombre_template = next(f for f in os.listdir(ruta_template) if f.endswith('.html'))
    except StopIteration:
        print("No se encontró un archivo HTML en la carpeta.")
        return
    # Ruta del logo
    logo_path = os.path.join(ruta_template, 'Logo_b_n.png') 
        
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_template))
    template = env.get_template(nombre_template)
    html = template.render(info, logo_path=logo_path)

    options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
        'margin-top': '1cm',
        'margin-right': '1cm',
        'margin-left': '2cm',
        'margin-bottom': '1cm',
        'disable-smart-shrinking': '',
        'enable-local-file-access': ''
    }

    # Configuración del ejecutable wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

    # Definir la ruta de salida para el PDF
    ruta_salida = os.path.join(os.path.expanduser("~"), "Documents", "output.pdf")
    
    try:
        pdfkit.from_string(html, ruta_salida, options=options, configuration=config)
        print(f"PDF generado correctamente en: {ruta_salida}")
    except Exception as e:
        print(f"Ocurrió un error: {e}") 

# Ejecuto la función
if __name__ == "__main__":
    # info = {"docente","carrera","materia","año","division","turno","dia","horario", "DNI"}
    # crea_pdf(info)
    info["materias_por_año"] = materias_por_año  # Estructura que agrupaste
    crea_pdf(info)  # Llama a tu función con la información completa

