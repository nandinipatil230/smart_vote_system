import customtkinter as ctk
from tkinter import messagebox
import sqlite3


class VotePage:

    def __init__(self, root, voterid):

        self.root = root
        self.voterid = voterid

        self.root.geometry("500x500")
        self.root.title("Vote Casting")

        title = ctk.CTkLabel(
            root,
            text="CAST YOUR VOTE",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        self.selected = ctk.StringVar(value="")

        for name, val in [
            ("Candidate A", "A"),
            ("Candidate B", "B"),
            ("Candidate C", "C")
        ]:

            ctk.CTkRadioButton(
                root,
                text=name,
                variable=self.selected,
                value=val
            ).pack(pady=10)

        ctk.CTkButton(
            root,
            text="Submit Vote",
            command=self.submit_vote
        ).pack(pady=20)

    # ================= VOTE SUBMIT =================

    def submit_vote(self):

        vote = self.selected.get()

        if vote == "":

            messagebox.showerror("Error", "Select Candidate")
            return

        conn = sqlite3.connect("voters.db")
        cursor = conn.cursor()

        # CHECK DOUBLE VOTE
        cursor.execute(
            "SELECT voted FROM voters WHERE voterid=?",
            (self.voterid,)
        )

        data = cursor.fetchone()

        if not data or data[0] == 1:

            messagebox.showerror("Denied", "Already Voted or Invalid")
            conn.close()
            return

        # STORE VOTE FOR DASHBOARD
        cursor.execute(
            "INSERT INTO votes (voterid, candidate) VALUES (?, ?)",
            (self.voterid, vote)
        )

        # MARK VOTED
        cursor.execute(
            "UPDATE voters SET voted=1 WHERE voterid=?",
            (self.voterid,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Voted for {vote}")

        self.root.destroy()