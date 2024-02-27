import os
import smtplib
import win32com.client as win32
from pathlib import Path
import database as db
import pythoncom

pythoncom.CoInitialize()

def enviar():
 # Ruta de la carpeta que contiene los currículums en formato PDF
 carpeta_curriculums = Path("C:/app_automatizacion_correo")
 # Realiza una consulta a la base de datos para obtener los correos electrónicos de la tabla "empresas"
 cursor = db.database.cursor()
 cursor.execute('SELECT correo FROM empresas')
 destinatarios = [registro[0] for registro in cursor.fetchall()]
    

 # Crear una instancia de Outlook
 outlook = win32.Dispatch("Outlook.Application")

 # Bucle sobre las direcciones de correo electrónico
 count=0
 for destinatario in destinatarios:
    
   
    #Eliminar los espacios en blanco al principio y al final de la línea
    destinatario = destinatario.strip()
    # Crear un nuevo correo electrónico
    mail = outlook.CreateItem(0)
    # Establecer el destinatario
    mail.To = destinatario
    # Establecer el asunto y el cuerpo del correo electrónico
    mail.Subject = "Envío de currículum"
    mail.Body = "Adjunto encontrarás mi currículum vitae."
    
    # Bucle sobre los archivos en la carpeta de currículums
    for archivo in os.listdir(carpeta_curriculums):
        # Comprobar si el archivo es un PDF
        if archivo.lower().endswith(".pdf"):
            # Crear la ruta completa del archivo
            ruta_archivo = os.path.join(carpeta_curriculums, archivo)
            # Adjuntar el archivo al correo electrónico
            mail.Attachments.Add(ruta_archivo)
    
    # Enviar el correo electrónico
    mail.Send()



