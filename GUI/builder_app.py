import customtkinter as ctk
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CalculatriceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculatrice Style Mac")
        self.geometry("700x580") 
        self.resizable(False, False)
        self.historique_active = True
        self.equation = ""

        # --- MISE EN PAGE ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame_historique = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E1E1E")
        self.frame_historique.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.frame_historique, text="Historique", font=("Helvetica", 16, "bold")).pack(pady=10)
        self.text_historique = ctk.CTkTextbox(self.frame_historique, fg_color="transparent", font=("Helvetica", 12))
        self.text_historique.pack(expand=True, fill="both", padx=5, pady=5)
        self.text_historique.configure(state="disabled")

        self.frame_calc = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_calc.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        self.btn_toggle = ctk.CTkButton(self.frame_calc, text="H", width=35, height=35, fg_color="#505050", command=self.toggle_historique)
        self.btn_toggle.pack(anchor="nw", padx=5, pady=5)
        self.ecran = ctk.CTkLabel(self.frame_calc, text="0", font=("Helvetica", 55), anchor="e")
        self.ecran.pack(fill="x", pady=(5, 15), padx=10)

        self.buttons_frame = ctk.CTkFrame(self.frame_calc, fg_color="transparent")
        self.buttons_frame.pack(expand=True, fill="both")
        for i in range(5): self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4): self.buttons_frame.grid_columnconfigure(i, weight=1)
        self.creer_boutons()

    def creer_boutons(self):
        boutons = [
            ('AC', '#505050', 0, 0, 2), ('%', '#505050', 2, 0, 1), ('÷', '#FF9F0A', 3, 0, 1),
            ('7', '#333333', 0, 1, 1), ('8', '#333333', 1, 1, 1), ('9', '#333333', 2, 1, 1), ('×', '#FF9F0A', 3, 1, 1),
            ('4', '#333333', 0, 2, 1), ('5', '#333333', 1, 2, 1), ('6', '#333333', 2, 2, 1), ('-', '#FF9F0A', 3, 2, 1),
            ('1', '#333333', 0, 3, 1), ('2', '#333333', 1, 3, 1), ('3', '#333333', 2, 3, 1), ('+', '#FF9F0A', 3, 3, 1),
            ('0', '#333333', 0, 4, 2), (',', '#333333', 2, 4, 1), ('=', '#FF9F0A', 3, 4, 1)
        ]
        for b in boutons:
            t, c, col, lig, span = b
            btn = ctk.CTkButton(self.buttons_frame, text=t, fg_color=c, hover_color="#707070", corner_radius=25, 
                                font=("Helvetica", 22, "bold"), command=lambda val=t: self.action_bouton(val))
            btn.grid(row=lig, column=col, columnspan=span, padx=6, pady=6, sticky="nsew")

    def toggle_historique(self):
        if self.historique_active:
            self.frame_historique.grid_forget()
            self.geometry("450x580")
        else:
            self.frame_historique.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            self.geometry("700x580")
        self.historique_active = not self.historique_active

    def action_bouton(self, valeur):
        if valeur == "AC":
            self.equation = ""
            self.ecran.configure(text="0")
        elif valeur == "=":
            self.calculer_resultat()
        elif valeur == "×": self.equation += "*"
        elif valeur == "÷": self.equation += "/"
        elif valeur == ",": self.equation += "."
        else:
            self.equation += valeur
            self.ecran.configure(text=self.equation.replace('*', '×').replace('/', '÷'))

    def calculer_resultat(self):
        try:
            # 1. Séparer les nombres et les opérateurs (ex: "10+5*2" -> ['10', '+', '5', '*', '2'])
            # On utilise re.findall pour isoler nombres (décimaux inclus) et signes
            elements = re.findall(r'\d+\.?\d*|[+\-*/%]', self.equation)
            
            # Convertir les chaînes de nombres en float
            tokens = [float(e) if e not in "+-*/%" else e for e in elements]

            # 2. Gérer les Priorités (Multiplication, Division, Modulo)
            i = 0
            while i < len(tokens):
                if tokens[i] in ['*', '/', '%']:
                    n1 = tokens[i-1]
                    op = tokens[i]
                    n2 = tokens[i+1]
                    if op == '*': res = n1 * n2
                    elif op == '/': res = n1 / n2 if n2 != 0 else "Err"
                    elif op == '%': res = n1 % n2
                    
                    # Remplacer les 3 éléments par le résultat
                    tokens[i-1:i+2] = [res]
                    i -= 1 # Re-vérifier l'index actuel
                i += 1

            # 3. Gérer Addition et Soustraction
            i = 0
            while i < len(tokens):
                if tokens[i] in ['+', '-']:
                    n1 = tokens[i-1]
                    op = tokens[i]
                    n2 = tokens[i+1]
                    res = n1 + n2 if op == '+' else n1 - n2
                    tokens[i-1:i+2] = [res]
                    i -= 1
                i += 1

            final_res = tokens[0]
            # Formatage propre
            res_str = f"{final_res:g}".replace('.', ',') 
            
            self.ajouter_historique(f"{self.equation} = {res_str}")
            self.ecran.configure(text=res_str)
            self.equation = str(final_res)
        except Exception:
            self.ecran.configure(text="Erreur")
            self.equation = ""

    def ajouter_historique(self, texte):
        self.text_historique.configure(state="normal")
        propre = texte.replace('*', '×').replace('/', '÷').replace('.', ',')
        self.text_historique.insert("0.0", propre + "\n\n")
        self.text_historique.configure(state="disabled")

if __name__ == "__main__":
    app = CalculatriceApp()
    app.mainloop()