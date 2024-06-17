# Utilizacion de la libreari yagmail para el envio de correos
import random
import yagmail

def generar_correo(phishing_type):
    saludos_y_cuerpos = {
        "Amazon": {
            "saludos": ["Estimado Usuario Amazon", "Estimado Cliente", "Hola"],
            "cuerpo": """
                Estimado usuario Amazon,

                Hemos detectado actividad inusual en su cuenta. Para garantizar la seguridad de su información, por favor haga clic en el siguiente enlace y cambie su contraseña de inmediato:

                [Enlace fraudulento]

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

                [Enlace fraudulento]

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

                [Enlace fraudulento]

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

                [Enlace fraudulento]

                Gracias por su cooperación.

                Atentamente,
                El equipo de soporte técnico
                """
        }
    }

    if phishing_type in saludos_y_cuerpos:
        datos = saludos_y_cuerpos[phishing_type]
        saludo = random.choice(datos["saludos"])
        asunto = "Urgente: Información de cuenta comprometida"
        cuerpo = datos["cuerpo"].strip()
        return saludo, asunto, cuerpo
    else:
        raise ValueError("Tipo de phishing no válido")

def enviar_correo(destinatarios, asunto, cuerpo, remitente, contrasena):
    try:
        yag = yagmail.SMTP(user=remitente, password=contrasena)
        for destinatario in destinatarios:
            yag.send(to=destinatario, subject=asunto, contents=cuerpo)
            print(f"Correo enviado a {destinatario}.")
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")

def main():
    print("Seleccione el tipo de phishing a generar:")
    print("1. Amazon")
    print("2. Facebook")
    print("3. Outlook")
    print("4. Gmail")
    
    opcion = input("Ingrese el número de la opción deseada: ").strip()
    
    opciones = {
        "1": "Amazon",
        "2": "Facebook",
        "3": "Outlook",
        "4": "Gmail"
    }
    
    tipo_phishing = opciones.get(opcion)
    
    if tipo_phishing:
        try:
            saludo, asunto, cuerpo = generar_correo(tipo_phishing)
            print("Enviando...")
            
            remitente = 'xxxxxxxxxxxxx@xxx.xx'  # Cambiar al correo proporcionado
            contrasena = 'xxxxxxxxxxxxx'  # Aquí deberías usar una contraseña real y segura
            
            # Lista de destinatarios
            destinatarios = ['xxxxxxxxxxxxx@xxx.xx']

            enviar_correo(destinatarios, asunto, cuerpo, remitente, contrasena)
        
        except ValueError as e:
            print(e)
    else:
        print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()
