import tkinter as tk
from tkinter import simpledialog, messagebox, PhotoImage

background_color = "#2d2d2d"
text_color = "#ffffff"
button_color = "#4e4e4e"
button_text_color = "#e0e0e0"
title_font = ("Verdana", 18, "bold")
description_font = ("Verdana", 12)
button_font = ("Verdana", 12, "bold")
score_font = ("Verdana", 12, "bold")

class Player:
    def __init__(self, name, total_questions):
        self.name = name
        self.knowledge = 0
        self.Done = 0
        self.score = 0
        self.race_progress = 0
        self.total_questions = total_questions
        self.correct_answers = 0

class NPC:
    def __init__(self, name, concept, puzzle):
        self.name = name
        self.concept = concept
        self.puzzle = puzzle

class Puzzle:
    def __init__(self, question, options, answer):
        self.question = question
        self.options = options
        self.answer = answer

class MultipleChoiceDialog(tk.Toplevel):
    def __init__(self, parent, title, question, options):
        super().__init__(parent)
        self.title(title)
        self.question = question
        self.options = options
        self.selected_answer = None
        self.timer_label = None
        self.var = tk.StringVar()
        self.create_widgets()
        self.start_timer()
        self.center_window()

    def create_widgets(self):
        question_label = tk.Label(self, text=self.question, font=description_font)
        question_label.pack(pady=(10, 10))
        question_label.config(justify='center')
        for option in self.options:
            radio = tk.Radiobutton(self, text=option, variable=self.var, value=option)
            radio.pack(anchor='w')
        submit_button = tk.Button(self, text="Submit", command=self.submit)
        submit_button.pack(pady=(5, 10))
        self.timer_label = tk.Label(self, text="10", font=("Verdana", 12, "bold"), fg="red")
        self.timer_label.pack()

    def start_timer(self, count=15):
        if count > 0:
            self.timer_label.config(text=str(count))
            self.after(1000, self.start_timer, count - 1)
        else:
            self.submit()

    def submit(self):
        if self.selected_answer is None:
            self.selected_answer = self.var.get()
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.wait_window()
        return self.selected_answer

    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) / 2
        self.geometry(f"+{int(x)}+{int(y)}")

def interact_with_npc(npc):
    global player
    dialog = MultipleChoiceDialog(root, "Choose an Option", npc.puzzle.question, npc.puzzle.options)
    answer = dialog.show()
    correct = answer == npc.puzzle.answer

    if correct:
        messagebox.showinfo("Result", "Correct answer!")
        player.knowledge += 1
        player.Done += 1
        player.score += 10
        player.correct_answers += 1
        update_race_progress()
    else:
        messagebox.showinfo("Correct Answer", f"Wrong answer! The correct answer was: {npc.puzzle.answer}")
        player.score -= 5
        player.Done += 1

    score_label.config(text=f"Score: {player.score}")

    if player.knowledge == player.total_questions:
        end_game()

def update_race_progress():
    global player
    race_length = canvas_width - 80
    steps = race_length // len(npcs)
    player.race_progress += steps
    new_x_position = min(player.race_progress, race_length)
    canvas.coords(racer, new_x_position, canvas_height // 2)

def close_game():
    root.destroy()

def end_game():
    global player
    accuracy = (player.correct_answers / player.total_questions) * 100

    if accuracy >= 75:
        message = (f"Outstanding Achievement, {player.name}!\n\n"
                   f"With an impressive score of {accuracy:.2f}%, you have explored the depths of Heidegger's philosophy. "
                   "Consider how this wisdom can be a guiding light in your professional career, paving the way for thoughtful and meaningful contributions. "
                   "In your personal life, let it deepen your relationships and self-understanding. "
                   "Spiritually, may it provide a compass for inner peace and existential contemplation. "
                   "Artistically, use these insights to create works that truly resonate with the essence of being.")
    elif accuracy >= 50:
        message = (f"Good Effort, {player.name}.\n\n"
                   f"With a score of {accuracy:.2f}%, you're on a meaningful journey of understanding. "
                   "In your professional life, integrate these concepts to enhance decision-making and creativity. "
                   "Personally, use this knowledge to navigate life's complexities with greater awareness. "
                   "Spiritually, let these teachings inspire a deeper connection with your inner self. "
                   "In your artistic pursuits, allow Heidegger's thoughts to influence your creativity, adding depth and substance to your work.")
    elif accuracy >= 25:
        message = (f"Keep Exploring, {player.name}.\n\n"
                   f"Scoring {accuracy:.2f}%, you have taken the first steps in a profound journey. "
                   "Professionally, ponder how Heidegger's ideas might bring new perspectives to your work. "
                   "On a personal level, let these teachings challenge and grow your understanding of self and others. "
                   "Spiritually, may these insights encourage exploration and questioning. "
                   "Artistically, experiment with these concepts to add a unique dimension to your creative expressions.")
    else:
        message = (f"Embark on a Journey of Discovery, {player.name}.\n\n"
                   f"With a score of {accuracy:.2f}%, the world of Heidegger's philosophy awaits you. "
                   "Professionally, think about how his ideas can inspire innovation and critical thinking. "
                   "Personally, let this be an invitation to introspection and personal growth. "
                   "Spiritually, explore how these teachings can offer new perspectives on your beliefs. "
                   "In your art, use this as an opportunity to experiment with deeper themes and existential questions.")

    messagebox.showinfo("Game Over", message)
    next_question_button.pack_forget()


def new_player():
    global player, npc_cycle
    player_name = simpledialog.askstring("New Player", "Enter new player name:")
    if not player_name:
        player_name = "Thinker"
    player = Player(player_name, len(npcs))
    player.knowledge = 0
    player.score = 0
    player.race_progress = 0
    player.Done = 0
    player.correct_answers = 0
    canvas.coords(racer, 40, canvas_height // 2)
    score_label.config(text=f"Score: {player.score}")
    next_question_button.pack(pady=10)
    npc_cycle = iter(npcs)

def generate_next_question():
    global player
    if player.Done < player.total_questions:
        npc = next(npc_cycle)
        interact_with_npc(npc)
    else:
        end_game()

npcs = [
    NPC("Builder", "Building", Puzzle("What does Heidegger imply by stating that 'building is really dwelling'?", 
                                      ["a) Building physical structures is the essence of human existence",
                                       "b) The act of building reflects the human need for shelter",
                                       "c) Building is an extension of dwelling, which is a fundamental aspect of being",
                                       "d) Dwelling is a secondary consequence of building activities"], 
                                      "c) Building is an extension of dwelling, which is a fundamental aspect of being")),

    NPC("Dweller", "Dwelling", Puzzle("According to Heidegger, the concept of 'dwelling' signifies which of the following?", 
                                      ["a) Residing in a physical location",
                                       "b) The basic character of human existence",
                                       "c) A temporary state of living",
                                       "d) An action similar to construction"], 
                                      "b) The basic character of human existence")),

    NPC("Thinker", "Space", Puzzle("How does Heidegger describe the relationship between humans and space?", 
                                   ["a) Humans conquer and manipulate space",
                                    "b) Space is a creation of the human mind",
                                    "c) Humans and space coexist independently",
                                    "d) Humans persist through spaces by virtue of their stay among things and locales"], 
                                   "d) Humans persist through spaces by virtue of their stay among things and locales")),

    NPC("Philosopher", "Fourfold", Puzzle("What is the significance of the 'fourfold' (earth, sky, divinities, mortals) in Heidegger's thought?", 
                                          ["a) It represents the separation of the physical and spiritual world",
                                           "b) It's a metaphor for different stages of life",
                                           "c) It's the union of key elements that make up human existence and the world",
                                           "d) It refers to four distinct philosophical concepts"], 
                                          "c) It's the union of key elements that make up human existence and the world")),

    NPC("Guardian", "Dwelling Essence", Puzzle("What role does 'saving' play in Heidegger’s concept of dwelling?", 
                                               ["a) Saving refers to the economic aspect of dwelling",
                                                "b) It involves protecting and nurturing the essence of things",
                                                "c) Saving is synonymous with hoarding resources",
                                                "d) It refers to the technological advancement in building"], 
                                               "b) It involves protecting and nurturing the essence of things")),

    NPC("Architect", "Building and Thinking", Puzzle("According to Heidegger, what is the relationship between thinking and building?", 
                                                     ["a) They are unrelated activities",
                                                      "b) Thinking leads to building, which in turn influences thinking",
                                                      "c) Building is a form of thinking",
                                                      "d) Thinking and building are both essential for dwelling, but they need to listen to each other"], 
                                                     "d) Thinking and building are both essential for dwelling, but they need to listen to each other")),

    NPC("Craftsman", "Making in Building", Puzzle("How does Heidegger view the process of 'making' in relation to building?", 
                                                  ["a) As an industrial and economic activity",
                                                   "b) Purely as a physical construction process",
                                                   "c) As a process of bringing forth the fourfold into a thing",
                                                   "d) As a temporary and changeable action"], 
                                                  "c) As a process of bringing forth the fourfold into a thing")),

    NPC("Geometer", "Essence of Space", Puzzle("What is the essence of 'space', according to Heidegger?", 
                                               ["a) A measurable void between objects",
                                                "b) An abstract mathematical concept",
                                                "c) A realm created by human perception",
                                                "d) Something made room for, defined by boundaries and locales"], 
                                               "d) Something made room for, defined by boundaries and locales")),

    NPC("Engineer", "Bridge in Thought", Puzzle("Heidegger's concept of the 'bridge' in 'Building Dwelling Thinking' serves to illustrate what?", 
                                                ["a) The technical aspect of construction",
                                                 "b) The bridge as a mere physical connection between two points",
                                                 "c) The gathering of the fourfold and creating a space",
                                                 "d) A historical evolution of architecture"], 
                                                "c) The gathering of the fourfold and creating a space")),

    NPC("Urban Planner", "Modern Dwelling", Puzzle("What does Heidegger suggest is the plight of modern dwelling?", 
                                                   ["a) The focus on technological advancement",
                                                    "b) The lack of physical houses",
                                                    "c) The disconnection from the essence of dwelling",
                                                    "d) The emphasis on urbanization"], 
                                                   "c) The disconnection from the essence of dwelling"))
]

npc_cycle = iter(npcs)

player_name = simpledialog.askstring("Player Name", "Enter your name:")
if not player_name:
    player_name = "Thinker"

player = Player(player_name, len(npcs))

root = tk.Tk()
root.title("Heidegger's Journey: Building, Dwelling, Thinking")
root.attributes('-fullscreen', True)
root.configure(bg=background_color)

heidegger_img = PhotoImage(file="heidegger.png")
heidegger_img = heidegger_img.subsample(3, 3)

title_label = tk.Label(root, text="Heidegger's Journey: Building, Dwelling, Thinking", font=title_font, bg=background_color, fg=text_color)
title_label.pack(pady=(20, 10))

description_label = tk.Label(root, text="Help Heidegger to win the race by answering questions. Right answer: +10, Wrong answer: -5", font=description_font, bg=background_color, fg=text_color)
description_label.pack(pady=(0, 20))

score_label = tk.Label(root, text=f"Score: {player.score}", font=score_font, bg=background_color, fg=text_color)
score_label.pack(pady=(0, 30))

canvas_width = 1200
canvas_height = 200
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack(pady=(5, 0))

racer = canvas.create_image(40, canvas_height // 2, image=heidegger_img)

source_text = "All questions are sourced from 'Martin Heidegger: Basic Writings from Being and Time (1927) to The Task of Thinking' by D.F. Krell and F.A. Capuzzi (1964)."
source_label = tk.Label(root, text=source_text, font=description_font, bg=background_color, fg=text_color, wraplength=500, justify="center")
source_label.pack(pady=(5, 20))

next_question_button = tk.Button(root, text="Generate Next Question", command=generate_next_question, bg=button_color, fg=button_text_color, font=button_font)
next_question_button.pack(pady=10)

close_button = tk.Button(root, text="Close Game", command=close_game, bg="#ff6347", fg=button_text_color, font=button_font)
close_button.pack(pady=(10, 5))

new_player_button = tk.Button(root, text="New Player", command=new_player, bg="#87ceeb", fg=button_text_color, font=button_font)
new_player_button.pack(pady=(5, 20))

root.mainloop()