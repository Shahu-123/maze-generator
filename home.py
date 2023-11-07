import tkinter as tk
from tkinter import ttk


def create_dropdown(root, choices):
    # Create a Tkinter variable for holding the selected option
    selected_option = tk.StringVar()

    # Create the dropdown menu
    dropdown = ttk.Combobox(root, textvariable=selected_option)

    # Set the options for the dropdown
    dropdown['values'] = choices

    # Set the default value for the dropdown (first option in the list)
    dropdown.current(0)

    # Position the dropdown using pack (you can also use grid or place)
    dropdown.pack()

    # Return the selected option variable and the dropdown object
    return selected_option, dropdown
def home():
    def on_click(value):
        result.set(value)
        root.destroy()

    root = tk.Tk()
    root.title("Home")

    # Set the size of the window
    root.geometry('700x300')

    # Set the background color to a light blue
    root.configure(bg='#ADD8E6')

    # This StringVar will hold the result to be returned.
    result = tk.StringVar()

    # Define buttons with commands that set the result and destroy the window
    # Use the place geometry manager to position buttons
    customFont = ('TkDefaultFont', 35)
    home_label = tk.Label(root, text="Home", bg='#ADD8E6',fg='black', font=customFont)
    home_label.place(x=200, y=5, width=300, height=50)

    local_leaderboard_button = tk.Button(root, text="Local Leaderboard", command=lambda: on_click("local"))
    local_leaderboard_button.place(x=50, y=100, width=200, height=50)

    level_label = tk.Label(root, text="Leaderboard Level:", bg='#ADD8E6', fg='black', font=("Arial", 15))
    level_label.place(x=50, y=65, width=130, height=30)

    # Define the options for the dropdown
    options = ['Easy', 'Medium', 'Hard']
    # Create the dropdown by calling the function
    selected_option_var, my_dropdown = create_dropdown(root, options)
    # Function to handle selection change
    selection = selected_option_var.get()
    def on_select(event):
        nonlocal selection
        selection = selected_option_var.get()
    # Bind the selection event to the dropdown
    my_dropdown.bind('<<ComboboxSelected>>', on_select)
    my_dropdown.place(x=200, y=65, width=75, height=30)

    global_leaderboard_button = tk.Button(root, text="Global Leaderboard", command=lambda: on_click("global"))
    global_leaderboard_button.place(x=50, y=200, width=200, height=50)

    game_setup_button = tk.Button(root, text="Game Setup", command=lambda: on_click("setup"))
    game_setup_button.place(x=450, y=150, width=200, height=50)

    log_out_button = tk.Button(root, text="Log Out", command=lambda: on_click("log out"))
    log_out_button.place(x=550, y=250, width=100, height=40)

    # Run the main loop and wait for the window to close
    root.mainloop()

    # After the window is destroyed, return the result
    return result.get() + selection


if __name__ == "__main__":
    result = home()
    print(result)
