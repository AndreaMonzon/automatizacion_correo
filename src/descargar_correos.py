import os
import win32com.client
import pythoncom

from pathlib import Path

pythoncom.CoInitialize()

def  descargar():
 CARPETA_DESCARGA = Path("C:/app_automatizacion_correo")  # Ruta donde se guardarán los archivos descargados

 # Conéctese a Outlook
 outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
 inbox = outlook.GetDefaultFolder(6)  # Carpeta raíz de la bandeja de entrada

 # Diccionario para rastrear archivos adjuntos descargados por tema y fecha
 adjuntos_descargados = {}

 # Bucle para procesar los correos electrónicos
 for mensaje in inbox.Items:
    # Obtener información del correo electrónico
    asunto_correo = mensaje.Subject
    remitente_correo = mensaje.SenderName
    fecha_correo = mensaje.ReceivedTime.date()

    # Verificar si el correo electrónico tiene archivos adjuntos
    if mensaje.Attachments.Count > 0:
        # Guardar archivos adjuntos en formato PDF en la carpeta
        for adjunto in mensaje.Attachments:
            if adjunto.FileName.lower().endswith(".pdf") or adjunto.FileName.lower().endswith(".docx"):
                nuevo_nombre = f"{remitente_correo.replace(' ', '_')}_{adjunto.FileName}"
                ruta_adjunto = os.path.join(CARPETA_DESCARGA, nuevo_nombre)
                adjunto.SaveAsFile(ruta_adjunto)
                print(f"Adjunto '{adjunto.FileName}' guardado como '{nuevo_nombre}' en {CARPETA_DESCARGA}")

    # Registrar la descarga del adjunto para evitar duplicados
    adjuntos_descargados[(asunto_correo, fecha_correo)] = True


