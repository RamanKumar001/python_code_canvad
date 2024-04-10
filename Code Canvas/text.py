from tkinter import *
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename,asksaveasfilename
import os
import subprocess
import keyword
import builtins
import webbrowser
import re  #use in search and replace

#deafault font size
font_size = 13

root = Tk()
root.geometry('900x500')
root.minsize(400,650)
root.title("CodeCanvas - Painting Code,Crafting Solution")
path=""
check = StringVar()  #define a variable
check_auto_save = StringVar()

output_visible = False  # Variable to track if output frame is visible

#define commands
#file menu action
def new_file(event=None):

    """event use beacouse in shortcut key press we get some parameter so that parameter catch by event if we not
    use shortcut key so no parameter pass so event is none""" 

    global path
    path = ""   #if we are not null this so he may be contain any path of old path
    root.title("New File")
    code_area.delete(1.0,END)
    output_area.delete(1.0,END)
def open_file(event=None):
    global path
    path = askopenfilename(initialfile='index.py',defaultextension='.py',filetypes=[
        ("Python Files", "*.py"), ("Text Documents", "*.txt"), ("HTML Files", "*.html"), 
        ("Java Files", "*.java"), ("JavaScript Files", "*.js"), ("CSS Files", "*.css")])
    
    if path !="":
        """os.path.basename :- give a file name which we use in title bar """
        root.title(os.path.basename(path))
        """delete is use is some data is write in current so after open command previous data will 
        be remove warna wo bhi aa jaye ga file open karne ke bad (try karne ke liye line ko comment kar ke
        dekh lo)"""
        code_area.delete(1.0,END)
        # file = open(path,"r")
        with open(path,"r") as file:
            data = file.read()
            code_area.insert(1.0,data)
            # file.close()

def save_file(event=None):
    global path
    if path == "":
        save_as()
    else:
        # file = open(path,'w')
        with open(path,'w') as file:
            file.write(code_area.get(1.0,END))
        file.close()


def save_as(event=None):
    global path
    path = asksaveasfilename(initialfile='index',defaultextension='.py',filetypes=[
        ("Python Files", "*.py"), ("Text Documents", "*.txt"), ("HTML Files", "*.html"), 
        ("Java Files", "*.java"), ("JavaScript Files", "*.js"), ("CSS Files", "*.css")])

    if path != "":     #beacouse if user click on cancel in save as popup box we face error 
        with open(path,'w') as file: 
            file.write(code_area.get(1.0,END))
        file.close()

#run menu action
def run(event=None):
        global path
        if path == "":
            messagebox.showerror("Remember", "Please First Save The File")
            save_as()
        else:
            command = f"python {path}"
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            output_area.delete(1.0, END)
            if output:
                output_area.configure(fg='darkblue', bg='lightgreen')
                output_area.insert(1.0, output)
            else:
                output_area.configure(fg='red', bg='yellow')
                output_area.insert(1.0, error)
            toggle_output()  # Show output frame

# Function to toggle visibility of output frame
def toggle_output():
        global output_visible
        if output_visible:
            out_frame.pack_forget()
            toggle_output_button.pack_forget()
            output_visible = False
        else:
            out_frame.pack(fill=X, expand=False)  # Decreased output frame area
            toggle_output_button.pack(side=BOTTOM, fill=BOTH)
            output_visible = True
                         

#create frame for code
#when you use any variable in font so give it in tuple - font_size(variable define in starting point)
code_frame = LabelFrame(root,text="Code",font=('arial',font_size,'bold')) 
code_frame.place(x=0,y=0,height=685,relwidth=1)

#scrollbar for code area
v_scroll_code = Scrollbar(code_frame,orient=VERTICAL)
v_scroll_code.pack(side=RIGHT,fill=Y)

# Create line_numbers Text widget
line_numbers = Text(code_frame, width=0, padx=10, pady=3,wrap="none",font=('arial', font_size),bg='lightgray',fg='brown')
line_numbers.pack(side=LEFT, fill=Y,ipadx=10)

# Create code_area Text widget
code_area = Text(code_frame, font=('arial', font_size), bg='lightgray', padx=5, pady=3, fg='darkblue',
                 yscrollcommand=v_scroll_code.set, wrap="none")
code_area.pack(fill=BOTH, expand=True)

v_scroll_code.config(command=code_area.yview)


#Output Frame
out_frame = LabelFrame(root, text="Output", font='arial 15')

#output scrollbar
v_scroll_out = Scrollbar(out_frame,orient=VERTICAL)
v_scroll_out.pack(side=RIGHT,fill=Y)
output_area = Text(out_frame,font='arial 15',bg='lightgreen',padx=5,pady=3,fg='darkblue',yscrollcommand=v_scroll_out.set)
output_area.pack(fill=BOTH)
v_scroll_out.config(command=output_area.yview)

# Toggle Output button
toggle_output_button = Button(root, text=" Close Output", command=toggle_output, bg='gray', fg='white',
                                 font='arial 14 bold')

# Initially hide the output frame
toggle_output_button.pack_forget()
out_frame.pack_forget()

#end of search and replace implement

#main menu
main_menu = Menu(root)
m1 = Menu(main_menu,tearoff=0)

#File menu
m1.add_command(label="New File    ",command=new_file,accelerator="Ctrl + N")
m1.add_separator()
m1.add_command(label="Open File    ",command=open_file,accelerator="Ctrl + O")
m1.add_separator()
m1.add_command(label="Save    ",command=save_file,accelerator="Ctrl + S")
m1.add_separator()
m1.add_command(label="Save As    ",command=save_as,accelerator="Ctrl + Z")
main_menu.add_cascade(label="File    ",menu=m1)

#run menu
code_run=Menu(main_menu,tearoff=0)
code_run.add_command(label = "Run Python",command=run)

main_menu.add_cascade(label="Run  ",menu=code_run)

root.config(menu=main_menu)


root.mainloop()