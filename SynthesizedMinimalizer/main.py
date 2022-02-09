import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
import numpy
from SplotchFiller import fillSplotches


window = tk.Tk()
window.title('Minimalizer')
window.iconphoto(False, tk.PhotoImage(file='ArtSatoriChirei.png'))
for i in range(3):
    window.columnconfigure(i,weight=1)
    window.rowconfigure(i,weight=1)

canvas_size=308
canvas_in = tk.Canvas(window, width=canvas_size, height=canvas_size)
txt_coord = tk.Text(width=50, height=25)
canvas_out = tk.Canvas(window, width=canvas_size, height=canvas_size)


def handle_fnin():
    fn = ""
    fn = askopenfilename(parent=window, initialdir="./", title='Select an image')
    if not(fn == ""):
        txt_coord.delete(1.0,tk.END)
        txt_coord.insert(tk.END,fn)
        input_image = Image.open(fn)
        input_image = input_image.resize((canvas_size, canvas_size))
        input_image_tk = ImageTk.PhotoImage(input_image)
        window.input_image_tk = input_image_tk
        canvas_in.create_image((0, 0), image=input_image_tk, anchor="nw")
        canvas_in.update()

def handle_canvasin(event):
    xcoord = event.x
    ycoord=event.y
    txt_coord.insert(tk.END,"\n"+str(xcoord)+", "+str(ycoord))

def handle_run():
    fname = txt_coord.get("1.0","2.0")
    coords = numpy.array(numpy.fromstring(txt_coord.get(str(2)+".0",str(3)+".0"),sep=','))
    for i in range(3,int(txt_coord.index('end').split('.')[0])):
        target = numpy.fromstring(txt_coord.get(str(i)+".0",str(i+1)+".0"),sep=',')
        coords = numpy.vstack((coords,target))
    try:
        window.title('Minimalizer (Loading...)')
        fillSplotches(fname, coords, canvas_size)
    except:
        window.title('Minimalizer (Invalid Input)')
    else:
        window.title('Minimalizer')
        output_image = Image.open('./ArtImage.png')
        output_image = output_image.resize((canvas_size, canvas_size))
        output_image_tk = ImageTk.PhotoImage(output_image)
        window.output_image_tk = output_image_tk
        canvas_out.create_image((0, 0), image=output_image_tk, anchor="nw")
        canvas_out.update()

def handle_fnout():
    fn=""
    fn=asksaveasfilename()
    if not(fn == ""):
        export_image = Image.open('./ArtImage.png')
        export_image.save(fn)

canvas_in.bind("<Button-1>",handle_canvasin)


btn_fnin = tk.Button(
    text="Select input image...",
    width=42,
    height=1,
    command=handle_fnin
)
btn_fnout = tk.Button(
    text="Save output image",
    width=42,
    height=1,
    command=handle_fnout
)
btn_run = tk.Button(
    text="Minimalize",
    width=42,
    height=1,
    command=handle_run
)

btn_fnin.grid(row=0, column=0, padx=5, pady=5)
btn_run.grid(row=0,column=1,padx=5,pady=5)
btn_fnout.grid(row=0, column=2, padx=5, pady=5)
canvas_in.grid(row=1, column=0, padx=5, pady=5)
txt_coord.grid(row=1, column=1, padx=5, pady=5)
canvas_out.grid(row=1,column=2,padx=5,pady=5)


window.mainloop()
