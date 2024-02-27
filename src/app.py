from flask import Flask,render_template,request,redirect,url_for,flash
import os
import database as db
import enviar_correo
import descargar_correos  
from pathlib import Path
import smtplib
import win32com.client as win32
import pythoncom





template_dir=os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir= os.path.join(template_dir,'src','templates')

app=Flask(__name__,template_folder=template_dir)

app.secret_key = 'Andreamonzon25_'
#Ruta de la aplicacion

@app.route('/')
def home():
    cursor =db.database.cursor()
    cursor.execute('select * from empresas')
    #devuelve en tuplas
    myresult=cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject=[]
    columnNames=[column[0] for column in cursor.description]
    for record in myresult:
        #dict para agregar los datos en formato diccionario
        insertObject.append(dict(zip(columnNames,record)))
    cursor.close()
    return render_template('index.html',data=insertObject)


@app.route('/user',methods=['POST'])
def addUser():
    nombre= request.form['nombre']
    correo= request.form['correo']


    if nombre and correo :
        cursor=db.database.cursor()
        sql='INSERT INTO empresas(nombre,correo) VALUES (%s , %s)'
        data=(nombre,correo)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('home'))


@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM empresas WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
       nombre= request.form['nombre']
       correo= request.form['correo']
       if nombre and correo :
        cursor=db.database.cursor()
        sql = "UPDATE empresas SET nombre = %s, correo = %s WHERE id = %s"
        data = (nombre, correo, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('home'))
    



@app.route('/enviar-correos', methods=['POST'])
def enviar_correos_route():
    pythoncom.CoInitialize()
    try:
        descargar_correos.descargar()
        enviar_correo.enviar()
        
        flash('Los correos se han enviado correctamente.', 'success')
    except Exception as e:
        flash('Ha ocurrido un error al enviar los correos: {}'.format(str(e)), 'danger')
    
    return redirect(url_for('home'))
                    
if __name__ =='__main__':
    app.run(debug=True,port=4000)
