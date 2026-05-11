import customtkinter as ctk
from PIL import Image
import sqlite3

from ui.vote_page import VotePage


class ProfilePage:

    def __init__(self, root, voterid):

        self.root = root
        self.voterid = voterid

        self.root.geometry("600x700")
        self.root.title("Voter Details")

        # ---------------- DATABASE ----------------

        conn = sqlite3.connect("voters.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                name,
                aadhaar,
                dob,
                voterid,
                image_path
            FROM voters
            WHERE voterid=?
        """, (voterid,))

        data = cursor.fetchone()
        conn.close()

        # ---------------- CHECK ----------------

        if data is None:

            ctk.CTkLabel(
                root,
                text="Voter Details Not Found",
                font=("Arial", 20, "bold")
            ).pack(pady=20)

            return

        name, aadhaar, dob, voterid, image_path = data

        # ---------------- TITLE ----------------

        ctk.CTkLabel(
            root,
            text="VOTER DETAILS",
            font=("Arial", 28, "bold")
        ).pack(pady=20)

        # ---------------- PHOTO ----------------

        try:
            image = ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=(180, 180)
            )

            ctk.CTkLabel(
                root,
                image=image,
                text=""
            ).pack(pady=10)

        except:
            ctk.CTkLabel(
                root,
                text="No Image Found",
                font=("Arial", 16)
            ).pack(pady=10)

        # ---------------- DETAILS ----------------

        ctk.CTkLabel(root, text=f"Name: {name}", font=("Arial", 18)).pack(pady=5)
        ctk.CTkLabel(root, text=f"Aadhaar: {aadhaar}", font=("Arial", 18)).pack(pady=5)
        ctk.CTkLabel(root, text=f"DOB: {dob}", font=("Arial", 18)).pack(pady=5)
        ctk.CTkLabel(root, text=f"Voter ID: {voterid}", font=("Arial", 18)).pack(pady=5)

        # ---------------- BUTTON ----------------

        ctk.CTkButton(
            root,
            text="Proceed To Vote",
            command=self.open_vote_page
        ).pack(pady=25)

    # ---------------- OPEN VOTE PAGE ----------------

    def open_vote_page(self):

        vote_window = ctk.CTkToplevel(self.root)

        VotePage(vote_window, self.voterid)