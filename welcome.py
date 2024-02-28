import tkinter as tk

def show_welcome_page():
    def start_game():
        root.destroy()
    root = tk.Tk()
    root.title("Maze Adventure")

    root.geometry("640x640")

    background_image = tk.PhotoImage(file="welcome.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(width=640, height=640)

    play_button = tk.Button(root, width=15, height=2, text="Play", font=("Arial", 20), command=start_game)
    play_button.place(x=336, y=397, anchor="center")

    root.mainloop()
    return

if __name__ == "__main__":
    x = show_welcome_page()
    print(x)

