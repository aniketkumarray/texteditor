import sys
from tkinter import *

root = Tk(  )

# Insert a menu bar on the main window
menubar = Menu(root)
root.config(menu=menubar)

# Create a menu button labeled "File" that brings up a menu
filemenu = Menu(menubar)
menubar.add_cascade(label='File', menu=filemenu)

# Create entries in the "File" menu
# simulated command functions that we want to invoke from our menus
def doPrint(  ): print('doPrint')
def doSave(  ): print ('doSave')
filemenu.add_command(label='Print', command=doPrint)
filemenu.add_command(label='Save', command=doSave)
filemenu.add_separator(  )
filemenu.add_command(label='Quit', command=sys.exit)

root.mainloop(  )

newbtn = PhotoImage(file='newfile.png')
new = Button(frm, image=newbtn, command=self.onNew)
new.image = newbtn
new.pack(side=LEFT)
savebtn = PhotoImage(file='save.png')
save = Button(frm, image=savebtn, command=self.onSave)
save.image = savebtn
save.pack(side=LEFT)
copybtn = PhotoImage(file='copy.png')
copy = Button(frm, image=copybtn, command=self.onCopy)
copy.image = copybtn
copy.pack(side=LEFT)
cutbtn = PhotoImage(file='scissors.png')
cut = Button(frm, image=cutbtn, command=self.onCut)
cut.image = cutbtn
cut.pack(side=LEFT)
pastebtn = PhotoImage(file='paste.png')
paste = Button(frm, image=pastebtn, command=self.onPaste())
paste.image = pastebtn
paste.pack(side=LEFT)