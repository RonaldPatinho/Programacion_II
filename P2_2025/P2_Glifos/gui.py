import customtkinter as ctk
from procesar_glifo import ConversorAGlifo
from verificar_numero import ValidarEntrada
import pyperclip

# P2 Conversor a Glifos

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor a Numeros Glificos")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        ctk.set_appearance_mode("dark")

        self.conversor = ConversorAGlifo()
        self.validator = ValidarEntrada()
        self.resultado_actual = ""
        self.copy_button = None

        self.setup_ui()

    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color="#332D56",
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True)

        # CTkTabview para gestionar las pestanas
        self.tab_view = ctk.CTkTabview(self.main_frame
                                       , fg_color="#332D56")
        self.tab_view.pack(fill="both", expand=True)

        self.tab_view.add("Conversion")
        self.tab_view.add("Info")

        # Config titulo
        self.label = ctk.CTkLabel(
            self.tab_view.tab("Conversion"),
            text="CONVERSOR NÚMEROS GLÍFICOS",
            font=("Calibri", 20, "bold"),
            text_color="#FFFFFF"
        )
        self.label.pack(pady=(190, 20))

        # Frame para el campo de entrada y boton
        self.input_frame = ctk.CTkFrame(
            self.tab_view.tab("Conversion"),
            fg_color="#4E6688",
            corner_radius=10,
            border_width=2,
            border_color="#FFFFFF"
        )
        self.input_frame.pack(pady=10, padx=20)

        # Campo de entrada
        self.entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Ingrese un numero [1-3999]",
            width=300,
            fg_color="#E3EEB2",
            text_color="#000000",
            placeholder_text_color="#808080",
            border_color="#332D56",
            border_width=3
        )
        self.entry.pack(pady=10, padx=10, side="left", expand=True, fill="x")

        # Boton
        self.convert_button = ctk.CTkButton(
            self.input_frame,
            text="Convertir", font=("Arial", 14, "bold"), text_color="#262626",
            command=self.convertir,
            fg_color="#71C0BB",
            hover_color="#32726D",
            border_color="#332D56",
            border_width=3
        )
        self.convert_button.pack(pady=10, padx=10, side="right")

        # Frame para el resultado
        self.result_frame = ctk.CTkFrame(
            self.tab_view.tab("Conversion"),
            fg_color="transparent"
        )
        self.result_frame.pack(pady=10)

        # Label para mostrar el resultado
        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="",
            font=("Calibri", 18, "bold"),
            text_color="#FFFFFF",
            justify="center"
        )
        self.result_label.pack(side="top", pady=10)

        # Frame para el boton
        self.copy_button_frame = ctk.CTkFrame(
            self.result_frame,
            fg_color="transparent"
        )
        self.copy_button_frame.pack(side="top", pady=10)

        self.error_label = ctk.CTkLabel(
            self.tab_view.tab("Conversion"),
            text="",
            text_color="#FF5353",
            font=("Calibri", 16, "bold")
        )
        self.error_label.place(relx=0.5, rely=0.85, anchor="center")

        #CTkScrollableFrame para la barra
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.tab_view.tab("Info"),
            fg_color="transparent"
        )
        self.scrollable_frame.pack(fill="both", expand=True)

        self.info_title_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Sistema de Numeración de Aethelgard",
            font=("Arial", 20, "bold"),
            text_color="#FFFFFF",
            justify="left"
        )
        self.info_title_label.pack(pady=(20, 10), padx=20)

        self.info_description_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="  En una civilización antigua olvidada, Aethelgard, se utilizaba un sistema\n"
                 "numérico peculiar basado en un conjunto limitado de glifos y reglas de\n"
                 "combinación muy específicas. Similar al sistema de números romanos.\n\n"
                 "-   Glifos y sus valores:\n\n"
                 "Σ: 1 \n"
                 "Λ: 5 \n"
                 "Ω: 10 \n"
                 "Δ: 50 \n"
                 "Φ: 100 \n"
                 "Ψ: 500 \n"
                 "Ξ: 1000 \n",
            font=("Calibri", 17),
            text_color="#FFFFFF",
            justify="left"
        )
        self.info_description_label.pack(pady=10, padx=20)

        self.fundamentos_title_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Fundamentos:",
            font=("Arial", 18, "bold"),
            text_color="#FFFFFF",
            justify="left"
        )
        self.fundamentos_title_label.pack(pady=(20, 10), padx=20)

        self.fundamentos_description_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="1. Los glifos se leen de izquierda a derecha.\n\n"
                 "2. Un glifo de mayor valor puede preceder a uno de menor valor,\n"
                 "     y sus valores se suman.\n\n"
                 "         Ejemplo: ΩΣ = 10+1 = 11\n\n"
                 "3.  No se repiten glifos más de 3 veces consecutivas.\n\n"
                 "         Ejemplo: 4 no es ΣΣΣΣ, sino ΣΛ.\n\n"
                 "4. Un glifo de menor valor colocado antes de un glifo mayor\n"
                 "     significa que resta al mayor.\n\n"
                 "         Ejemplo: ΣΛ = 4 (5 − 1)\n",
            font=("Calibri", 17),
            text_color="#FFFFFF",
            justify="left"
        )
        self.fundamentos_description_label.pack(pady=10, padx=20)

    def convertir(self):
        entrada = self.entry.get()
        numero = self.validator.validar_entrada(entrada)

        if numero is not None:
            glifos = self.conversor.convertir_a_glifos(numero)
            self.resultado_actual = glifos
            # Resultados
            self.result_label.configure(text=f"Número: {numero}"
                                             f"\n\nGlifos: {glifos}")
            self.error_label.configure(text="")

            # Boton copiar
            if not self.copy_button:
                self.copy_button = ctk.CTkButton(
                    self.copy_button_frame,
                    text="Copiar", font=("Arial", 14, "bold"), text_color="#262626",
                    command=self.copiar_resultado,
                    width=80,
                    fg_color="#71C0BB",
                    hover_color="#32726D",
                    border_color="#4E6688", border_width=3
                )
                self.copy_button.pack()
            else:
                # Visibilidad del boton copiar
                self.copy_button.configure(state="normal")
        else:
            if not entrada.isdigit():
                self.error_label.configure(text="ERROR: Formato de entrada inválido. No es un número.",
                                           text_color="#FF5353")
            else:
                self.error_label.configure(text="ERROR: Número fuera de rango (1-3999)", text_color="#FF5353")
            self.result_label.configure(text="")

            if self.copy_button:
                self.copy_button.configure(state="disabled")

    def copiar_resultado(self):
        if self.resultado_actual:
            pyperclip.copy(self.resultado_actual)
            self.error_label.configure(text="Copiado al portapapeles.",
                                       text_color="#87CB3D",
                                       font=("Calibri", 16, "bold"))
            self.root.after(2000, lambda: self.error_label.configure(text=""))