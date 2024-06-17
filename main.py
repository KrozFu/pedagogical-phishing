import os
import random
import yagmail
import http.server
import socketserver
from dotenv import load_dotenv

# Definimos constantes
TIPOS_PHISHING = {
    "1": "Amazon",
    "2": "Facebook",
    "3": "Outlook",
    "4": "Gmail"
}
    
SALUDOS_Y_CUERPOS = {
    "Amazon": {
        "saludos": ["Estimado Usuario Amazon", "Estimado Cliente", "Hola"],
        "cuerpo": """
            Estimado usuario Amazon,

            Hemos detectado actividad inusual en su cuenta. Para garantizar la seguridad de su información, por favor haga clic en el siguiente enlace y cambie su contraseña de inmediato:

            <a href="{{ENLACE_FRAUDULENTO}}">Haga clic aquí para cambiar su contraseña</a>

            Gracias por su cooperación.

            Atentamente,
            El equipo de soporte técnico
        """
    },
    "Facebook": {
        "saludos": ["Estimado usuario Facebook", "Hola"],
        "cuerpo": """
            Estimado usuario Facebook,

            Hemos detectado actividad inusual en su cuenta. Para garantizar la seguridad de su información, por favor haga clic en el siguiente enlace y cambie su contraseña de inmediato:

            <a href="{{ENLACE_FRAUDULENTO}}">Haga clic aquí para cambiar su contraseña</a>

            Gracias por su cooperación.

            Atentamente,
            El equipo de soporte técnico
        """
    },
    "Outlook": {
        "saludos": ["Estimado usuario Outlook", "Hola"],
        "cuerpo": """
            Estimado usuario Outlook,

            Hemos detectado actividad inusual en su cuenta. Para garantizar la seguridad de su información, por favor haga clic en el siguiente enlace y cambie su contraseña de inmediato:

            <a href="{{ENLACE_FRAUDULENTO}}">Haga clic aquí para cambiar su contraseña</a>

            Gracias por su cooperación.

            Atentamente,
            El equipo de soporte técnico
        """
    },
   "Gmail": {
        "saludos": ["Estimado usuario Gmail", "Hola"],
        "cuerpo": """
            Estimado usuario Gmail,

            Hemos detectado actividad inusual en su cuenta. Para garantizar la seguridad de su información, por favor haga clic en el siguiente enlace y cambie su contraseña de inmediato:

            <a href="{{ENLACE_FRAUDULENTO}}">Haga clic aquí para cambiar su contraseña</a>

            Gracias por su cooperación.

            Atentamente,
            El equipo de soporte técnico
        """
    }
}

ASUNTO = "Urgente: Información de cuenta comprometida"

def generar_puerto_aleatorio():
    # Generar un puerto aleatorio entre 8000 y 8999
    return random.randint(8000, 8999)

def generar_correo(phishing_type, puerto, archivo_html):
    if phishing_type in SALUDOS_Y_CUERPOS:
        datos = SALUDOS_Y_CUERPOS[phishing_type]
        saludo = random.choice(datos["saludos"])
        cuerpo = datos["cuerpo"].strip()
        
        # Reemplazar {{ENLACE_FRAUDULENTO}} por la URL del archivo HTML correspondiente
        cuerpo = cuerpo.replace("{{ENLACE_FRAUDULENTO}}", f"http://localhost:{puerto}")
        
        return saludo, ASUNTO, cuerpo
    else:
        raise ValueError("Tipo de phishing no válido")

def levantar_servidor(archivo_html, puerto): 
    # Definir el handler para servir archivos desde la carpeta src/templates
    class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=os.path.join(os.getcwd(), 'src', 'templates'), **kwargs)
        
        def do_GET(self):
            # Sobreescribir el path para asegurar que siempre se sirva el archivo especificado
            self.path = archivo_html
            return super().do_GET()
    
    with socketserver.TCPServer(("", puerto), MyHttpRequestHandler) as httpd:
        print(f"Servidor local iniciado en http://localhost:{puerto}")
        httpd.serve_forever()

def enviar_correo(destinatarios, asunto, cuerpo, remitente, contrasena):
    try:
        yag = yagmail.SMTP(user=remitente, password=contrasena)
        for destinatario in destinatarios:
            yag.send(to=destinatario, subject=asunto, contents=cuerpo)
            print(f"Correo enviado a {destinatario}.")
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")

def seleccionar_tipo_phishing():
    print("Seleccione el tipo de phishing a generar:")
    for key, value in TIPOS_PHISHING.items():
        print(f"{key}. {value}")
    
    opcion = input("Ingrese el número de la opción deseada: ").strip()
    return TIPOS_PHISHING.get(opcion)

def cargar_destinatarios(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            destinatarios = [linea.strip() for linea in archivo if linea.strip()]
        return destinatarios
    except FileNotFoundError:
        print(f"Archivo {nombre_archivo} no encontrado.")
        return []
    except Exception as e:
        print(f"Error al leer el archivo {nombre_archivo}: {str(e)}")
        return []

def main():
    tipo_phishing = seleccionar_tipo_phishing()
    
    if tipo_phishing:
        try:
            archivo_html = f"{tipo_phishing.lower()}.html"
            puerto = generar_puerto_aleatorio()
            saludo, asunto, cuerpo = generar_correo(tipo_phishing, puerto, archivo_html)
            print("Enviando...")

            load_dotenv()
            remitente = os.getenv('EMAIL_REMITENTE')
            contrasena = os.getenv('EMAIL_CONTRASENA')
            
            if not remitente or not contrasena:
                print("Remitente o contraseña no configurados. Asegúrese de configurar las variables de entorno 'EMAIL_REMITENTE' y 'EMAIL_CONTRASENA'.")
                return

            nombre_archivo = 'emails.txt'
            destinatarios = cargar_destinatarios(nombre_archivo)
            
            if destinatarios:
                enviar_correo(destinatarios, asunto, cuerpo, remitente, contrasena)
                levantar_servidor(archivo_html, puerto)
                
            else:
                print("No se encontraron destinatarios válidos.")
        
        except ValueError as e:
            print(e)
    else:
        print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()