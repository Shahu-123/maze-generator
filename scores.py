import tkinter as tk
import sqlite3

def get_local_high_scores(account, difficulty):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    query = '''SELECT name, MIN(score) as min_score
               FROM scores 
               WHERE username = ? and difficulty = ?
               GROUP BY name
               ORDER BY min_score;'''

    cursor.execute(query, (account, difficulty))
    scores = cursor.fetchall()
    conn.close()

    return scores


def get_global_high_scores(difficulty):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    query = '''SELECT name, MIN(score) as min_score
                       FROM scores 
                       WHERE difficulty = ?
                       GROUP BY name
                       ORDER BY min_score;'''

    cursor.execute(query, (difficulty,))
    scores = cursor.fetchall()
    conn.close()

    return scores

def show_local_scores(account, difficulty):
    def return_to_home():
        root.destroy()
        return True

    # Fetch the global high scores
    local_scores = get_local_high_scores(account, difficulty)

    # Create the main window
    root = tk.Tk()
    root.title("High Scores")
    root.configure(bg='light blue')  # Set background color of the root window

    # Create a frame for global scores with a light blue background
    local_frame = tk.Frame(root, padx=20, pady=20, bg='light blue')
    local_frame.pack(side="top", fill="both", expand=True)

    # Add titles for the score sections with a larger font
    title = tk.Label(local_frame, text="Local High Scores", font=("Arial", 20, 'bold'), bg='light blue', fg="black")
    title.pack(side="top", pady=(0, 10))  # Add some padding below the title

    # Use a monospaced font for scores to align them nicely
    score_font = ("Courier", 15)

    # Create a canvas for scrolling
    canvas = tk.Canvas(local_frame, bg='light blue', highlightthickness=0)
    scrollbar = tk.Scrollbar(local_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='light blue')

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for name, score in local_scores:
        score_label = tk.Label(scrollable_frame, text=f"{name}: {score}", anchor="e", font=score_font, bg='light blue',
                 fg="black")
        score_label.pack(side="top", fill="x", padx=130)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Button for returning, with some padding for visual appeal
    btn_return = tk.Button(local_frame, text="Return", command=return_to_home, bg='light blue', fg='black')
    btn_return.pack(side="bottom", fill='x', padx=20, pady=(10, 0))

    # Set the minimum size of the window to prevent squishing
    root.minsize(300, 400)

    # Start the Tkinter event loop
    root.mainloop()

def show_global_scores(difficulty):
    def return_to_home():
        root.destroy()
        return True

    # Fetch the global high scores
    global_scores = get_global_high_scores(difficulty)

    # Create the main window
    root = tk.Tk()
    root.title("High Scores")
    root.configure(bg='light blue')  # Set background color of the root window

    # Create a frame for global scores with a light blue background
    global_frame = tk.Frame(root, padx=20, pady=20, bg='light blue')
    global_frame.pack(side="top", fill="both", expand=True)

    # Add titles for the score sections with a larger font
    title = tk.Label(global_frame, text="Global High Scores", font=("Arial", 20, 'bold'), bg='light blue', fg="black")
    title.pack(side="top", pady=(0, 10))  # Add some padding below the title

    # Use a monospaced font for scores to align them nicely
    score_font = ("Courier", 15)

    # Create a canvas for scrolling
    canvas = tk.Canvas(global_frame, bg='light blue', highlightthickness=0)
    scrollbar = tk.Scrollbar(global_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='light blue')

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for name, score in global_scores:
        score_label = tk.Label(scrollable_frame, text=f"{name}: {score}", anchor="e", font=score_font, bg='light blue',
                               fg="black")
        score_label.pack(side="top", fill="x", padx=130)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Button for returning, with some padding for visual appeal
    btn_return = tk.Button(global_frame, text="Return", command=return_to_home, bg='light blue', fg='black')
    btn_return.pack(side="bottom", fill='x', padx=20, pady=(10, 0))

    # Set the minimum size of the window to prevent squishing
    root.minsize(300, 400)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    show_local_scores("test", "Easy")
    show_global_scores("Easy")