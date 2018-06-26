from tkinter import *
from tkinter.filedialog import asksaveasfilename
from tkinter.simpledialog import askstring
from tkinter.messagebox import askokcancel
from tkinter.messagebox import showinfo, showerror, askyesno


################################################################################
class fun():
    def clearAllText(self):
        self.text.delete('1.0', END)

    def onNew(self):
        """
        start editing a new file from scratch in current window;
        see onClone to pop-up a new independent edit window instead;
        """
        if self.text.edit_modified():  # 2.0
            if not askyesno('PyEdit', 'Text has changed: discard changes?'):
                return

        self.clearAllText()
        self.text.edit_reset()  # 2.0: clear undo/redo stks
        self.text.edit_modified(0)  # 2.0: clear modified flag

    def onSave(self):
        filename = asksaveasfilename(defaultextension='.txt',
                                     filetypes=(('Text files', '*.txt'),
                                                ('Python files', '*.py *.pyw'),
                                                ('All files', '*.*')))
        if filename:
            with open(filename, 'w') as stream:
                stream.write(self.gettext())

    def onDelete(self):  # delete selected text, no save
        if not self.text.tag_ranges(SEL):
            showerror('PyEdit', 'No text selected')
        else:
            self.text.delete(SEL_FIRST, SEL_LAST)

    def onCopy(self):  # get text selected by mouse, etc.
        if not self.text.tag_ranges(SEL):  # save in cross-app clipboard
            showerror('PyEdit', 'No text selected')
        else:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)

    def onCut(self):
        if not self.text.tag_ranges(SEL):
            showerror('PyEdit', 'No text selected')
        else:
            self.onCopy()  # save and delete selected text
            self.onDelete()
    def onPaste(self):
        try:
            self.text.insert(INSERT, self.selection_get(selection='CLIPBOARD'))
        except TclError:
            pass

    def onFind(self):
        self.target = askstring('SimpleEditor', 'Search String?',
                                initialvalue=self.target)
        if self.target:
            where = self.text.search(self.target, INSERT, END, nocase=True)
            if where:
                print(where)
                self.text.tag_remove(SEL, '1.0', END)
                pastit = '{}+{}c'.format(where, len(self.target))
                self.text.tag_add(SEL, where, pastit)
                self.text.mark_set(INSERT, pastit)
                self.text.see(INSERT)
                self.text.focus()

    def onUndo(self):
        try:  # tk8.4 keeps undo/redo stacks
            self.text.edit_undo()  # exception if stacks empty
        except TclError:  # menu tear-offs for quick undo
            showinfo('PyEdit', 'Nothing to undo')

    def onRedo(self):  # 2.0: redo an undone
        try:
            self.text.edit_redo()
        except TclError:
            showinfo('PyEdit', 'Nothing to redo')
    def onPickFg(self):
     self.pickColor('fg')


class Menut():
    root = Tk()

    menuM = Menu(root)
    root.configure(menu=menuM)

    fileM = Menu(menuM)
    menuM.add_cascade(label='File', menu=fileM)
    fileM.add_command(label='New',command=fun.onNew)
    fileM.add_command(label='Open...')
    fileM.add_separator()
    fileM.add_command(label='Exit', command=root.destroy)

    editM = Menu(menuM)
    menuM.add_cascade(label='Edit', menu=editM)
    editM.add_command(label='copy')

    viewM = Menu(menuM)
    menuM.add_cascade(label='View', menu=viewM)

    helpM = Menu(menuM)
    menuM.add_cascade(label='Help', menu=helpM)
    helpM.add_command(label='About')

    viewM.add_command(label='Color List', command=fun.onPickFg)


class ScrolledText(Frame):

    def __init__(self, parent=None, text='', file=None):
        super().__init__(parent)
        self.pack(expand=YES, fill=BOTH)
        self.makewidgets()
        self.settext(text, file)

    def makewidgets(self):
        sbar = Scrollbar(self)
        self.text = Text(self, relief=SUNKEN, wrap=WORD)
        sbar['command'] = self.text.yview
        self.text['yscrollcommand'] = sbar.set
        sbar.pack(side=RIGHT, fill=Y)
        self.text.pack(side=LEFT, expand=YES, fill=BOTH)

    def settext(self, text='', file=None):
        if file:
            with open(file, 'r') as stream:
                text = stream.read()
        self.text.delete('1.0', END)
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()

    def gettext(self):
        return self.text.get('1.0', END + '-1c')


class SimpleEditor(ScrolledText,fun):

    def __init__(self, parent=None, file=None):
        frm = Frame(parent)
        frm.pack(fill=X)
        Button(frm, text='New', command=self.onNew).pack(side=LEFT)
        Button(frm, text='Save', command=self.onSave).pack(side=LEFT)
        Button(frm, text='Copy', command=self.onCopy).pack(side=LEFT)
        Button(frm, text='Cut', command=self.onCut).pack(side=LEFT)
        Button(frm, text='Paste', command=self.onPaste).pack(side=LEFT)
        Button(frm, text='Find', command=self.onFind).pack(side=LEFT)
        Button(frm, text='Undo', command=self.onUndo).pack(side=LEFT)
        Button(frm, text='Redo', command=self.onRedo).pack(side=LEFT)
        Quitter(frm).pack(side=LEFT)
        super().__init__(parent, file=file)
        self.text['font'] = 'courier', 9, 'normal'
        self.target = ''




################################################################################


################################################################################

class Quitter(Frame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pack()
        widget = Button(self, text='Quit', command=self.quit)
        widget.pack(expand=YES, fill=BOTH, side=LEFT)

    def quit(self):
        if askokcancel('Verify exit', 'Really quit?'):
            self._root().destroy()


################################################################################

if __name__ == '__main__':
    SimpleEditor(file=sys.argv[1] if len(sys.argv) > 1 else None).mainloop()
