from tkinter import *
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename,asksaveasfilename
import os
import subprocess
import webbrowser
import re  #use in search and replace
from PIL import Image, ImageTk
import time
import many_help

font_size = 13

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
    pass

def execute_code():
    #deafault font size

    root = Tk()
    root.geometry('1000x500')
    root.minsize(400,650)
    root.title("CodeCanvas - Painting Code,Crafting Solution")
    root.iconphoto(True, PhotoImage(file="logo.png"))
    global path
    check = StringVar()  #define a variable
    check_auto_save = StringVar()
    check_auto_save.set("No")
    check.set("Light")
    path = ""
    global output_visible 
    output_visible = False
    # Variable to track if output frame is visible

    # def install_py():
    #     messagebox.showinfo("Python Install","For run this code editor you need to install python in your system.")

    def check_dependencies():
        required_packages = ['tkinter', 'os', 'subprocess','keyword','builtins','webbrowser','re','PIL','time','importlib','sys']  # List of required packages
        missing_packages = []

        try:
            import importlib.util  # Check if importlib.util is available
            for package in required_packages:
                if not importlib.util.find_spec(package):
                    missing_packages.append(package)
        except AttributeError:
            # Fallback for older Python versions without importlib.util
            import importlib
            for package in required_packages:
                try:
                    importlib.import_module(package)
                except ImportError:
                    missing_packages.append(package)
        if missing_packages:
            messagebox.showinfo("Dependencies Missing", "Please ensure your internet connection is active for installing dependencies.")
            subprocess.Popen(["pip", "install"] + missing_packages, shell=True)  # Install missing packages
                
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
                file.close()

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
        path = asksaveasfilename(initialfile='index', defaultextension='.py', filetypes=[
            ("Python Files", "*.py"), ("Text Documents", "*.txt"), ("All Files", "*.*")])

        if path != "":
            # Check if the 'code canvas' folder exists on the desktop, if not, create it
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            code_canvas_path = os.path.join(desktop_path, "code_canvas")
            if not os.path.exists(code_canvas_path):
                os.mkdir(code_canvas_path)

            # Define the mapping of extensions to folder names
            extension_folders = {
                ".html": "html",
                ".py": "python",
                ".css": "css",
                ".js": "javascript",
                ".txt": "text",
                ".java": "java"
                # Add more extensions and corresponding folder names as needed
            }

            # Get the extension of the file being saved
            _, file_extension = os.path.splitext(path)

            # Check if the extension is mapped to a folder
            if file_extension in extension_folders:
                # Create the folder if it doesn't exist in 'code canvas' folder
                file_folder = os.path.join(code_canvas_path, extension_folders[file_extension])
                if not os.path.exists(file_folder):
                    os.mkdir(file_folder)

                # Save the file in the corresponding folder within 'code canvas' folder
                file_path = os.path.join(file_folder, os.path.basename(path))
                with open(file_path, 'w') as file:
                    file.write(code_area.get(1.0, END))
            else:
                messagebox.showerror("Error", "Unsupported file extension.")

            # Update the title of the main window with the saved file path
            root.title(path)
     
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
        display_line_numbers()


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

    #run python file
    def run_python(event=None):
        global path
        if path == "":
            messagebox.showerror("Remember", "Please First Save The File")
            save_as()
        else:
            # Ensure the path is correctly set to include the code_canvas and python folders
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            code_canvas_path = os.path.join(desktop_path, "code_canvas", "python")
            
            # Update path to reflect the correct location if it's not already in the code_canvas/python directory
            if not path.startswith(code_canvas_path):
                path = os.path.join(code_canvas_path, os.path.basename(path))

            # Ensure the path is correctly quoted to handle spaces
            quoted_path = f'"{path}"'
            command = f"python {quoted_path}"
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
                            5. Format Document                              Ctrl + F
                            5. Font Increase                                Ctrl + I
                            5. Font Decrease                                Ctrl + D
                            6. Set Font Size                                --------
                            7. Import Code                                  Ctrl + m
                            
                                        ------- Theme Menu -----
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
                            2. About Us                                     Ctrl + U
                            
                            ---------------------- Additional -----------------------
                            1.HTML Boilerplate                            ! (Shift+1)
                            '''
    )

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
        data = many_help.all_words
        for word in data:
            start_index = "1.0"
            while True:
                start_index = code_area.search(fr'\y{word}\y', start_index, stopindex="end", regexp=True)
                if not start_index:
                    break
                # Check if the word is not enclosed in double or single quotes
                line_start, col_start = map(int, start_index.split('.'))
                line_end, col_end = line_start, col_start + len(word)
                line_text = code_area.get(f"{line_start}.{col_start-1}", f"{line_end}.{col_end+1}")
                if not (line_text.startswith('"') and line_text.endswith('"')) and not (line_text.startswith("'") and line_text.endswith("'")):
                    end_index = f"{start_index}+{len(word)}c"
                    code_area.tag_add("highlight_html", start_index, end_index)
                    code_area.tag_config("highlight_html", foreground="crimson", font=('arial', font_size,'italic'))
                    start_index = end_index  # Move this line inside the if condition
                else:
                    start_index = f"{start_index}+1c"  # Move to the next character if word is in quotes
                    
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
                messagebox.showerror("Find JDK","For run java file first you need to install jdk.")
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
                #function for right-click on mouse window show
    #function for right-click on mouse window show
    def show_context_menu(event=None):
        context_menu = Menu(root, tearoff=0,bg='lightgray',fg='darkred',font=('Cambria',9,'bold'))

        # Create a submenu for Paste with more options
        run_submenu = Menu(context_menu, tearoff=0,bg='lightgray',fg='darkred',font=('Cambria',9,'bold'))
        run_submenu.add_command(label="Run Python",command=run_python)
        run_submenu.add_separator()
        run_submenu.add_command(label="Run Java",command=run_java)
        run_submenu.add_separator()
        run_submenu.add_command(label="Run Html",command=run_html)

        # Add the submenu to the Paste option
        context_menu.add_command(label="Save File     ",command=save_file)
        context_menu.add_separator()
        context_menu.add_cascade(label="Run File  ", menu=run_submenu)
        context_menu.add_separator()
        # Add other options to the context menu
        context_menu.add_command(label="Format Document",command=format_code)
        context_menu.add_separator()
        context_menu.add_command(label="Search & Replace",command=toggle_search_replace)
        context_menu.add_separator()
        context_menu.add_command(label="Clear File",command=clear)
        context_menu.add_separator()
        context_menu.add_command(label="All Shortcuts",command=shortcut)

        # Post the context menu at the cursor's position
        context_menu.post(event.x_root, event.y_root)

    # Function to format code
    def format_code(event=None):
        code = code_area.get(1.0, END)
        formatted_code = ""

        # Replace tabs with 4 spaces
        code = code.replace('\t', ' ' * 4)

        # Use regular expressions to add proper Python indentation
        indent_level = 0
        for line in code.splitlines():
            line = line.strip()
            if line:  # Ignore empty lines
                if line.endswith((":", "(", "[", "{")):
                    formatted_code += ' ' * (indent_level * 4) + line + '\n'
                    indent_level += 1
                elif line.startswith(("}", "]", ")")):
                    indent_level -= 1
                    formatted_code += ' ' * (indent_level * 4) + line + '\n'
                else:
                    formatted_code += ' ' * (indent_level * 4) + line + '\n'
            else:
                formatted_code += '\n'

        code_area.delete(1.0, END)
        code_area.insert(1.0, formatted_code.strip())

    def set_font_size(event=None):
        global font_size
        # Create a new window for setting font size
        font_size_window = Toplevel(root)
        font_size_window.geometry("300x100")
        font_size_window.title("Set Font Size")
        
        # Label and Entry for entering font size
        Label(font_size_window, text="Enter Font Size:").pack()
        font_size_entry = Entry(font_size_window)
        font_size_entry.pack()
        
        # OK and Cancel buttons
        def set_size(event=None):
            try:
                new_font_size = int(font_size_entry.get())
                if new_font_size > 0:
                    font_size = new_font_size
                    messagebox.showinfo("Success", f"Font Size set to {font_size}")
                    font_size_window.destroy()
                    
                    # Update the font size of the code area and output area
                    code_area.config(font=('arial', font_size))
                    output_area.config(font=('arial', font_size))
                else:
                    messagebox.showerror("Error", "Please enter a positive integer for font size.")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer for font size.")
        
        ok_button = Button(font_size_window, text="OK", command=set_size)
        ok_button.pack()
        
        cancel_button = Button(font_size_window, text="Cancel", command=font_size_window.destroy)
        cancel_button.pack()

    #add importing code 
    def code_help(event=None):
    # Create a new window for code help
        code_help_window = Toplevel(root)
        code_help_window.geometry("250x150")
        code_help_window.title("Import Code")
        code_help_window.config(bg="#414a4c")

        # Label and Entry for searching code
        Label(code_help_window, text="Enter Function Name:",bg="#414a4c",fg="White",font=('arial',font_size,'bold')).pack(pady=5)
        function_name_entry = Entry(code_help_window)
        function_name_entry.pack()

        # Import and Cancel buttons
        def import_code():
            function_name = function_name_entry.get()
            if function_name:
                try:
                    with open('many_help.py', 'r') as file:
                        lines = file.readlines()
                        start_index = -1
                        end_index = -1
                        in_function = False
                        for i, line in enumerate(lines):
                            if line.strip().startswith(f'def {function_name}('):
                                start_index = i + 1
                                in_function = True
                            elif in_function and line.strip() == "":
                                end_index = i
                                break
                        
                        if start_index != -1 and end_index != -1:
                            function_code = "".join(lines[start_index:end_index])
                            # Remove four spaces from each line
                            function_code_stripped = "\n".join(line[4:] if len(line) > 4 else line for line in function_code.split("\n"))
                            # Append the code to the editor
                            code_area.insert(END, function_code_stripped)
                            # Highlight exact keywords after importing code
                            highlight_exact_keywords()
                            highlight_comments()
                            display_line_numbers()
                        else:
                            messagebox.showerror("Error", f"Function '{function_name}' not found see the import function names.")
                except FileNotFoundError:
                    messagebox.showerror("Error", "File 'many_help.py' not found.")
            else:
                messagebox.showerror("Error", "Please enter a function name.")
        
        import_button = Button(code_help_window, text="Import", command=import_code,bg='lightgreen',fg='darkblue',font=('arial',10,'bold'))
        import_button.pack(pady=5)

        cancel_button = Button(code_help_window, text="Cancel", command=code_help_window.destroy,bg='lightgreen',fg='darkblue',font=('arial',10,'bold'))
        cancel_button.pack(pady=5)
    def insert_html_boilerplate(event=None):
        if path and path.endswith('.html'):
            html_boilerplate = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        
    </body>
</html>"""
            code_area.insert(END, html_boilerplate)
            display_line_numbers()
        else:
            messagebox.showinfo("Information", "HTML boilerplate can only be inserted in HTML files.")

    check_dependencies()  # Check and install dependencies
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
    m1.add_radiobutton(label='Auto Save',accelerator="None",variable=check_auto_save,value='Yes',command=auto_save)
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
    m2.add_command(label="Format Code", command=format_code,accelerator="Ctrl + f")
    m2.add_separator()
    m2.add_command(label="Font Increase  ",command=font_increase,accelerator="Ctrl + i")
    m2.add_separator()
    m2.add_command(label="Font decrease  ",command=font_decrease,accelerator="Ctrl + d")
    m2.add_separator()
    m2.add_command(label="Set Font Size  ",command=set_font_size)
    m2.add_separator()
    m2.add_command(label="Import Code  ",command=code_help,accelerator="Ctrl + Shift + h")
    main_menu.add_cascade(label="Edit    ",menu=m2)

    #theme menu
    theme_menu = Menu(main_menu,tearoff=False)

    theme_menu.add_radiobutton(label='Dark',accelerator="Ctrl + t",variable=check,value='Dark',command=theme) #check variable store only light and dark
    theme_menu.add_radiobutton(label='Light',accelerator="Ctrl + t",variable=check,value='Light',command=theme)
    main_menu.add_cascade(label="Theme    ",menu=theme_menu)

    #run menu
    code_run=Menu(main_menu,tearoff=0)
    code_run.add_command(label = "Run Python",command=run_python,accelerator='Ctrl + r')
    code_run.add_command(label = "Run Java ",command=run_java,accelerator='Ctrl + j')
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
    root.bind("<Control-v>", paste)

    #for run shortcut key
    root.bind("<Control-r>",run_python)

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

    #for right-click bind
    code_area.bind("<Button-3>", show_context_menu)

    #for importing code
    root.bind("<Control-m>", code_help)

    #for html boilerplate
    root.bind("!", insert_html_boilerplate)
    #show msg to install python 

    root.mainloop()

# Display the image for 5 seconds
show_image()
# Wait for 5 seconds before executing the code
time.sleep(0)
# Execute the code
execute_code()
