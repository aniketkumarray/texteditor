#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
from tkinter import *
from tkinter import PhotoImage, messagebox,mainloop, Toplevel, Tk, Text, Menu, IntVar, Entry, TclError, SEL, INSERT, END, NONE, WORD, TOP, RAISED, SUNKEN, HORIZONTAL, E, W, N, S, X, BOTTOM, BOTH, LEFT
from tkinter.ttk import  Frame, Scrollbar, Button, Label,Checkbutton
from tkinter.filedialog import askopenfile
from tkinter.messagebox import showinfo, showerror
from tkinter.simpledialog import askstring
try:
    import textConfig                        # startup font and colors
    configs = textConfig.__dict__            # work if not on the path or bad
except:                                      # define in client app directory
    configs = {}
TITLE = "Aniket Text Editor"
top = Tk()
if "nt" == os.name:
    top.wm_iconbitmap(bitmap="Notepad.ico")  # top.wm_iconbitmap("Notepad.ico")
else:
    try:
        img = PhotoImage(file='notepad.gif')
        top.tk.call('wm', 'iconphoto', top._w, img)
    except:
        pass
filename = None
key_word = ""

frame = Frame(top, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
yscrollbar = Scrollbar(frame)
yscrollbar.grid(row=0, column=1, sticky=N + S)

# text widget
editor = Text(frame, wrap=NONE,
              yscrollcommand=yscrollbar.set)
editor.focus_set()
editor.grid(row=0, column=0, sticky=N + S + E + W)
editor.config(wrap=WORD,  # use word wrapping
              undo=True,  # Tk 8.4
              width=64)

yscrollbar.config(command=editor.yview)


class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()


statusbar = StatusBar(frame)
statusbar.grid(row=2, column=1, columnspan=2, sticky=E + W)
frame.pack(side=BOTTOM, fill=BOTH, expand=1)


def set_title(local_filename=None):
    if local_filename == None:
        top.wm_title("Untitled" + " - " + TITLE)
    else:
        top.wm_title(os.path.basename(local_filename) + " - " + TITLE)


set_title(filename)


# toolbar commands
def br(event=None):
    editor.insert(INSERT, "<br />")


def ins_br():
    try:
        editor.delete(SEL)
    except:
        print('exception in function: ins_br')
    br()
    return 'break'


def indent(event=None):
    index = editor.index(INSERT).split(".")
    line_no = int(index[0])
    line_text = editor.get("%d.%d" % (line_no, 0), "%d.end" % (line_no))
    text_only = line_text.lstrip(" ")
    no_of_spaces = len(line_text) - len(text_only)
    spaces = "\n" + " " * no_of_spaces
    editor.insert(INSERT, spaces)
    return 'break'


def indent_and_br(event=None):
    ins_br()
    indent()
    return 'break'



def save_if_modified():
    print("save_if_modified() editor.edit_modified()", editor.edit_modified())
    if editor.edit_modified():
        from tkinter.messagebox import askyesnocancel
        response = askyesnocancel(TITLE,
                                  "This document has been modified. Do you want to save changes?")  # cancel = none, no = false, yes = true
        print("Response: ", response)
        if response:
            cancelled = save()
            print("Cancelled: ", response)
            if cancelled == 1:
                return None
            elif cancelled == 0:
                return response
        else:
            return response
    else:
        return 0


def save():  # local_filename = filename):
    local_filename = filename
    if local_filename:
        cancelled = save_as(local_filename)
    else:
        cancelled = save_as()
    return cancelled


def save_as(local_filename=None):
    if local_filename == None:
        from tkinter.filedialog import asksaveasfilename
        local_filename = asksaveasfilename(filetypes=(
        ('Text files', '*.txt'), ('Python files', '*.py *.pyw'), ('All files', '*.*')))  # defaultextension='.txt',
    try:
        with open(local_filename, 'wb') as f:
            text = editor.get(1.0, END)
            f.write(bytes(text, 'UTF-8'))
            # f.write("\n") # normalize trailing whitespace
            editor.edit_modified(False)
            set_title(local_filename)
            return 0
    except FileNotFoundError:
        print('FileNotFoundError')
        return 1


# file menu functions
def file_new(event=None):
    response = save_if_modified()
    if response != None:
        editor.delete(1.0, END)
        editor.edit_modified(False)
        global filename
        filename = None
        set_title()
        editor.edit_reset()


def file_open(event=None, local_filename=None):
    response = save_if_modified()
    if response != None:
        # Returns the opened file
        if local_filename == None:
            from tkinter.filedialog import askopenfilename
            local_filename = askopenfilename()
        if local_filename != None and local_filename != '':
            with open(local_filename, 'rb') as f:
                fileContents = f.read()  # Get all the text from file.
            # Set current text to file contents
            editor.delete(1.0, END)
            editor.insert(1.0, fileContents)
            editor.edit_modified(False)
            set_title(local_filename)
        global filename
        filename = local_filename
        return 'break'


if len(sys.argv) > 1:
    filename = sys.argv[1]
    file_open(local_filename=filename)


def file_save(event=None):
    save()


def file_save_as(event=None):
    save_as()


def file_quit(event=None):
    close()  # sys.exit(0)


# edit menu functions
def edit_copy(event=None):
    print('rs.get()=', rs.get())
    if rs.get() == 1:
        editor.clipboard_clear()
        clipped_text = rect_sel_end()
        print('clipped_text=', clipped_text)
        editor.clipboard_append(clipped_text)
    else:
        try:
            editor.clipboard_clear()
            clipped_text = editor.get("sel.first", "sel.last")
            editor.clipboard_append(clipped_text)
        except TclError:
            pass
    return 'break'


def edit_cut(event=None):
    edit_copy()
    edit_delete()


def edit_paste(event=None):
    try:
        clipped_text = editor.selection_get(selection='CLIPBOARD')
        editor.insert('insert', clipped_text)
    except:
        pass
    return 'break'


def edit_delete(event=None):
    if rs.get() == 0:
        clipped_text = rect_sel_end()
        if clipped_text != None:
            rect_sel_end(delete=1)
            return 'break'


def edit_select_all(event=None):
    editor.tag_add(SEL, "1.0", END)
    editor.mark_set(INSERT, "1.0")
    editor.see(INSERT)
    return 'break'


def edit_find(event=None):
    search_toplevel = Toplevel(frame)
    search_toplevel.title('Find Text')
    search_toplevel.transient(frame)

    Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')

    search_entry_widget = Entry(
        search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(
        row=1, column=1, sticky='e', padx=2, pady=2)
    Button(search_toplevel, text="Find All", underline=0,
           command=lambda: search_output(
               search_entry_widget.get(), ignore_case_value.get(),
               editor, search_toplevel, search_entry_widget)
           ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

    def close_search_window():
        editor.tag_remove('match', '1.0', END)
        search_toplevel.destroy()

    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    return "break"


def search_output(needle, if_ignore_case, content_text,
                  search_toplevel, search_box):
    content_text.tag_remove('match', '1.0', END)
    matches_found = 0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(needle, start_pos,
                                            nocase=if_ignore_case, stopindex=END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(needle))
            content_text.tag_add('match', start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
        content_text.tag_config(
            'match', foreground='red', background='yellow')
    search_box.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))


def edit_goto(event=None):
    from tkinter.simpledialog import askinteger
    line = askinteger('Goto', 'Enter line number:')
    editor.update()
    editor.focus()
    if line is not None:
        maxindex = editor.index(END + '-1c')
        maxline = int(maxindex.split('.')[0])
        if line > 0 and line <= maxline:
            editor.mark_set(INSERT, '%d.0' % line)  # goto line
            editor.tag_remove(SEL, '1.0', END)  # delete selects
            editor.tag_add(SEL, INSERT, 'insert + 1l')  # select line
            editor.text.see(INSERT)  # scroll to line
        else:
            from tkinter.messagebox import showerror
            showerror('PyEdit', 'Bad line number')



def close():
    response = save_if_modified()
    if response != None:  # None = Cancel save before new/open/quit confirmation, True = Save and quit, False = Quit without saving
        top.destroy()  # sys.exit(0)


def fn():
    print(editor.edit_modified())


# toolbar
toolbar = Frame(top, relief=RAISED)
toolbar.pack(side=TOP, fill=X)
newbtn=PhotoImage(file='newfile.png')
new = Button(toolbar, image=newbtn, command=file_new)
new.image=newbtn
new.pack(side=LEFT)
savebtn=PhotoImage(file='save.png')
save = Button(toolbar, image=savebtn, command=save)
save.image = savebtn
save.pack(side=LEFT)
copybtn = PhotoImage(file='copy.png')
copy = Button(toolbar, image=copybtn, command=edit_copy)
copy.image = copybtn
copy.pack(side=LEFT)
cutbtn = PhotoImage(file='scissors.png')
cut = Button(toolbar, image=cutbtn, command=edit_cut)
cut.image = cutbtn
cut.pack(side=LEFT)
pastebtn = PhotoImage(file='paste.png')
paste = Button(toolbar, image=pastebtn, command=edit_paste)
paste.image = pastebtn
paste.pack(side=LEFT)
findbtn = PhotoImage(file='find.png')
find = Button(toolbar, image=findbtn, command=edit_find)
find.image = findbtn
find.pack(side=LEFT)
undobtn = PhotoImage(file='undo.png')
undo = Button(toolbar, image=undobtn, command=editor.edit_undo)
undo.image = undobtn
undo.pack(side=LEFT)
redobtn = PhotoImage(file='redo.png')
redo = Button(toolbar, image=redobtn, command=editor.edit_redo)
redo.image = redobtn
redo.pack(side=LEFT)
quitbtn = PhotoImage(file='close.png')
closeb = Button(toolbar, image=quitbtn, command=close)
closeb.image = quitbtn
closeb.pack(side=LEFT)




def rect_sel_end(event=None, delete=0):
    try:
        start_index = editor.index("sel.first").split(".")
        end_index = editor.index("sel.last").split(".")
        start_line = int(start_index[0])
        start_char = int(start_index[1])
        end_line = int(end_index[0])
        end_char = int(end_index[1])
        text = ""
        counter = 0
        no_of_lines = end_line - start_line + 1
        while no_of_lines > 0:
            start_rect_sel = str(start_line + counter) + "." + str(start_char)
            end_rect_sel = str(start_line + counter) + "." + str(end_char)
            if delete == 1:
                editor.delete(start_rect_sel, end_rect_sel)
            else:
                text = text + editor.get(start_rect_sel, end_rect_sel) + "\n"
            counter = counter + 1
            no_of_lines = no_of_lines - 1
        return text
    except TclError:
        editor.tag_delete("selection")
        editor.mark_set("insert", INSERT)


rs = IntVar()

# other functions
def hello():
    messagebox.showinfo("Ok!")


# instead of closing the window, execute a function
top.protocol("WM_DELETE_WINDOW", close)

# create a top level menu
menubar = Menu(top)
# Menu item File
filemenu = Menu(menubar, tearoff=0)  # tearoff = 0 => can't be seperated from window
filemenu.add_command(label="New", underline=1, command=file_new, accelerator="Ctrl+N")
filemenu.add_command(label="Open...", underline=1, command=file_open, accelerator="Ctrl+O")
filemenu.add_command(label="Save", underline=1, command=file_save, accelerator="Ctrl+S")
filemenu.add_command(label="Save As...", underline=5, command=file_save_as, accelerator="Ctrl+Alt+S")
filemenu.add_separator()
filemenu.add_command(label="Exit", underline=2, command=file_quit, accelerator="Alt+F4")
menubar.add_cascade(label="File", underline=0, menu=filemenu)
# Menu item Edit
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", underline=0, command=editor.edit_undo, accelerator="Ctrl+Z")
editmenu.add_command(label="Redo", underline=0, command=editor.edit_redo, accelerator="Ctrl+Y")
editmenu.add_separator()
editmenu.add_command(label="Cut", underline=2, command=edit_cut, accelerator="Ctrl+X")
editmenu.add_command(label="Copy", underline=0, command=edit_copy, accelerator="Ctrl+C")
editmenu.add_command(label="Paste", underline=0, command=edit_paste, accelerator="Ctrl+V")
editmenu.add_command(label="Delete", underline=2, command=edit_delete, accelerator="Del")
editmenu.add_separator()
editmenu.add_command(label="Find...", underline=0, command=edit_find, accelerator="Ctrl+F")
editmenu.add_command(label="Find Next", underline=6, command=hello, accelerator="F3")
editmenu.add_command(label="Replace...", underline=0, command=hello, accelerator="Ctrl+H")
editmenu.add_command(label="Go To...", underline=0, command=edit_goto, accelerator="Ctrl+G")
editmenu.add_separator()
editmenu.add_command(label="Select All", command=edit_select_all, accelerator="Ctrl+A")
editmenu.add_command(label="Time/Date", command=hello, accelerator="F5")
menubar.add_cascade(label="Edit", underline=0, menu=editmenu)
# Menu item Format
formatmenu = Menu(menubar, tearoff=0)
formatmenu.add_command(label="Word Wrap", command=hello)
formatmenu.add_command(label="Font...", command=hello)
menubar.add_cascade(label="Format", underline=1, menu=formatmenu)
# Menu item View
viewmenu = Menu(menubar, tearoff=0)
viewmenu.add_command(label="Status Bar", command=hello)
menubar.add_cascade(label="View", underline=0, menu=viewmenu)
# Menu item Help
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Manual", command=hello)
helpmenu.add_command(label="About", command=hello)
menubar.add_cascade(label="Help", underline=0, menu=helpmenu)
# display the menu
top.config(menu=menubar)
# create keyboard shortcuts for functions
editor.bind("<Control-n>", file_new)
editor.bind("<Control-o>", file_open)
editor.bind("<Control-s>", file_save)
editor.bind("<Control-Shift-s>", file_save_as)
editor.bind("<Control-q>", file_quit)
editor.bind("<Control-N>", file_new)
editor.bind("<Control-O>", file_open)
editor.bind("<Control-S>", file_save)
editor.bind("<Control-Shift-S>", file_save_as)
editor.bind("<Control-Q>", file_quit)
editor.bind("<Control-a>", edit_select_all)
editor.bind("<Control-A>", edit_select_all)
editor.bind("<Control-f>", edit_find)
editor.bind("<Control-F>", edit_find)
editor.bind("<Control-C>", edit_copy)
editor.bind("<Control-c>", edit_copy)
editor.bind("<Control-V>", edit_paste)
editor.bind("<Control-v>", edit_paste)
editor.bind("<Control-X>", edit_cut)
editor.bind("<Control-x>", edit_cut)
editor.bind("<BackSpace>", edit_delete)
editor.bind("<Delete>", edit_delete)
editor.bind("<Control-G>", edit_goto)
editor.bind("<Control-g>", edit_goto)

# context menu
cmenu = Menu(top, tearoff=0)
cmenu.add_command(label="Undo", command=editor.edit_undo)
cmenu.add_separator()
cmenu.add_command(label="Cut", command=edit_cut)
cmenu.add_command(label="Copy", command=edit_copy)
cmenu.add_command(label="Paste", command=edit_paste)
cmenu.add_command(label="Delete", command=edit_delete)
cmenu.add_separator()
cmenu.add_command(label="Select all", command=edit_select_all)
cmenu.add_separator()
cmenu.add_command(label="Exit", command=file_quit)


def context_menu(event):
    cmenu.post(event.x_root, event.y_root)


editor.bind("<Button-3>", context_menu)

mainloop()
