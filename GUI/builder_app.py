import customtkinter as ctk
from Calculator import Calculator

# --- CONFIGURATION APP ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- COULEURS APPLE ---
COLOR_BG_FRAME = "#1E1E1E"
COLOR_BTN_OP = "#FF9F0A"
COLOR_BTN_NUM = "#333333"
COLOR_BTN_FUNC = "#505050"
COLOR_BTN_SCI = "#333333"
COLOR_HOVER = "#707070"


class CalculatriceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- LOGIQUE ---
        self.calc = Calculator()
        self.historique_visible = True
        self.mode_scientifique = False

        # --- SETUP ---
        self.setup_window()
        self.setup_historique()
        self.setup_calc()
        self.setup_buttons()
        self.setup_sci_buttons()

    # --- FENÊTRE ---
    def setup_window(self):
        self.title("Calculatrice")
        self.geometry("700x580")
        self.resizable(False, False)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    # --- HISTORIQUE ---
    def setup_historique(self):
        self.frame_historique = ctk.CTkFrame(self, corner_radius=15, fg_color=COLOR_BG_FRAME)
        self.frame_historique.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_historique, text="Historique", font=("Helvetica", 16, "bold")).pack(pady=10)

        self.text_historique = ctk.CTkTextbox(self.frame_historique, fg_color="transparent", font=("Helvetica", 12))
        self.text_historique.pack(expand=True, fill="both", padx=5, pady=5)
        self.text_historique.configure(state="disabled")

    # --- CALCULATRICE ---
    def setup_calc(self):
        self.frame_calc = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_calc.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        # Frame pour les boutons du haut (H et Sci)
        self.top_buttons_frame = ctk.CTkFrame(self.frame_calc, fg_color="transparent")
        self.top_buttons_frame.pack(anchor="nw", padx=5, pady=5)

        # Bouton toggle historique
        self.btn_toggle = ctk.CTkButton(
            self.top_buttons_frame, text="H", width=35, height=35,
            fg_color=COLOR_BTN_FUNC, command=self.toggle_historique
        )
        self.btn_toggle.pack(side="left", padx=2)

        # Bouton mode scientifique
        self.btn_sci = ctk.CTkButton(
            self.top_buttons_frame, text="Sci", width=45, height=35,
            fg_color=COLOR_BTN_FUNC, command=self.toggle_scientifique
        )
        self.btn_sci.pack(side="left", padx=2)

        # Écran
        self.ecran = ctk.CTkLabel(self.frame_calc, text="0", font=("Helvetica", 48), anchor="e")
        self.ecran.pack(fill="x", pady=(5, 15), padx=10)

        # Frame conteneur pour tous les boutons
        self.all_buttons_frame = ctk.CTkFrame(self.frame_calc, fg_color="transparent")
        self.all_buttons_frame.pack(expand=True, fill="both")

        # Frame boutons scientifiques (à gauche, caché par défaut)
        self.sci_buttons_frame = ctk.CTkFrame(self.all_buttons_frame, fg_color="transparent", width=130)

        # Frame boutons principaux (à droite)
        self.buttons_frame = ctk.CTkFrame(self.all_buttons_frame, fg_color="transparent")
        self.buttons_frame.pack(side="left", expand=True, fill="both")

    # --- BOUTONS PRINCIPAUX ---
    def setup_buttons(self):
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)

        boutons = [
            ("AC", COLOR_BTN_FUNC, 0, 0, 2), ("%", COLOR_BTN_FUNC, 2, 0, 1), ("÷", COLOR_BTN_OP, 3, 0, 1),
            ("7", COLOR_BTN_NUM, 0, 1, 1), ("8", COLOR_BTN_NUM, 1, 1, 1),
            ("9", COLOR_BTN_NUM, 2, 1, 1), ("×", COLOR_BTN_OP, 3, 1, 1),
            ("4", COLOR_BTN_NUM, 0, 2, 1), ("5", COLOR_BTN_NUM, 1, 2, 1),
            ("6", COLOR_BTN_NUM, 2, 2, 1), ("-", COLOR_BTN_OP, 3, 2, 1),
            ("1", COLOR_BTN_NUM, 0, 3, 1), ("2", COLOR_BTN_NUM, 1, 3, 1),
            ("3", COLOR_BTN_NUM, 2, 3, 1), ("+", COLOR_BTN_OP, 3, 3, 1),
            ("0", COLOR_BTN_NUM, 0, 4, 2), (",", COLOR_BTN_NUM, 2, 4, 1), ("=", COLOR_BTN_OP, 3, 4, 1),
        ]

        for texte, couleur, col, lig, span in boutons:
            btn = ctk.CTkButton(
                self.buttons_frame,
                text=texte,
                fg_color=couleur,
                hover_color=COLOR_HOVER,
                corner_radius=25,
                font=("Helvetica", 22, "bold"),
                command=lambda val=texte: self.action_bouton(val)
            )
            btn.grid(row=lig, column=col, columnspan=span, padx=5, pady=5, sticky="nsew")

    # --- BOUTONS SCIENTIFIQUES (style Apple) ---
    def setup_sci_buttons(self):
        for i in range(5):
            self.sci_buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.sci_buttons_frame.grid_columnconfigure(i, weight=1)

        boutons_sci = [
            ("(", 0, 0), (")", 1, 0),
            ("sin", 0, 1), ("cos", 1, 1),
            ("tan", 0, 2), ("√", 1, 2),
            ("xʸ", 0, 3), ("x²", 1, 3),
            ("π", 0, 4), ("e", 1, 4),
        ]

        for texte, col, lig in boutons_sci:
            btn = ctk.CTkButton(
                self.sci_buttons_frame,
                text=texte,
                fg_color=COLOR_BTN_SCI,
                hover_color=COLOR_HOVER,
                corner_radius=25,
                font=("Helvetica", 18, "bold"),
                width=55,
                command=lambda val=texte: self.action_bouton(val)
            )
            btn.grid(row=lig, column=col, padx=4, pady=5, sticky="nsew")

    # --- TOGGLE HISTORIQUE ---
    def toggle_historique(self):
        if self.historique_visible:
            self.frame_historique.grid_forget()
            base_width = 550 if self.mode_scientifique else 420
        else:
            self.frame_historique.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            base_width = 800 if self.mode_scientifique else 700

        self.geometry(f"{base_width}x580")
        self.historique_visible = not self.historique_visible

    # --- TOGGLE MODE SCIENTIFIQUE ---
    def toggle_scientifique(self):
        if self.mode_scientifique:
            self.sci_buttons_frame.pack_forget()
            self.btn_sci.configure(fg_color=COLOR_BTN_FUNC)
            width = 700 if self.historique_visible else 420
        else:
            self.sci_buttons_frame.pack(side="left", fill="both", padx=(0, 10), before=self.buttons_frame)
            self.btn_sci.configure(fg_color=COLOR_BTN_OP)
            width = 800 if self.historique_visible else 550

        self.geometry(f"{width}x580")
        self.mode_scientifique = not self.mode_scientifique

    # --- ACTION BOUTON ---
    def action_bouton(self, valeur):
        if valeur == "AC":
            self.calc.clear()
            self.ecran.configure(text="0")
        elif valeur == "=":
            result = self.calc.calculate()
            self.ecran.configure(text=result)
            self.update_historique()
        else:
            self.calc.add_value(valeur)
            self.update_ecran()

    # --- MISE À JOUR ÉCRAN ---
    def update_ecran(self):
        display = self.calc.get_display()
        self.ecran.configure(text=display if display else "0")

    # --- MISE À JOUR HISTORIQUE ---
    def update_historique(self):
        self.text_historique.configure(state="normal")
        self.text_historique.delete("0.0", "end")
        self.text_historique.insert("0.0", self.calc.get_formatted_history())
        self.text_historique.configure(state="disabled")


if __name__ == "__main__":
    app = CalculatriceApp()
    app.mainloop()
