import tkinter as tk

def show_welcome_page():
    def start_game():
        root.destroy()
        return True

    root = tk.Tk()
    root.title("Maze Adventure")

    # Assuming the image dimensions are 1024x1024
    root.geometry("640x640")

    # Background Image (Assuming you have saved the generated image as 'welcome_page.png')
    background_image = tk.PhotoImage(file="welcome.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Play Button
    play_button = tk.Button(root, width=15 ,height=2, text="Play", font=("Arial", 20), command=start_game)
    play_button.place(relx=0.525, rely=0.62, anchor="center")


    root.mainloop()
    return True

if __name__ == "__main__":
    show_welcome_page()
