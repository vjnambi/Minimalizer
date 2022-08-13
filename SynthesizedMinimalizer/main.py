import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
import numpy
from SplotchFiller import fillSplotches
from SplotchFinder import findSplotches


window = tk.Tk()
window.title('Minimalizer')
for i in range(3):
    window.columnconfigure(i,weight=1)
    window.rowconfigure(i,weight=1)

canvas_size=600
canvas_size2=300
canvas_in = tk.Canvas(window, width=canvas_size, height=canvas_size, bd=0, highlightthickness=0, relief='ridge')
txt_coord = tk.Text(width=20, height=25)
outputframe = tk.Frame(window)
inputbuttonframe = tk.Frame(window)
canvas_out = tk.Canvas(outputframe, width=canvas_size2, height=canvas_size2, bd=0, highlightthickness=0, relief='ridge')
canvas_sug = tk.Canvas(outputframe, width=canvas_size2, height=canvas_size2, bd=0, highlightthickness=0, relief='ridge')



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

def handle_canvasin1(event):
    xcoord = event.x
    ycoord=event.y
    txt_coord.insert(tk.END,"\n"+str(xcoord)+", "+str(ycoord)+", 0")

def handle_canvasin2(event):
    xcoord = event.x
    ycoord=event.y
    txt_coord.insert(tk.END,"\n"+str(xcoord)+", "+str(ycoord)+", 2")

def handle_canvasin3(event):
    xcoord = event.x
    ycoord=event.y
    txt_coord.insert(tk.END,"\n"+str(xcoord)+", "+str(ycoord)+", 1")

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
        output_image = output_image.resize((canvas_size2, canvas_size2))
        output_image_tk = ImageTk.PhotoImage(output_image)
        window.output_image_tk = output_image_tk
        canvas_out.create_image((0, 0), image=output_image_tk, anchor="nw")
        canvas_out.update()

        suggestion_image = Image.open('./ArtSuggestion.png')
        suggestion_image = suggestion_image.resize((canvas_size2, canvas_size2))
        suggestion_image_tk = ImageTk.PhotoImage(suggestion_image)
        window.suggestion_image_tk = suggestion_image_tk
        canvas_sug.create_image((0, 0), image=suggestion_image_tk, anchor="nw")
        canvas_sug.update()

def handle_fnout():
    fn=""
    fn=asksaveasfilename()
    if not(fn == ""):
        export_image = Image.open('./ArtImage.png')
        export_image.save(fn)

def handle_auto():
    fname = txt_coord.get("1.0","2.0")
    txt_coord.insert(tk.END,findSplotches(fname, canvas_size))


canvas_in.bind("<Button-1>",handle_canvasin1)
canvas_in.bind("<Button-2>",handle_canvasin2)
canvas_in.bind("<Button-3>",handle_canvasin3)


btn_fnin = tk.Button(
    master=inputbuttonframe,
    text="Select input image",
    width=20,
    height=1,
    command=handle_fnin
)
btn_fnout = tk.Button(
    text="Save output image",
    width=20,
    height=1,
    command=handle_fnout
)
btn_run = tk.Button(
    text="Minimalize",
    width=20,
    height=1,
    command=handle_run
)
btn_auto = tk.Button(
    master=inputbuttonframe,
    text="Auto-Select",
    width=20,
    height=1,
    command=handle_auto
)
inputbuttonframe.grid(row=0, column=0, padx=5, pady=5)
btn_fnin.grid(row=0, column=0, padx=5, pady=5)
btn_auto.grid(row=0, column=1, padx=5, pady=5)
btn_run.grid(row=0,column=1,padx=5,pady=5)
btn_fnout.grid(row=0, column=2, padx=5, pady=5)
canvas_in.grid(row=1, column=0, padx=5, pady=5)
txt_coord.grid(row=1, column=1, padx=5, pady=5)
outputframe.grid(row=1, column=2,padx=5, pady=5)
canvas_out.pack()
canvas_sug.pack()


window.mainloop()
