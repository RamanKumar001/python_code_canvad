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
import tkinter as tk
from PIL import Image, ImageTk
import time

def show_image():
    # Define the image path
    image_path = "thumbnail.jpg"  # Replace with the actual path to your image file

    def close_image_window():
        image_window.destroy()

    # Create a new Tkinter window for displaying the image
    image_window = tk.Tk()
    image_window.geometry("800x500")
    image_window.title("CodeCanvas - Painting Code,Crafting Solution")
    image_window.iconphoto(True, tk.PhotoImage(file="D:\Web Development\Python Package\Python Tkinter\Projects\Code Canvas\logo.png"))

    # Remove title bar, minimize, close, and maximize options
    image_window.overrideredirect(True)

    # Load the image using PIL
    img = Image.open(image_path)
    img = img.resize((800, 500))  # Resize the image to fit the window

    # Create a Tkinter-compatible image
    photo = ImageTk.PhotoImage(img)

    # Display the image in a label
    label = tk.Label(image_window, image=photo)
    label.pack()
    
    screen_width = image_window.winfo_screenwidth()
    screen_height = image_window.winfo_screenheight()

    # Calculate the position to center the window
    x_position = (screen_width - 800) // 2  # Assuming image width is 800
    y_position = (screen_height - 500) // 2  # Assuming image height is 500

    # Set the window geometry and position it at the center
    image_window.geometry(f"800x500+{x_position}+{y_position}")
     
    # Close the image window after 5 seconds
    image_window.after(3200, close_image_window)

    # Start the Tkinter event loop
    image_window.mainloop()

def execute_code():
    #deafault font size

    root = Tk()
    root.geometry('1000x500')
    root.minsize(400,650)
    root.title("CodeCanvas - Painting Code,Crafting Solution")
    root.iconphoto(True, PhotoImage(file="D:\Web Development\Python Package\Python Tkinter\Projects\Code Canvas\logo.png"))
    global path
    check = StringVar()  #define a variable
    check_auto_save = StringVar()
    check_auto_save.set("No")
    check.set("Light")

    font_size = 13
    path = ""
    global output_visible 
    output_visible = False# Variable to track if output frame is visible
            
    #use to increase a font using shortcut key which is bind in a last of this page
    def font_increase(event=None):
        global font_size
        font_size+=1
        #without config our change will not go to code area so config in use to change the font= into a real area
        code_area.config(font=('arial',font_size,'bold'))

    def font_decrease(event=None):
        global font_size
        font_size-=1
        #without config our change will not go to code area so config in use to change the font= into a real area
        code_area.config(font=('arial',font_size,'bold'))


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
            # file.close()


    def save_as(event=None):
        global path
        path = asksaveasfilename(initialfile='index',defaultextension='.py',filetypes=[
            ("Python Files", "*.py"), ("Text Documents", "*.txt"), ("HTML Files", "*.html"), 
            ("Java Files", "*.java"), ("JavaScript Files", "*.js"), ("CSS Files", "*.css")])

        if path != "":     #beacouse if user click on cancel in save as popup box we face error 
            with open(path,'w') as file: 
                file.write(code_area.get(1.0,END))
     
    # Function to auto-save the file
    def auto_save():
        global path
        if path and code_area.get(1.0, "end-1c").strip():  # Check if path is not empty and code area has content
            with open(path, 'w') as file:
                file.write(code_area.get(1.0, END))
            root.after(1000, auto_save)  # Auto-save every 1 second (1000 milliseconds)


    # Start auto-save loop
    if check_auto_save.get()=="No":
        pass
    else:
        auto_save()

        
    #for asking a user to save a code or not when you exit
    def on_close():
        result = messagebox.askyesnocancel('Confirm', 'Do You Want To Save The File Before Closing?')
        if result is True:
            save_file()
            root.destroy()
        elif result is False:
            root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)

    #for exit we use
    def exit(event=None):
        result = messagebox.askyesno('Confirm','Do You Want To Exit')
        # it return True and False
        if result == True:
            root.destroy()
        else:
            pass
    #edit menu action
    def cut(event=None):
        code_area.event_generate(("<<Cut>>"))
    def copy(event=None):
        code_area.event_generate(("<<Copy>>"))
    def paste(event=None):
        code_area.event_generate(("<<Paste>>"))


    #theme menu action
    def theme(event=None):
        if check.get()=="Light":
            code_area.configure(bg="lightgray",fg='darkblue')
            code_area.configure(insertbackground="black")
            output_area.configure(bg='lightgreen',fg='darkblue')
            output_area.configure(insertbackground="black")
        if check.get()== "Dark":
            code_area.configure(bg='#333333',fg='white')
            code_area.configure(insertbackground="white")
            output_area.configure(insertbackground="white")
            
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
    
    #clear menu action
    def clear(event=None):
        code_area.delete(1.0,END)
        output_area.delete(1.0,END)

    #help menu action
    def About_us():
        messagebox.showinfo("About Us","This editor is created by Raman Kumar in:\n 19/february/2023")

    def shortcut():
        messagebox.showinfo("All Shortcuts List",
                            '''List of all shortcuts related to CodeCanvas
                            
                            ---------------------- File Menu -----------------------
                            1. New File                                     Ctrl + N
                            2. Open File                                    Ctrl + O
                            3. Auto Save                                    Ctrl + E
                            4. Save                                         Ctrl + S
                            5. Save As                                      Ctrl + Z
                            6. Exit                                         Ctrl + Q
                            
                            ---------------------- Edit Menu -----------------------
                            1. Cut                                          Ctrl + X
                            2. Copy                                         Ctrl + C
                            3. Paste                                        Ctrl + V
                            4. Search and Replace                           Ctrl + P
                            5. Font Increase                                Ctrl + I
                            5. Font Decrease                                Ctrl + D
                            
                            ---------------------- Theme Menu -----------------------
                            1. Light Theme                                  Ctrl + T
                            2. Dark Theme                                   ctrl + T
                            
                            ---------------------- Run Menu ------------------------
                            1. Run Python File                              Ctrl + R
                            2. Run Html File                                Ctrl + H
                            3. Run Java File                                Ctrl + J
                            
                            ---------------------- Clear Menu ----------------------
                            1. Clear file                                   Ctrl + K
                            
                            ---------------------- Help Menu -----------------------
                            1. All Shortcut                                 Ctrl + W
                            2. About Us                                     Ctrl + U''')

    #for give indentaion 

    def auto_indent(event=None):
        current_line = code_area.index(INSERT).split('.')[0]
        current_col = code_area.index(INSERT).split('.')[1]

        line_text = code_area.get(f"{current_line}.0", f"{current_line}.end")

        prev_line = str(int(current_line) - 1)
        prev_line_text = code_area.get(
            f"{prev_line}.0", f"{prev_line}.end")

        # Indentation will be 2 and 2 give by \t spaces regardless of the previous line
        indent_count = 2

        block_end_chars = [':', '{', '[']
        ends_with_block_end = any(
            prev_line_text.rstrip().endswith(char) for char in block_end_chars)

        if ends_with_block_end:
            code_area.insert(INSERT, '  ' + ' ' * indent_count)
            return 'break'
        return None

    # Function to highlight Python keywords
    def highlight_exact_keywords(event=None):
        keywords = keyword.kwlist
        for word in keywords:
            start_index = "1.0"
            while True:
                start_index = code_area.search(fr'\y{word}\y', start_index, stopindex="end", regexp=True)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(word)}c"
                code_area.tag_add("highlight", start_index, end_index)
                start_index = end_index
        
        code_area.tag_config("highlight", foreground="orangered", font=('arial', font_size, 'italic'))

    #function to highlight comment
    def highlight_comments(event=None):
        start_index = "1.0"
        while True:
            start_index = code_area.search("#", start_index, stopindex="end", regexp=True)
            if not start_index:
                break
            end_index = code_area.index(f"{start_index} lineend")
            code_area.tag_add("comment", start_index, end_index)
            start_index = end_index

        code_area.tag_config("comment", foreground="hotpink")


    # Function to display line numbers
    def display_line_numbers(event=None):
        # Clear the current line numbers
        line_numbers.delete(1.0, END)
        
        # Get the current content of the code area
        code_content = code_area.get(1.0, "end-1c")
        
        # Count the number of lines in the content
        line_count = code_content.count('\n') + 1
        
        # Insert line numbers into the line_numbers widget
        for line_number in range(1, line_count + 1):
            line_numbers.insert(END, f"{line_number}\n")
            
    # Create a function to synchronize the line numbers with the code area scrollbar
    def sync_scroll(*args):
        # Get the current position of the code area scrollbar
        code_scroll_position = code_area.yview()[0]
        # Move the line numbers scrollbar to the same position
        line_numbers.yview_moveto(code_scroll_position)
            
    #for run html file on browser
    def run_html(event=None):
        global path
        if path == "":
            messagebox.showerror("Remember", "Please First Save The File")
            save_as()
        else:
            if not path.endswith('.html'):
                messagebox.showerror("Error", "Please save the file with a .html extension")
            else:
                webbrowser.open(path)

    #strat for creating function for search and replace

    # Function to toggle the visibility of search and replace widgets
    def toggle_search_replace(event=None):
        if search_frame.winfo_ismapped():
            search_frame.pack_forget()
        else:
            window_height = root.winfo_height()
            padding = window_height // 3  # Adjust this value as needed
            
            # Place the search frame at the right side and fill half of the window vertically with padding
            search_frame.pack(side="right", fill="y", padx=40, pady=(padding, padding))

    # Function to search for a word in the code
    def search_word():
        search_term = search_entry.get()  # Get the search term from the entry widget
        if search_term:
            code_area.tag_remove("search", "1.0", "end")  # Remove any previous tags
            start_index = "1.0"
            while True:
                start_index = code_area.search(search_term, start_index, stopindex="end", regexp=True)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(search_term)}c"
                code_area.tag_add("search", start_index, end_index)
                start_index = end_index
            code_area.tag_config("search", background="yellow")

    # Function to replace a word in the code
    def replace_word():
        search_term = search_entry.get()
        replace_term = replace_entry.get()
        if search_term and replace_term:
            content = code_area.get("1.0", "end")
            new_content = re.sub(search_term, replace_term, content)
            code_area.delete("1.0", "end")
            code_area.insert("1.0", new_content)

    # Function to clear search tags
    def clear_search_tags():
        code_area.tag_remove("search", "1.0", "end")
        search_entry.delete(0, "end")
        search_entry.focus()
        replace_entry.delete(0,"end")

    #end of creating function for search and replace
            
    # Function to run Java code
    def run_java(event=None):
        global path
        if path == "":
            messagebox.showerror("Remember", "Please First Save The File")
            save_as()
        else:
            if not path.endswith('.java'):
                messagebox.showerror("Error", "Please save the file with a .java extension")
            else:
                # Compile Java file
                compile_command = f"javac {path}"
                compile_process = subprocess.Popen(compile_command, shell=True, stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE)
                compile_output, compile_error = compile_process.communicate()

                if compile_error:
                    output_area.delete(1.0, END)
                    output_area.configure(fg='red', bg='yellow')
                    output_area.insert(1.0, compile_error.decode())
                else:
                    # Run compiled Java file
                    file_name = os.path.splitext(os.path.basename(path))[0]
                    run_command = f"java {file_name}"
                    run_process = subprocess.Popen(run_command, shell=True, stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
                    run_output, run_error = run_process.communicate()

                    output_area.delete(1.0, END)
                    if run_output:
                        output_area.configure(fg='darkblue', bg='lightgreen')
                        output_area.insert(1.0, run_output.decode())
                    else:
                        output_area.configure(fg='red', bg='yellow')
                        output_area.insert(1.0, run_error.decode())
                        

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
    toggle_output_button = Button(root, text="Close Output", command=toggle_output, bg='gray', fg='white',
                                    font='arial 14 bold')
    
     # Initially hide the output frame
    toggle_output_button.pack_forget()
    out_frame.pack_forget()

    # Configure the code area scrollbar to call sync_scroll when moved
    code_area.config(yscrollcommand=lambda *args: (sync_scroll(), v_scroll_code.set(*args)))

    # Call the sync_scroll function initially to synchronize the line numbers
    sync_scroll()

    #start for search and replace implement
    
    # Create a frame for search and replace widgets
    search_frame = Frame(root,bg="#414a4c")

    # Create search and replace widgets
    search_label = Label(search_frame, text="Search:",bg="#414a4c",fg="white",font=('arial',10,'bold'))
    search_label.grid(row=0, column=0,pady=(10, 0))

    search_entry = Entry(search_frame)
    search_entry.grid(row=0, column=1,pady=(10, 0),padx=30)

    replace_label = Label(search_frame, text="Replace:",bg="#414a4c",fg="white",font=('arial',10,'bold'))
    replace_label.grid(row=1, column=0, pady=(10, 0))

    replace_entry = Entry(search_frame)
    replace_entry.grid(row=1, column=1,pady=(10, 0))

    search_button = Button(search_frame, text="Search", command=search_word,bg="lightgreen",fg="darkblue",font=('arial',10,'bold'))
    search_button.grid(row=3, column=1, pady=(10, 0))

    replace_button = Button(search_frame, text="Replace", command=replace_word,bg="lightgreen",fg="darkblue",font=('arial',10,'bold'))
    replace_button.grid(row=4, column=1,pady=(10, 0))

    clear_button = Button(search_frame, text="Clear Search", command=clear_search_tags,bg="lightgreen",fg="darkblue",font=('arial',10,'bold'))
    clear_button.grid(row=5, column=1, pady=(10, 0))

    close_label = Label(search_frame, text="*Close-(Ctrl+P)*",fg="white",bg="#414a4c",font=('arial',12,'bold'))
    close_label.grid(row=6, column=1,pady=(10, 0))

    # Initially hide the search and replace widgets
    search_frame.pack_forget()


    #end of search and replace implement

    #main menu
    main_menu = Menu(root)
    m1 = Menu(main_menu,tearoff=0)

    #File menu
    m1.add_command(label="New File    ",command=new_file,accelerator="Ctrl + N")
    m1.add_separator()
    m1.add_command(label="Open File    ",command=open_file,accelerator="Ctrl + O")
    m1.add_separator()
    m1.add_radiobutton(label='Auto Save',accelerator="Ctrl + E",variable=check_auto_save,value='Yes',command=auto_save)
    m1.add_separator()
    m1.add_command(label="Save    ",command=save_file,accelerator="Ctrl + S")
    m1.add_separator()
    m1.add_command(label="Save As    ",command=save_as,accelerator="Ctrl + Z")
    m1.add_separator()
    m1.add_command(label="Exit    ",command=exit,accelerator="Ctrl + Q")
    main_menu.add_cascade(label="File    ",menu=m1)

    #edit menu
    m2 = Menu(main_menu,tearoff=0)
    m2.add_command(label="Cut          ",command=cut,accelerator="Ctrl + x")
    m2.add_separator()
    m2.add_command(label="Copy          ",command=copy,accelerator="Ctrl + C")
    m2.add_separator()
    m2.add_command(label="Paste         ",command=paste,accelerator="Ctrl + V")
    m2.add_separator()
    m2.add_command(label="Search and Replace", command=toggle_search_replace,accelerator="Ctrl + p") 
    m2.add_separator()
    m2.add_command(label="Font Increase  ",command=font_increase,accelerator="Ctrl + i")
    m2.add_separator()
    m2.add_command(label="Font decrease  ",command=font_decrease,accelerator="Ctrl + d")
    main_menu.add_cascade(label="Edit    ",menu=m2)

    #theme menu
    theme_menu = Menu(main_menu,tearoff=False)

    theme_menu.add_radiobutton(label='Dark',accelerator="Ctrl + t",variable=check,value='Dark',command=theme) #check variable store only light and dark
    theme_menu.add_radiobutton(label='Light',accelerator="Ctrl + t",variable=check,value='Light',command=theme)
    main_menu.add_cascade(label="Theme    ",menu=theme_menu)

    #run menu
    code_run=Menu(main_menu,tearoff=0)
    code_run.add_command(label = "Run Python",command=run,accelerator='Ctrl + r')
    # code_run.add_command(label = "Run Java ",command=run_java,accelerator='Ctrl + j')
    code_run.add_command(label = "Run Html ",command=run_html,accelerator='Ctrl + h')
    main_menu.add_cascade(label="Run  ",menu=code_run)

    #clear
    main_menu.add_command(label="Clear    ",command=clear,accelerator="Ctrl + k")


    #help menu
    m3 = Menu(main_menu,tearoff=0)
    m3.add_cascade(label='All Shortcut      ',command=shortcut,accelerator="Ctrl + w")
    m3.add_command(label='About Us          ',command=About_us,accelerator="Ctrl + u")
    main_menu.add_cascade(label='Help       ',menu=m3)

    root.config(menu=main_menu)


    #we are using bind to connect a shortcut keys
    #file option shortcut keys
    root.bind("<Control-n>",new_file)
    root.bind("<Control-o>",open_file)
    root.bind("<Control-e>",auto_save)
    root.bind("<Control-s>",save_file)
    root.bind("<Control-z>",save_as)
    root.bind("<Control-q>",exit)

    #edit menu
    root.bind("<Control-x>",cut)
    root.bind("<Control-c>",copy)

    #for run shortcut key
    root.bind("<Control-r>",run)

    #for clear shortcut key
    root.bind("<Control-k>",clear)

    #for increase
    root.bind("<Control-i>",font_increase)
    root.bind("<Control-d>",font_decrease)

    #for call indent function
    root.bind("<Return>", auto_indent)

    #for keyword color
    root.bind("<KeyRelease>", highlight_exact_keywords)

    #for comment color
    code_area.bind("<KeyRelease>", highlight_comments)

    # Call the function initially to display line numbers
    code_area.bind("<KeyPress>", display_line_numbers)

    # Bind the shortcut key for running HTML
    root.bind("<Control-h>", run_html)

    #to open search and replace 
    root.bind("<Control-p>",toggle_search_replace)

    #for all shortcut
    root.bind("<Control-w>",shortcut)

    #for about us
    root.bind("<Control-u>",About_us)

    root.mainloop()

# Display the image for 5 seconds
show_image()

# Wait for 5 seconds before executing the code
time.sleep(0)

# Execute the code
execute_code()
