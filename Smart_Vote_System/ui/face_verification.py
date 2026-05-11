import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import cv2
import os
from deepface import DeepFace


class FaceVerification:

    def __init__(self, root, callback):

        self.root = root
        self.callback = callback

        self.root.title("Face Verification")
        self.root.geometry("400x300")

        ctk.CTkLabel(
            root,
            text="FACE VERIFICATION",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        ctk.CTkButton(
            root,
            text="Start Scan",
            command=self.verify_face
        ).pack(pady=20)

    # ==================================================
    # DEEPFACE VERIFICATION
    # ==================================================

    def verify_face(self):

        # ================= DATABASE =================

        conn = sqlite3.connect("voters.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT voterid, image_path FROM voters"
        )

        data = cursor.fetchall()

        conn.close()

        # ================= CAMERA =================

        cap = cv2.VideoCapture(0)

        messagebox.showinfo(
            "Camera",
            "Press SPACE to capture face"
        )

        temp_image = "temp_capture.jpg"

        while True:

            ret, frame = cap.read()

            cv2.imshow(
                "Face Verification",
                frame
            )

            key = cv2.waitKey(1)

            # SPACE KEY
            if key == 32:

                cv2.imwrite(
                    temp_image,
                    frame
                )

                break

            # ESC KEY
            elif key == 27:

                cap.release()
                cv2.destroyAllWindows()

                return

        cap.release()
        cv2.destroyAllWindows()

        # ==================================================
        # VERIFY FACE AGAINST DATABASE
        # ==================================================

        matched_ids = []

        for voterid, path in data:

            if path and os.path.exists(path):

                try:

                    result = DeepFace.verify(
                        img1_path=temp_image,
                        img2_path=path,
                        model_name="Facenet",
                        enforce_detection=False
                    )

                    if result["verified"]:

                        matched_ids.append(voterid)

                except:
                    continue

        # DELETE TEMP IMAGE

        if os.path.exists(temp_image):

            os.remove(temp_image)

        # ==================================================
        # FINAL SECURITY LOGIC
        # ==================================================

        unique_ids = list(set(matched_ids))

        # ❌ NO MATCH

        if len(unique_ids) == 0:

            messagebox.showerror(
                "Denied",
                "Face not recognized. Please register."
            )

            return

        # ❌ MULTIPLE IDS SAME FACE

        if len(unique_ids) > 1:

            messagebox.showerror(
                "Security Alert",
                "Multiple voter IDs detected for same face.\nAccess denied."
            )

            return

        # ✅ VALID USER

        voterid = unique_ids[0]

        messagebox.showinfo(
            "Verified",
            f"Identity confirmed: {voterid}"
        )

        # NEXT PAGE

        self.callback(voterid)