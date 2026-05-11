import customtkinter as ctk
from tkinter import filedialog, messagebox
import sqlite3
import re
import shutil
import cv2
import os
from datetime import datetime

DB_PATH = "voters.db"


class RegisterPage:

    def __init__(self, root):

        self.root = root
        self.root.title("Voter Registration")
        self.root.geometry("500x780")

        self.image_path = ""

        # PASSWORD VISIBILITY
        self.password_visible = False

        # ================= TITLE =================

        title = ctk.CTkLabel(
            root,
            text="VOTER REGISTRATION",
            font=("Arial", 28, "bold")
        )

        title.pack(pady=20)

        # ================= NAME =================

        self.name_entry = ctk.CTkEntry(
            root,
            placeholder_text="Enter Name",
            width=300,
            height=40,
            border_width=2
        )

        self.name_entry.pack(pady=10)

        # ================= PASSWORD =================

        password_frame = ctk.CTkFrame(
            root,
            fg_color="transparent"
        )

        password_frame.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Strong Password",
            show="*",
            width=250,
            height=40,
            border_width=2
        )

        self.password_entry.pack(
            side="left",
            padx=5
        )

        self.password_entry.bind(
            "<KeyRelease>",
            self.validate_password
        )

        # EYE BUTTON

        self.eye_button = ctk.CTkButton(
            password_frame,
            text="👁",
            width=40,
            height=40,
            command=self.toggle_password
        )

        self.eye_button.pack(
            side="left"
        )

        # ================= AADHAAR =================

        self.aadhaar_entry = ctk.CTkEntry(
            root,
            placeholder_text="12 Digit Aadhaar Number",
            width=300,
            height=40,
            border_width=2
        )

        self.aadhaar_entry.pack(pady=10)

        self.aadhaar_entry.bind(
            "<KeyRelease>",
            self.validate_aadhaar
        )

        # ================= DOB =================

        self.dob_entry = ctk.CTkEntry(
            root,
            placeholder_text="DD/MM/YYYY",
            width=300,
            height=40,
            border_width=2
        )

        self.dob_entry.pack(pady=10)

        self.dob_entry.bind(
            "<KeyRelease>",
            self.validate_dob
        )

        # ================= VOTER ID =================

        self.voterid_entry = ctk.CTkEntry(
            root,
            placeholder_text="Voter ID (V001)",
            width=300,
            height=40,
            border_width=2
        )

        self.voterid_entry.pack(pady=10)

        self.voterid_entry.bind(
            "<KeyRelease>",
            self.validate_voterid
        )

        # ================= IMAGE BUTTONS =================

        upload_btn = ctk.CTkButton(
            root,
            text="Upload Face Image",
            command=self.upload_image,
            width=250
        )

        upload_btn.pack(pady=10)

        capture_btn = ctk.CTkButton(
            root,
            text="Capture Live Face",
            command=self.capture_face,
            fg_color="green",
            width=250
        )

        capture_btn.pack(pady=10)

        # ================= REGISTER BUTTON =================

        register_btn = ctk.CTkButton(
            root,
            text="Register",
            command=self.register,
            width=250,
            height=40
        )

        register_btn.pack(pady=20)

    # =====================================================
    # SHOW / HIDE PASSWORD
    # =====================================================

    def toggle_password(self):

        if self.password_visible:

            self.password_entry.configure(
                show="*"
            )

            self.password_visible = False

        else:

            self.password_entry.configure(
                show=""
            )

            self.password_visible = True

    # =====================================================
    # VALID COLORS
    # =====================================================

    def set_valid(self, widget):

        widget.configure(
            border_color="green"
        )

    def set_invalid(self, widget):

        widget.configure(
            border_color="red"
        )

    # =====================================================
    # PASSWORD VALIDATION
    # =====================================================

    def validate_password(self, event=None):

        password = self.password_entry.get()

        strong = (

            len(password) >= 6 and

            re.search(r"[A-Z]", password) and

            re.search(r"[a-z]", password) and

            re.search(r"[0-9]", password) and

            re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password)

        )

        if strong:

            self.set_valid(
                self.password_entry
            )

            return True

        else:

            self.set_invalid(
                self.password_entry
            )

            return False

    # =====================================================
    # AADHAAR VALIDATION
    # =====================================================

    def validate_aadhaar(self, event=None):

        aadhaar = self.aadhaar_entry.get()

        if aadhaar.isdigit() and len(aadhaar) == 12:

            self.set_valid(
                self.aadhaar_entry
            )

            return True

        else:

            self.set_invalid(
                self.aadhaar_entry
            )

            return False

    # =====================================================
    # DOB VALIDATION
    # =====================================================

    def validate_dob(self, event=None):

        dob = self.dob_entry.get()

        try:

            datetime.strptime(
                dob,
                "%d/%m/%Y"
            )

            self.set_valid(
                self.dob_entry
            )

            return True

        except:

            self.set_invalid(
                self.dob_entry
            )

            return False

    # =====================================================
    # VOTER ID VALIDATION
    # =====================================================

    def validate_voterid(self, event=None):

        voterid = self.voterid_entry.get()

        if re.fullmatch(r"V\d{3}", voterid):

            self.set_valid(
                self.voterid_entry
            )

            return True

        else:

            self.set_invalid(
                self.voterid_entry
            )

            return False

    # =====================================================
    # UPLOAD IMAGE
    # =====================================================

    def upload_image(self):

        file_path = filedialog.askopenfilename(
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.png *.jpeg"
                )
            ]
        )

        if file_path:

            os.makedirs(
                "dataset",
                exist_ok=True
            )

            filename = os.path.basename(
                file_path
            )

            destination = os.path.join(
                "dataset",
                filename
            )

            shutil.copy(
                file_path,
                destination
            )

            self.image_path = destination

            messagebox.showinfo(
                "Success",
                "Image Uploaded Successfully"
            )

    # =====================================================
    # CAPTURE FACE
    # =====================================================

    def capture_face(self):

        cam = cv2.VideoCapture(0)

        messagebox.showinfo(
            "Instructions",
            "Press SPACE to Capture"
        )

        while True:

            ret, frame = cam.read()

            cv2.imshow(
                "Capture Face",
                frame
            )

            key = cv2.waitKey(1)

            if key == 32:

                os.makedirs(
                    "dataset",
                    exist_ok=True
                )

                image_name = (
                    self.voterid_entry.get() + ".jpg"
                )

                path = os.path.join(
                    "dataset",
                    image_name
                )

                cv2.imwrite(
                    path,
                    frame
                )

                self.image_path = path

                break

        cam.release()

        cv2.destroyAllWindows()

        messagebox.showinfo(
            "Success",
            "Face Captured Successfully"
        )

    # =====================================================
    # REGISTER FUNCTION
    # =====================================================

    def register(self):

        name = self.name_entry.get()
        password = self.password_entry.get()
        aadhaar = self.aadhaar_entry.get()
        dob = self.dob_entry.get()
        voterid = self.voterid_entry.get()

        # VALIDATIONS

        if not self.validate_password():

            messagebox.showerror(
                "Error",
                "Password must contain:\n"
                "- 6 characters\n"
                "- 1 uppercase\n"
                "- 1 lowercase\n"
                "- 1 number\n"
                "- 1 special character"
            )

            return

        if not self.validate_aadhaar():

            messagebox.showerror(
                "Error",
                "Invalid Aadhaar Number"
            )

            return

        if not self.validate_dob():

            messagebox.showerror(
                "Error",
                "Invalid DOB Format"
            )

            return

        if not self.validate_voterid():

            messagebox.showerror(
                "Error",
                "Voter ID should be like V001"
            )

            return

        if self.image_path == "":

            messagebox.showerror(
                "Error",
                "Upload or Capture Face Image"
            )

            return

        try:

            conn = sqlite3.connect(
                DB_PATH
            )

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO voters
                (
                    name,
                    password,
                    aadhaar,
                    dob,
                    voterid,
                    image_path
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name,
                password,
                aadhaar,
                dob,
                voterid,
                self.image_path
            ))

            conn.commit()

            conn.close()

            messagebox.showinfo(
                "Success",
                "Registration Successful"
            )

            self.root.destroy()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "Voter ID Already Exists"
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )