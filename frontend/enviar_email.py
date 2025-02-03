"""
Módulo para el envío de correos electrónicos usando SMTP de Gmail.
Proporciona una función simple para enviar correos con autenticación
y manejo de errores.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo(destinatario, asunto, mensaje):
    """
    Envía un correo electrónico usando el servidor SMTP de Gmail.
    
    Args:
        destinatario (str): Dirección de correo electrónico del destinatario
        asunto (str): Asunto del correo electrónico
        mensaje (str): Contenido del correo en formato texto plano
        
    Efectos:
        - Envía un correo electrónico a través de Gmail        
        
    Notas:
        - Utiliza credenciales predefinidas para el remitente
        - Requiere una contraseña de aplicación de Gmail
        - Usa TLS para la conexión segura
    """
    # Configurar el mensaje
    email = MIMEMultipart()    
    email['From'] = "lorenzovizcaino74@gmail.com"
    email['To'] = destinatario
    email['Subject'] = asunto
    

    # Credenciales de Gmail
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

