# -*- coding: utf-8 -*-

from PIL import Image, ImageTk
from tkinter import ttk
import tensorflow as tf
import tkinter as tk

from GUI import (
    DisabledAPP,
    NormalAPP
)

from Constants import (
    GUI_PHONE_PNG,
    OTHER_TEKNOFEST_LOGO_PNG,
    OTHER_CLUB_LOGO_PNG,
    AI_MODEL_PATH,
    OTHER_CLUB_ICO_ICO
)

from Utilities import (
    get_available_cameras,
    get_available_michrophones,
)

class Application(tk.Tk) :

    def __init__(self, *args, **kwargs) -> None:
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

        self.detector_model = tf.keras.models.load_model(AI_MODEL_PATH)
        self.available_cameras = get_available_cameras()
        self.available_michrophones = get_available_michrophones()

        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

        style = ttk.Style()

        style.theme_use("clam")

        self.configure(background=style.lookup("TFrame", "background"))

        style.configure("StartButton.TButton", font=("Seoge UI", 18, "bold"), foreground="white", background="#00b300", borderwidth=0, cursor="hand2", relief="flat")
        style.configure("StartButton2.TButton", font=("Seoge UI", 18, "bold"), foreground="white", background="red", borderwidth=0, cursor="hand2", relief="flat")
        
        self.title("Herkes İçin İşaret Dili")

        self.iconbitmap(OTHER_CLUB_ICO_ICO)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0)

        self.background_label = ttk.Label(self.container)
        self.background_label.place(x=0, y=0)

        self.logo_sizes = (250, 170)
        self.teknofest_logo = ImageTk.PhotoImage(Image.open(OTHER_TEKNOFEST_LOGO_PNG).resize(self.logo_sizes, Image.LANCZOS))
        self.club_logo = ImageTk.PhotoImage(Image.open(OTHER_CLUB_LOGO_PNG).resize(self.logo_sizes, Image.LANCZOS))
        self.teknofes_logo_label = ttk.Label(self.container, image=self.teknofest_logo, cursor="heart")
        self.club_logo_label = ttk.Label(self.container, image=self.club_logo, cursor="heart")
        self.teknofes_logo_label.grid(row=0, column=0, pady=40)
        self.club_logo_label.grid(row=1, column=0)

        self.info_text = [
            "Merhaba Hoş Geldiniz !",
            "Bu uygulamadaki motivasyonumuz aşağıdaki gibidir:",
            "İşaret Dilininin: ",
            "-Yaygınlaşmasını sağlamak",
            "-Farkındalığını artırmak",
            "-Kullanımını kolaylaştırmak",
            "-Öğretiminde verimi artırmak",
            "MEF Dynamics - Engelsiz Yaşam ekibi sunar",
        ]
        
        self.info_text = "\n\n".join(self.info_text)
        self.info_label = ttk.Label(self.container, text=self.info_text, justify="center", cursor="star", font=("Seoge UI", 14, "bold"))
        self.info_label.grid(row=2, column=0, padx=40, pady=40)

        self.input_button = ttk.Button(self.container, text="Uygulamaları Başlat", command=self.start_applications, style="StartButton.TButton", cursor="hand2")
        self.input_button.grid(row=3, column=0)

        dummy_label = ttk.Label(self.container, text="")
        dummy_label.grid(row=4, column=0, pady=20)

        self.update()
        self.update_idletasks()
        
        tpl = (self.container.winfo_width(), self.container.winfo_height())
        self.minsize(*tpl)
        # self.background_image = ImageTk.PhotoImage(Image.open(GUI_PHONE_PNG).resize(tpl, Image.LANCZOS))
        # self.background_label.config(image=self.background_image)

        self.rotateApplicationWindow()

        self.update()
        self.update_idletasks()
        
    def close(self) -> None:
        """
        Class Method, that closes the application.
        @Params:
            None
        @Returns:
            None
        """
        try :
            self.close_applications()
        except :
            pass
        self.destroy()
        self.quit()

    def start_applications(self) -> None:
        """
        Class Method, that starts the applications.
        @Params:
            None
        @Returns:
            None
        """

        self.input_button.config(text="Uygulamaları Kapat", cursor="hand2", style="StartButton2.TButton")
        self.input_button.config(command=self.close_applications)

        self.disabled_app = DisabledAPP(self.available_cameras, self.detector_model)
        self.normal_app = NormalAPP(self.available_michrophones)

        self.normal_app.mainloop()
        self.disabled_app.mainloop()

    def close_applications(self) -> None:
        """
        Class Method, that closes the applications.
        @Params:
            None
        @Returns:
            None
        """
        self.input_button.config(text="Uygulamaları Başlat", cursor="hand2", style="StartButton.TButton")
        self.input_button.config(command=self.start_applications)

        try :
            self.normal_app.close()
            self.disabled_app.close()
        except :
            pass


    def rotateApplicationWindow(self) -> None:
        """
        Class Method, that rotates the application window.
        @Params:
            None
        @Returns:
            None
        """
        self.update()
        self.geometry("+{}+{}".format(int(self.winfo_screenwidth()/2 - self.winfo_reqwidth()/2), int(self.winfo_screenheight()/2 - self.winfo_reqheight()/2)))
