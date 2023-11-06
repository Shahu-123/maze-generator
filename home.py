import tkinter as tk


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

    global_leaderboard_button = tk.Button(root, text="Global Leaderboard", command=lambda: on_click("global"))
    global_leaderboard_button.place(x=50, y=200, width=200, height=50)

    game_setup_button = tk.Button(root, text="Game Setup", command=lambda: on_click("setup"))
    game_setup_button.place(x=450, y=150, width=200, height=50)

    log_out_button = tk.Button(root, text="Log Out", command=lambda: on_click("log out"))
    log_out_button.place(x=550, y=250, width=100, height=40)

    # Run the main loop and wait for the window to close
    root.mainloop()

    # After the window is destroyed, return the result
    return result.get()


if __name__ == "__main__":
    result = home()
    print(result)
