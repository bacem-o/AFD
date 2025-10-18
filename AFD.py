import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from graphviz import Digraph
import os

# Step 1: Define the AFD
ALPHABET = {'a', 'b'}
STATES = {'q0', 'q1', 'q2'}
INITIAL_STATE = 'q0'
FINAL_STATES = {'q2'}
TRANSITIONS = {
    'q0': {'a': 'q1', 'b': 'q0'},
    'q1': {'a': 'q1', 'b': 'q2'},
    'q2': {'a': 'q1', 'b': 'q0'}
}

# Step 3: AFD Verifier Function
def verifier_afd(chaine, etat_initial, etats_finaux, transitions):
    etat_courant = etat_initial
    for symbole in chaine:
        if symbole in transitions.get(etat_courant, {}):
            etat_courant = transitions[etat_courant][symbole]
        else:
            return False
    return etat_courant in etats_finaux


# Step 5: Creative App
class CreativeAFDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AFD Recognizer")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        self.graph_visible = False

        # Title
        self.title_label = tk.Label(
            root,
            text="✨ Automate Fini Déterministe ✨",
            font=("Arial", 28, "bold"),
            bg="#8e44ad",
            fg="white"
        )
        self.title_label.pack(pady=20)

        # Input Section
        self.input_frame = tk.Frame(root, bg="#f8f9fa", relief=tk.RAISED, bd=2)
        self.input_frame.pack(pady=20, padx=10, ipadx=20, ipady=10)

        self.input_label = tk.Label(self.input_frame, text="Entrez une chaîne :", font=("Arial", 16), bg="#f8f9fa")
        self.input_label.grid(row=0, column=0, padx=10)

        self.input_entry = ttk.Entry(self.input_frame, font=("Arial", 16), width=20)
        self.input_entry.grid(row=0, column=1, padx=10)

        self.verify_button = ttk.Button(self.input_frame, text="✅ Vérifier", command=self.verify_word, style="TButton")
        self.verify_button.grid(row=0, column=2, padx=10)

        # Result Section
        self.result_label = tk.Label(root, text="", font=("Arial", 20, "bold"), bg="#f8f9fa", relief=tk.GROOVE, width=40)
        self.result_label.pack(pady=20)

        # Graph Display Button
        self.toggle_button = tk.Button(
            root, text="Show Graph", command=self.display_graph,
            font=("Helvetica", 14), bg="#4CAF50", fg="white"
        )
        self.toggle_button.pack(pady=10)

        # Add Style
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 14), padding=8)

    def verify_word(self):
        """
        Verify the input word against the AFD.
        """
        chaine = self.input_entry.get()

        if not set(chaine).issubset(ALPHABET):
            messagebox.showerror("Erreur", "La chaîne contient des symboles non valides.")
            return

        if verifier_afd(chaine, INITIAL_STATE, FINAL_STATES, TRANSITIONS):
            self.result_label.config(text=f"La chaîne '{chaine}' est ACCEPTÉE ✅", bg="#2ecc71", fg="white")
        else:
            self.result_label.config(text=f"La chaîne '{chaine}' est REJETÉE ❌", bg="#e74c3c", fg="white")

    def create_graph(self):
        """
        Create a Graphviz visualization of the AFD and save it as a PNG file.
        """
        graph = Digraph(format='png')
        graph.attr(rankdir='LR')  # Left-to-right orientation
        graph.attr('node', shape='circle', style='filled', color='lightblue')

        # Add states
        for state in STATES:
            if state in FINAL_STATES:
                graph.node(state, shape='doublecircle')  # Final states are double circles
            else:
                graph.node(state)

        # Add transitions
        for state, transitions in TRANSITIONS.items():
            for symbol, next_state in transitions.items():
                graph.edge(state, next_state, label=symbol)

        # Initial state marker
        graph.node('', shape='none', width='0')  # Invisible starting point
        graph.edge('', INITIAL_STATE)

        # Render the graph and save it
        graph_path = './afd_graph'
        try:
            graph.render(graph_path, cleanup=True)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création du graphe : {e}")

    def display_graph(self):
        """
        Display the AFD graph using Graphviz.
        """
        self.create_graph()
        try:
            img = Image.open('./afd_graph.png')
            img = img.resize((800, 400), Image.LANCZOS)  # Resize for display

            # Display the image in a new window
            graph_window = tk.Toplevel(self.root)
            graph_window.title("AFD Graph")
            graph_window.geometry("820x450")
            graph_window.resizable(False, False)

            img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(graph_window, image=img_tk)
            label.image = img_tk  # Keep a reference to avoid garbage collection
            label.pack()
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Impossible de charger l'image du graphe.")


# Run the Creative App
if __name__ == "__main__":
    root = tk.Tk()
    app = CreativeAFDApp(root)
    root.mainloop()

