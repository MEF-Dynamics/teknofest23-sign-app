# -*- coding: utf-8 -*-

from PIL import Image, ImageTk
from tkinter import ttk
import mediapipe as mp
import tkinter as tk
import numpy as np
import threading
import cv2

from Constants import (
    GUI_PHONE_PNG,
    GUI_CAMERA_B_PNG,
    GUI_CAMERA_R_PNG,
    OTHER_CLUB_ICO_ICO,
)

from Utilities import (
    translate_text,
    vocalize_text,
)

class DisabledAPP(tk.Tk) :

    def __init__(self, available_devices:list, model, *args, **kwargs) :
        """
        Constructor method. Creates the main window of the application.
        @Params:
            available_devices (list): (Reqired) List of available devices.
            *args (tuple): (Optimal) Arguments.
            **kwargs (dict): (Optimal) Keyword arguments.
        @Returns:
            None
        """
        super().__init__(*args, **kwargs)

        self.available_devices = available_devices
        self.model = model

        self.state = "start"

        style = ttk.Style()

        style.theme_use("clam")

        # set root background color to "clam" theme's background color
        self.configure(background=style.lookup("TFrame", "background"))

        style.configure("Output.TLabel", font=("Seoge UI", 14, "bold"), borderwidth=0, cursor="hand2", relief="flat")
        style.configure("SelectedDevice.TLabel", font=("Seoge UI", 11, "bold"), borderwidth=0, cursor="hand2", relief="flat")
        style.configure("SeelctionCombobox.TCombobox", font=("Seoge UI", 11, "bold"), borderwidth=0, cursor="hand2", relief="flat")

        self.title("İşaret Dili Tanımlayıcı")

        self.iconbitmap(OTHER_CLUB_ICO_ICO)

        self.output_text = tk.StringVar(value="Girdi Bekleniyor")

        try :
            self.current_device_name = tk.StringVar(value=self.available_devices[1])
            self.current_device_index = tk.IntVar(value=1)
        except :
            self.current_device_name = tk.StringVar(value=self.available_devices[0])
            self.current_device_index = tk.IntVar(value=0)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0)

        self.background_label = ttk.Label(self.container)
        self.background_label.place(x=0, y=0)

        self.cap = cv2.VideoCapture(self.current_device_index.get())
        
        dummy_label = ttk.Label(self.container, text="")
        dummy_label.grid(row=0, column=0, pady=20)

        frame = self.cap.read()[1]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        self.captured_image = ImageTk.PhotoImage(Image.fromarray(frame).resize((500, 500), Image.LANCZOS))
        self.camera_view_label = ttk.Label(self.container, image=self.captured_image, justify="center", cursor="star", anchor="center", borderwidth=5, border=1)
        self.camera_view_label.grid(row=1, column=0, padx=45)

        self.output_label = ttk.Label(self.container, textvariable=self.output_text, justify="center", cursor="star", style="Output.TLabel")
        self.output_label.grid(row=2, column=0, pady=40)

        self.capture_button_photo = ImageTk.PhotoImage(Image.open(GUI_CAMERA_B_PNG).resize((100, 100), Image.LANCZOS))
        self.capture_button = ttk.Button(self.container, image=self.capture_button_photo, cursor="hand2", command=self.handle_capture_button)
        self.capture_button.grid(row=3, column=0)
        
        dummy_label2 = ttk.Label(self.container, text="")
        dummy_label2.grid(row=4, column=0, pady=20)

        self.device_selection_label = ttk.Label(self.container, text="Kamera Seçimi", justify="center", cursor="star", style="SelectedDevice.TLabel")
        self.device_selection_label.grid(row=5, column=0)

        self.device_selection_combobox = ttk.Combobox(self.container, values=list(self.available_devices.values()), textvariable=self.current_device_name, state="readonly", justify="center", cursor="hand2", width=50, style="SeelctionCombobox.TCombobox")
        self.device_selection_combobox.grid(row=6, column=0)

        self.device_selection_combobox.bind("<<ComboboxSelected>>", self.handle_device_selection)

        dummy_label3 = ttk.Label(self.container, text="")
        dummy_label3.grid(row=7, column=0, pady=20)

        self.update()
        self.update_idletasks()

        tpl = (self.container.winfo_width(), self.container.winfo_height())
        self.minsize(*tpl)
        self.background_image = ImageTk.PhotoImage(Image.open(GUI_PHONE_PNG).resize(tpl, Image.LANCZOS))
        self.background_label.config(image=self.background_image)

        self.update()
        self.update_idletasks()

    def reset_model_variables(self) -> None:
        """
        Class Method, that resets model variables
        @Params
            None
        @Returns
            None
        """

        self.mp_holistic = mp.solutions.holistic # Holistic model
        self.mp_drawing = mp.solutions.drawing_utils # Drawing utilities

        self.sequence = []
        self.sentence = []
        self.predictions = []
        self.threshold = 0.5

        self.actions = np.array(['hello', 'thanks', 'iloveyou'])

        self.holistic = self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def handle_capture_button(self) -> None:
        """
        Class Method, that handles capture button
        @Params
            None
        @Returns
            None
        """

        if self.state == "start" :

            self.capture_button_photo = ImageTk.PhotoImage(Image.open(GUI_CAMERA_R_PNG).resize((100, 100), Image.LANCZOS))
            self.capture_button.config(image=self.capture_button_photo)
            self.device_selection_combobox.config(state="disabled", cursor="arrow")

            self.update()
            self.update_idletasks()

            self.reset_model_variables()

            self.cap = cv2.VideoCapture(self.current_device_index.get())

            self.start_detection()

            self.state = "stop"
        else :

            self.cap.release()
            cv2.destroyAllWindows()

            turkish_sentence = translate_text("en", "tr", " ".join(self.sentence))

            if len(turkish_sentence) > 40 :
                turkish_sentence = turkish_sentence[:40] + "..."

            self.output_text.set(turkish_sentence)

            self.update()
            self.update_idletasks()

            vocalizer_thread = threading.Thread(target=vocalize_text, args=("tr", turkish_sentence))
            vocalizer_thread.start()

            self.capture_button_photo = ImageTk.PhotoImage(Image.open(GUI_CAMERA_B_PNG).resize((100, 100), Image.LANCZOS))
            self.capture_button.config(state="normal", cursor="hand2", image=self.capture_button_photo)
            self.device_selection_combobox.config(state="readonly", cursor="hand2")

            self.camera_view_label.config(image=self.captured_image)

            self.state = "start"

            self.update()
            self.update_idletasks()

            self.rotateApplicationWindow()

            self.update()
            self.update_idletasks()

    def rotateApplicationWindow(self) -> None:
        """
        Class Method, that rotates application window
        @Params
            None
        @Returns
            None
        """
        self.update()
        self.geometry("+{}+{}".format(int(self.winfo_screenwidth()/2 - self.winfo_reqwidth()/2), int(self.winfo_screenheight()/2 - self.winfo_reqheight()/2)))

    def handle_device_selection(self, *event) -> None:
        """
        Class Method, that handles device selection
        @Params
            None
        @Returns
            None
        """
        self.current_device_name.set(self.device_selection_combobox.get())
        self.current_device_index.set(list(self.available_devices.values()).index(self.current_device_name.get()))

    def start_detection(self) -> None:
        """
        Class Method, that starts detection with new thread.
        @Params
            None
        @Returns
            None
        """
        self.main_thread = threading.Thread(target=self.detect)
        self.main_thread.start()

    def detect(self) -> None:
        """
        Class Method, that detects hand gestures.
        @Params
            None
        @Returns
            None
        """

        while self.cap.isOpened() :

            _, current_captured_frame = self.cap.read()

            image = cv2.cvtColor(current_captured_frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = self.holistic.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            #self.mp_drawing.draw_landmarks(image, results.face_landmarks, self.mp_holistic.FACEMESH_TESSELATION, self.mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), self.mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1))
            #self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS,self.mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), self.mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2))
            #self.mp_drawing.draw_landmarks(image, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS, self.mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), self.mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2))
            #self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS, self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

            keypoints = np.concatenate(
                [
                    np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4),
                    np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3),
                    np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3),
                    np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
                ]
            )
            self.sequence.append(keypoints)
            self.sequence = self.sequence[-30:]

            if len(self.sequence) == 30:
                res = self.model.predict(np.expand_dims(self.sequence, axis=0))[0]
                self.predictions.append(np.argmax(res))

            if len(self.sequence) == 30:
                res = self.model.predict(np.expand_dims(self.sequence, axis=0))[0]
                self.predictions.append(np.argmax(res))
                
                if np.unique(self.predictions[-10:])[0]==np.argmax(res): 
                    if res[np.argmax(res)] > self.threshold: 
                        
                        if len(self.sentence) > 0: 
                            if self.actions[np.argmax(res)] != self.sentence[-1]:
                                self.sentence.append(self.actions[np.argmax(res)])
                        else:
                            self.sentence.append(self.actions[np.argmax(res)])

                if len(self.sentence) > 5: 
                    self.sentence = self.sentence[-5:]

            # use the image as video frame
            vd_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            vd_frame = cv2.flip(vd_frame, 1)
            vd_frame = Image.fromarray(vd_frame).resize((500, 500), Image.LANCZOS)
            vd_frame = ImageTk.PhotoImage(image=vd_frame)
            self.camera_view_label.config(image=vd_frame)
            self.captured_image = vd_frame