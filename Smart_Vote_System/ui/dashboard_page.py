import customtkinter as ctk
import sqlite3


class DashboardPage:

    def __init__(self, root):

        self.root = root
        self.root.title("Voting Dashboard")
        self.root.geometry("500x500")

        # ================= TITLE =================

        title = ctk.CTkLabel(
            root,
            text="LIVE VOTING DASHBOARD",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        # ================= RESULT LABEL =================

        self.result_label = ctk.CTkLabel(
            root,
            text="Loading vote data...",
            font=("Arial", 18)
        )
        self.result_label.pack(pady=20)

        # ================= REFRESH BUTTON =================

        refresh_btn = ctk.CTkButton(
            root,
            text="Refresh Now",
            command=self.load_votes
        )
        refresh_btn.pack(pady=10)

        # ================= INITIAL LOAD =================

        self.load_votes()

        # ================= AUTO REFRESH =================

        self.auto_refresh()

    # ==================================================
    # LOAD VOTES FROM DATABASE
    # ==================================================

    def load_votes(self):

        conn = sqlite3.connect("voters.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT candidate, COUNT(*) 
            FROM votes 
            GROUP BY candidate
        """)

        data = cursor.fetchall()
        conn.close()

        # Default values
        votes = {
            "A": 0,
            "B": 0,
            "C": 0
        }

        for candidate, count in data:
            votes[candidate] = count

        display_text = f"""
Candidate A: {votes['A']}
Candidate B: {votes['B']}
Candidate C: {votes['C']}

TOTAL VOTES: {votes['A'] + votes['B'] + votes['C']}
        """

        self.result_label.configure(text=display_text)

    # ==================================================
    # AUTO REFRESH EVERY 2 SECONDS
    # ==================================================

    def auto_refresh(self):

        self.load_votes()

        self.root.after(2000, self.auto_refresh)