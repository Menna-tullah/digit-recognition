from PIL import ImageTk,Image
import PIL.Image
import io
from tkinter import *
import tkinter as tk
import numpy as np
from keras.models import load_model

window = Tk()
window.configure(background='white')
window.title("Digit Recognition")
model = load_model('mnist.h5')

window.geometry('900x600')
window.resizable(0,0)


def destroy_widget(widget):
    widget.destroy()


def pred_digit():
    global no, no1
    ps = canvas.postscript(colormode='color')
    # use PIL to convert to PNG
    im1 = PIL.Image.open(io.BytesIO(ps.encode('utf-8')))
    img = im1.resize((28, 28))
    # convert rgb to grayscale
    img = img.convert('L')
    img = np.array(img)
    # reshaping to support our model input and normalizing
    img = img.reshape(1, 28, 28, 1)
    img = img/255.0
    # predicting the class
    res = model.predict([img])[0]
    pred = np.argmax(res)
    acc = max(res)
    no = tk.Label(window, text='Predicted Digit is: '+str(pred), width=34, height=1,
                  fg="white", bg="black",
                  font=('times', 16, ' bold '))
    no.place(x=460, y=380)

    no1 = tk.Label(window, text='Prediction Accuracy is: '+str(acc), width=34, height=1,
                   fg="white", bg="black",
                   font=('times', 16, ' bold '))
    no1.place(x=460, y=415)


def draw_digit(event):
    # canvas.configure(background="black")
    x = event.x
    y = event.y
    r = 10
    canvas.create_oval(x-r, y-r, x + r, y + r, fill='black')
    panel5.configure(state=NORMAL)


def clear_digit():
    panel5.configure(state=DISABLED)
    canvas.delete("all")
    try:
        no.destroy()
        no1.destroy()
    except:
        pass


panel5 = Button(window, text='Predict Digit', state=DISABLED, command=pred_digit, width=15, borderwidth=0,
                bg='midnightblue', fg='white', font=('times', 18, 'bold'))
panel5.place(x=60, y=305)

panel6 = Button(window, text='Clear', width=15, borderwidth=0, command=clear_digit, bg='red', fg='white',
                font=('times', 18, 'bold'))
panel6.place(x=60, y=355)

canvas = tk.Canvas(window, width=405, height=280, highlightthickness=1, highlightbackground="midnightblue",
                   cursor="pencil")
canvas.grid(row=0, column=0, pady=2, sticky=W,)
canvas.place(x=460, y=90)
canvas.bind("<B1-Motion>", draw_digit)

lab = tk.Label(window, text="Draw Digit...", width=18, height=1, fg="white", bg="midnightblue",
               font=('times', 16, ' bold '))
lab.place(x=554, y=60)

window.mainloop()