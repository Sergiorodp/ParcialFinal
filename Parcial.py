import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


from pyfirmata import Arduino, util
from tkinter import *
from PIL import Image
from PIL import ImageTk
import time

placa = Arduino ('COM3')
it = util.Iterator(placa)
it.start()
time.sleep(0.5)

a_0 = placa.get_pin('a:0:i')
a_1 = placa.get_pin('a:1:i')

pin_led4 = placa.get_pin('d:10:p')
pin_led5 = placa.get_pin('d:9:p')

xcenter = 150

cont1 = 0
cont2 = 0

girar = False
promedio = False
update = False

promA1,promA2 = 0,0

datosA1 = [0,0,0,0,0,0,0,0,0,0]
datosA2 = [0,0,0,0,0,0,0,0,0,0]

conttime = 0

ventana = Tk()
ventana.geometry('600x300')
ventana.title("Parcial")

cred = credentials.Certificate('key/key.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://testdatabase-c031c.firebaseio.com/'
})


marco1 = Frame(ventana, bg="gray", highlightthickness=1, width=600, height=300, bd= 5)
marco1.place(x = 0,y = 0)

cont_indicador= Label(marco1, text=str(cont1),bg='cadet blue1', font=("Arial Bold", 15), fg="white")
cont_indicador.place(x=0 + xcenter, y=90)

aviso_adc1 =Label(marco1, text="ADC1",bg='cadet blue1', font=("Arial Bold", 15), fg="white")
aviso_adc1.place(x =0 + xcenter,y=130)

cont_indicador1= Label(marco1, text=str(cont2),bg='cadet blue1', font=("Arial Bold", 15), fg="white")
cont_indicador1.place(x=100 + xcenter, y=90)

aviso_adc2 =Label(marco1, text="ADC2",bg='cadet blue1', font=("Arial Bold", 15), fg="white")
aviso_adc2.place(x = 100 + xcenter,y=130)

entry = Entry(marco1)
entry.place(x=150, y=200)

def update_label(input):
    global cont1,cont2
    global girar
    global promedio
    global update

    content = entry.get()
    entry.delete(0, END)

    if str(content).lower() == 'i':
        print("i")
        girar = not(girar)

    if str(content).lower() == 'p' :
        print("p")
        promedio = True
    if str(content).lower() == 'g' :
        print("g")
        update = True



def Act(cont1,cont2):
    global promA1,promA2

    ref = db.reference("parcialInfo")
    ref.update({
        'ADC1': {
            'prom' : promA1,
            'valActual' : cont1,
            }
        }
    )

    ref.update({
        'ADC2':{
            'prom':promA2,
            'valActual' : cont2,
        }
    })



def update_win():
    global a_0,a_1
    global cont1,cont2
    global pin_led4, pin_led5
    global conttime
    global girar,update
    global promedio,promA1,promA2
    global datosA1,datosA2

    data1,data2 = 0,0

    cont1 = a_0.read()
    cont2 = a_1.read()

    if(girar):
        data1 = cont2
        data2 = cont1
    else:
        data1 = cont1
        data2 = cont2

    if(promedio):
        sum1 = 0
        sum2 = 0
        for i in range(10):
            cont1 = a_0.read()
            cont2 = a_1.read()
            sum1 += cont1
            sum2 +=cont2
            datosA1[i] = cont1
            datosA2[i] = cont2
        promA1 = sum1/10
        promA2 = sum2/10
        print(datosA1)
        print(datosA2)
        print(promA1, " y ", promA2) 
        promedio = False
    
    if(update):
        Act(cont1,cont2)
        update = False

    pin_led4.write(data1)
    cont_indicador.config(text = str(cont1))
    pin_led5.write(data2)
    cont_indicador1.config(text = str(cont2))

    ventana.after(10,update_win)

Label(ventana, text="Input: ").place(x=160, y=180)
entry.bind('<Return>', update_label) 

update_win()

ventana.mainloop()