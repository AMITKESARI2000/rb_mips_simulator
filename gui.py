from tkinter import *
from tkinter.messagebox import showinfo
import simu

simu.rm_cmnts()

root = Tk()


#root.resizable(width=False, height=False) #Restricting Resizable
root.title("rb mips simulator 😎")
# Panel
simulator_body = PanedWindow(orient=VERTICAL, width=1000, height=500, bg="black")
simulator_body.pack(fill=BOTH, expand = 1)

# Head Panel
head_panel = PanedWindow(simulator_body, bd=1, relief="raised", bg="black")
simulator_body.add(head_panel)

head = Label(head_panel, text="SIMULATOR", font=("Arial", 13))
head_panel.add(head)

# Execution Panel
step_exe = Button(text="Step By Step Execution", bg="red", fg="white", command=lambda: showinfo("Message", "STILL IN PROGRESS!!!")).pack(side=LEFT)
space1 = Button(text="      ", bg="white").pack(side=LEFT)
once_exe = Button(text="At Once Execution", bg="blue", fg="white", command=lambda: modify_gui_data()).pack(side=LEFT)
space2 = Button(text="      ", bg="white").pack(side=LEFT)
console_button = Button(text="Upload a file", bg="green", fg="white", command=lambda: showinfo("Message", "STILL IN PROGRESS!!!")).pack(side=LEFT)

# Body Panel
body_panel = PanedWindow(simulator_body, orient=HORIZONTAL, relief="raised", bg="black")
simulator_body.add(body_panel)

# Register Panel
reg_panel = PanedWindow(body_panel, orient=VERTICAL, bd=1, relief="raised", bg="black")
body_panel.add(reg_panel)

# Memory Panel
mem_panel = PanedWindow(body_panel, orient=VERTICAL,  bd=1, relief="raised", bg="black")
body_panel.add(mem_panel)

# User Text Panel
user_panel = PanedWindow(body_panel, orient=VERTICAL,  bd=1, relief="raised", bg="black")
body_panel.add(user_panel)

# Head Panel of Register and Memory and User
reg_head = PanedWindow(reg_panel, bd=1, relief="raised")
mem_head = PanedWindow(mem_panel, bd=1, relief="raised")
user_head = PanedWindow(user_panel, bd=1, relief="raised")
reg_panel.add(reg_head)
mem_panel.add(mem_head)
user_panel.add(user_head)

regHead = Label(reg_head, text="REGISTERS", height=1, font=("Arial", 10)).grid(row = 0, column = 0)
memHead = Label(mem_head, text="MEMORY", height=1, font=("Arial", 10)).grid(row = 0, column = 0)
userHead = Label(user_head, text="USER TEXT", height=1, font=("Arial", 10)).grid(row = 0, column = 0)

# Body Panel of Register and Memory and User
reg_body = PanedWindow(reg_panel, bg = "white")
mem_body = PanedWindow(mem_panel, bg = "white")
user_body = PanedWindow(user_panel, bg = "white")

reg_panel.add(reg_body)
mem_panel.add(mem_body)
user_panel.add(user_body)

scroll_reg = Scrollbar(reg_body ,orient="vertical")
scroll_mem = Scrollbar(mem_body ,orient="vertical")
scroll_user = Scrollbar(user_body ,orient="vertical")
scroll_reg.pack(side=RIGHT, fill=Y)
scroll_mem.pack(side=RIGHT, fill=Y)
scroll_user.pack(side=RIGHT, fill=Y)

t_reg = Text(reg_body, height = 50, width = 15, wrap = NONE, yscrollcommand = scroll_reg.set, font=("Arial", 9))
t_mem = Text(mem_body, height = 50, width = 35, wrap = NONE, yscrollcommand = scroll_mem.set, font=("Arial", 9))
t_user = Text(user_body, height = 15, width = 50, wrap = NONE, yscrollcommand = scroll_user.set, font=("Arial", 9))

# Console Panel
console_panel = PanedWindow(user_panel, orient="vertical", relief="raised", bg="white")
user_panel.add(console_panel)

console_head = Label(console_panel, text="CONSOLE", relief="raised", height=1, font=("Arial", 10))
console_panel.add(console_head)

console = Label(console_panel, bg="black", font=("Arial", 13), fg="yellow")
console_panel.add(console)

t_console = Text(console, height = 50, width = 70, bg="black", wrap = NONE, font=("Arial", 9), fg="yellow")

def run_gui_data():
    t_reg.configure(state='normal')
    t_mem.configure(state='normal')
    t_user.configure(state='normal')
    t_console.configure(state='normal')

    t_reg.delete("1.0","end")
    t_mem.delete("1.0", "end")
    t_user.delete("1.0", "end")
    t_console.delete("1.0", "end")

    # Data in Register Panel
    t_reg.insert(END, "PC = 0\n")
    k=4
    for i in simu.REGISTERS:
        t_reg.insert(END, str(i) + " = " + str(simu.REGISTERS[i])+"\n")
        k+=1
    t_reg.pack(side=TOP, fill=X)
    scroll_reg.config(command=t_reg.yview)

    # Data in Memory Panel
    k=4
    for i in simu.RAM:
        t_mem.insert(END, str(k-4) + " : " + str(i) + "\n")
        k+=1
    t_mem.pack(side=TOP, fill=X)
    scroll_mem.config(command=t_mem.yview)

    # Data in User Text Panel
    k=4
    for i in simu.lines:
        t_user.insert(END, str(k-3)+" : " + str(i) + "\n")
        k+=1
    t_user.pack(side=TOP, fill=X)
    scroll_user.config(command=t_user.yview)

    # Data in console
    for i in simu.cnsl:
        t_console.insert(END, str(i)+" ")
    t_console.pack(side=TOP, fill=X)
    simu.cnsl = []

    t_reg.configure(state='disabled')
    t_mem.configure(state='disabled')
    t_user.configure(state='disabled')
    t_console.configure(state='disabled')

def modify_gui_data():
    simu.main()
    run_gui_data()

run_gui_data()
root.mainloop()