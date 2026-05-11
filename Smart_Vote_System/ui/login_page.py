import customtkinter as ctk
from tkinter import messagebox
import sqlite3

from ui.register_page import RegisterPage
from ui.face_verification import FaceVerification
from ui.profile_page import ProfilePage
from ui.vote_page import VotePage
from ui.dashboard_page import DashboardPage


class LoginPage:

    def __init__(self, root):

        self.root = root
        self.root.title("Smart Voting System")
        self.root.geometry("500x550")

        self.password_visible = False

        # TITLE
        ctk.CTkLabel(
            root,
            text="SMART VOTING SYSTEM",
            font=("Arial", 30, "bold")
        ).pack(pady=30)

        # USERNAME
        self.username_entry = ctk.CTkEntry(root, placeholder_text="Enter Username", width=300)
        self.username_entry.pack(pady=10)

        # PASSWORD FRAME
        password_frame = ctk.CTkFrame(root, fg_color="transparent")
        password_frame.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Enter Password",
            show="*",
            width=250
        )
        self.password_entry.pack(side="left")

        # EYE BUTTON
        ctk.CTkButton(
            password_frame,
            text="👁",
            width=40,
            command=self.toggle_password
        ).pack(side="left", padx=5)

        # LOGIN
        ctk.CTkButton(root, text="Login", command=self.login).pack(pady=10)

        # SIGNUP
        ctk.CTkButton(root, text="Signup", fg_color="green",
                      command=self.open_signup).pack(pady=10)

        # DASHBOARD
        ctk.CTkButton(root, text="Open Dashboard", fg_color="purple",
                      command=self.open_dashboard).pack(pady=10)

    # ================= PASSWORD TOGGLE =================

    def toggle_password(self):

        if self.password_visible:
            self.password_entry.configure(show="*")
            self.password_visible = False
        else:
            self.password_entry.configure(show="")
            self.password_visible = True

    # ================= LOGIN =================

    def login(self):

        user = self.username_entry.get()
        pwd = self.password_entry.get()

        conn = sqlite3.connect("voters.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT voterid, voted FROM voters WHERE name=? AND password=?",
            (user, pwd)
        )

        data = cursor.fetchone()
        conn.close()

        if not data:
            messagebox.showerror("Error", "Invalid Login")
            return

        voterid, voted = data

        if voted == 1:
            messagebox.showerror("Denied", "Already Voted")
            return

        # FACE VERIFICATION → PROFILE PAGE FLOW

        face_window = ctk.CTkToplevel(self.root)

        FaceVerification(
            face_window,
            callback=self.open_profile_page
        )

    # ================= PROFILE PAGE =================

    def open_profile_page(self, voterid):

        profile_window = ctk.CTkToplevel(self.root)

        ProfilePage(profile_window, voterid)

    # ================= VOTE PAGE (CALLED FROM PROFILE PAGE) =================

    def open_vote_page(self, voterid):

        vote_window = ctk.CTkToplevel(self.root)

        VotePage(vote_window, voterid)

    # ================= DASHBOARD =================

    def open_dashboard(self):

        dash = ctk.CTkToplevel(self.root)

        DashboardPage(dash)

    # ================= SIGNUP =================

    def open_signup(self):

        signup = ctk.CTkToplevel(self.root)

        RegisterPage(signup)