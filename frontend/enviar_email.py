import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo(destinatario, asunto, mensaje):
    """
    Envía un correo electrónico usando SMTP de Gmail.
    
    Parámetros:
    remitente (str): Dirección de correo del remitente (Gmail)
    contraseña (str): Contraseña de aplicación de Gmail
    destinatario (str): Dirección de correo del destinatario
    asunto (str): Asunto del correo
    mensaje (str): Contenido del correo
    """
    # Configurar el mensaje
    email = MIMEMultipart()
    #email['From'] = "lorenzovizcaino@gmail.com"
    email['From'] = "lorenzovizcaino74@gmail.com"
    email['To'] = destinatario
    email['Subject'] = asunto
    #remitente = "lorenzovizcaino@gmail.com"
    #contraseña="dpms ufyv ojcd lxar"


    remitente = "lorenzovizcaino74@gmail.com"    
    contraseña="zctk lbdp uuib rafr"
    
    
    # Agregar el cuerpo del mensaje
    email.attach(MIMEText(mensaje, 'plain'))
    
    try:
        # Crear la conexión SMTP con Gmail
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        
        # Iniciar sesión
        servidor.login(remitente, contraseña)
        
        # Enviar el correo
        texto = email.as_string()
        servidor.sendmail(remitente, destinatario, texto)
        
        # Cerrar la conexión
        servidor.quit()
        
        print("Correo enviado correctamente")
        
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")

