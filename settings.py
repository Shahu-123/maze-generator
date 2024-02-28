import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def home():
    user_choice = None

    def play():
        nonlocal user_choice
        difficulty = difficulty_combo.get()
        num_players = int(num_players_combo.get())

        # Check if difficulty is blank
        if not difficulty:
            tk.messagebox.showerror("Error", "Please select a difficulty!")
            return

        player_details = []
        for i in range(num_players):
            color = color_combos[i].get()
            name = name_entries[i].get() or f"Player {i + 1}"  # Default to Player i if name is blank

            # Check if color for the player is blank
            if not color:
                tk.messagebox.showerror("Error", f"Please select a color for {name}!")
                return

            player_details.append({"name": name, "color": color})

        user_choice = {"difficulty": difficulty, "num_players": num_players, "players": player_details}
        root.quit()
        return


    # Default control sets
    default_controls = [
        ['↑', '↓', '←', '→'],  # Arrow keys for Player 1
        ['W', 'S', 'A', 'D'],  # WASD for Player 2
        ['I', 'K', 'J', 'L']  # IJKL for Player 3
    ]


    root = tk.Tk()
    root.title("Maze Game Setup")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Difficulty Selector
    label_difficulty = ttk.Label(frame, text="Select Difficulty:")
    label_difficulty.grid(row=0, column=0, sticky="w", pady=5)
    difficulties = ["Easy", "Medium", "Hard"]
    difficulty_combo = ttk.Combobox(frame, values=difficulties, state="readonly")
    difficulty_combo.grid(row=0, column=1, pady=5, padx=5)
    difficulty_combo.set("Easy")

    # Player Details
    directions = ["Up", "Down", "Left", "Right"]
    colors = ["Red", "Green", "Blue", "Black"]
    player_labels = [ttk.Label(frame, text=f"Player {i + 1}:") for i in range(3)]
    direction_labels = [ttk.Label(frame, text=direction) for direction in directions]
    control_labels = [[ttk.Label(frame, text=control_set[j]) for j in range(4)] for control_set in default_controls]
    color_combos = [ttk.Combobox(frame, values=colors, state="readonly") for _ in range(4)]
    color_label = ttk.Label(frame, text="Color")
    color_label.grid(row=3, column=2)
    name_label = ttk.Label(frame, text="Name")
    name_label.grid(row=3, column=1)
    name_entries = [ttk.Entry(frame) for _ in range(3)]  # Create entry widgets for player names

    def update_player_options(event):
        selected = int(num_players_combo.get())

        # Display direction labels only once above all control labels
        for idx, direction_label in enumerate(direction_labels):
            direction_label.grid(row=3, column=3 + idx, padx=5)

        for i in range(3):
            if i < selected:
                player_labels[i].grid(row=2 * i + 4, column=0, pady=5, sticky="w")
                name_entries[i].grid(row=2 * i + 4, column=1, pady=5, padx=5)
                color_combos[i].grid(row=2 * i + 4, column=2, pady=5, padx=5)
                for j in range(4):
                    control_labels[i][j].config(text=default_controls[i][j])
                    control_labels[i][j].grid(row=2 * i + 4, column=3 + j, padx=5)
            else:
                player_labels[i].grid_forget()
                name_entries[i].grid_forget()
                color_combos[i].grid_forget()
                for j in range(4):
                    control_labels[i][j].grid_forget()

    # Number of Players Selector
    label_num_players = ttk.Label(frame, text="Number of Players:")
    label_num_players.grid(row=1, column=0, sticky="w", pady=5)
    num_players_combo = ttk.Combobox(frame, values=[1, 2, 3], state="readonly")
    num_players_combo.grid(row=1, column=1, pady=5, padx=5)
    num_players_combo.set(1)  # Set a default value of 1 player.
    num_players_combo.bind("<<ComboboxSelected>>", update_player_options)

    # Create Play Button
    play_button = ttk.Button(frame, text="Play!", command=play)
    play_button.grid(row=0, column=5, pady=5, padx=5, sticky='e')

    update_player_options(None)

    root.mainloop()
    root.destroy()
    return user_choice

if __name__ == "__main__":
    x = home()
    print(x)