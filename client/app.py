import tkinter as tk

def bar_menu(wind):
    bar_menu = tk.Menu(wind)
    wind.config(menu = bar_menu, width= 300, height=300)
    
    menu_start = tk.Menu(bar_menu, tearoff = 0)
    bar_menu.add_cascade(label='Start', menu = menu_start)
    
    menu_start.add_command(label='Create Register' )
    menu_start.add_command(label='delete Register')
    menu_start.add_command(label='Exit', command= wind.destroy)
    
    bar_menu.add_cascade(label='Query')
    bar_menu.add_cascade(label='Setting')
    bar_menu.add_cascade(label='Help')