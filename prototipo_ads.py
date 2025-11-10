import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os # Necessário para lidar com caminhos de arquivo

# --- DADOS DO PROJETO INTEGRADOS ---
PEVS_DATA = [
    {"nome": "PEV Califórnia", "endereco": "Rua Cristiano de Carvalho, nº 50", "status": "Amarelo"},
    {"nome": "PEV Christiano Carvalho", "endereco": "Avenida João Ribeiro do Nascimento", "status": "Verde"},
    {"nome": "PEV Exposição", "endereco": "Rua Fábio Junqueira Franco, nº 301", "status": "Verde"},
    {"nome": "PEV Leda Amendola", "endereco": "LSA 10 - João Botacini, s/nº", "status": "Vermelho"},
]
MATERIAIS = "Restos de construção (entulho), Móveis antigos, Resíduos recicláveis, Podas de madeira, Lixo eletrônico."

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    """Classe principal do aplicativo com fundo de imagem e TabView."""
    def __init__(self):
        super().__init__()

        self.title("MVP Comunitário ADS")
        self.geometry("380x700")
        self.resizable(False, False)

        # 1. TENTATIVA DE CARREGAR IMAGEM DE FUNDO
        try:
            current_path = os.path.dirname(os.path.realpath(__file__))
            self.bg_image = Image.open(os.path.join(current_path, "fundo_bonito.jpg")).resize((380, 700))
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            
            # Adiciona o label da imagem no fundo (background)
            self.bg_label = tk.Label(self, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            # Dentro de class App(ctk.CTk):

# ...
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # Adiciona o label da imagem no fundo (background)
            self.bg_label = tk.Label(self, image=self.bg_photo)
        
        # LINHA DE CORREÇÃO ESSENCIAL: Armazena a referência dentro do label
            self.bg_label.image = self.bg_photo # <--- ADICIONE ESTA LINHA
        
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
# ...

            
        except FileNotFoundError:
            # Caso o usuário não tenha colocado a imagem na pasta
            print("AVISO: 'fundo_bonito.jpg' não encontrado. Usando fundo padrão.")
            self.configure(fg_color="#F0F0F0") 

        # TabView para os dois módulos principais
        self.tab_view = ctk.CTkTabview(self, width=380, fg_color="#FFFFFF", segmented_button_fg_color="#006400", segmented_button_selected_color="#008000")
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_view.add("Mapeamento Comunitário")
        self.tab_view.add("Higiene Digital (ODS 3)")

        # Criação dos Frames (Fluxo Logístico)
        self.frames = {}
        # É necessário que o fg_color seja diferente de None e semi-transparente para ver o fundo, mas para a clareza do protótipo, manteremos branco.
        for F in (MapFrame, StatusFrame, CameraFrame, ConfirmationFrame, HygieneFrame):
            page_name = F.__name__
            frame = F(parent=self.tab_view.tab("Mapeamento Comunitário"), controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Configurações do Módulo de Higiene Digital
        self.frames["HygieneFrame"] = HygieneFrame(parent=self.tab_view.tab("Higiene Digital (ODS 3)"), controller=self)
        self.frames["HygieneFrame"].pack(fill="both", expand=True)

        self.tab_view.set("Mapeamento Comunitário")
        self.show_frame("MapFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# --- MÓDULO 1: Mapeamento Comunitário (Logística) ---

class MapFrame(ctk.CTkFrame):
    """Tela 1: Exibe os PEVs, a Geolocalização Ativa e o Botão de Reporte."""
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent, fg_color="#FFFFFF")
        self.controller = controller

        ctk.CTkLabel(self, text="PEV Finder: Encontre seu Ponto de Descarte", 
                     font=ctk.CTkFont(size=18, weight="bold"), text_color="#1F1F1F").pack(pady=10)

        # 3. SIMULAÇÃO DE GEOLOCALIZAÇÃO ATIVA E MAPA DINÂMICO
        map_area = ctk.CTkFrame(self, fg_color="#ADD8E6", height=250, corner_radius=8)
        map_area.pack(fill="x", pady=(0, 10), padx=10)
        
        ctk.CTkLabel(map_area, text="📡 GPS ATIVO: Localização Atualizada", 
                     text_color="#006400", font=ctk.CTkFont(size=14, weight="bold")).place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        
        # PEV mais próximo em foco
        ctk.CTkLabel(map_area, text="📍 PEV Califórnia (300m)", 
                     text_color="#CC0000", font=ctk.CTkFont(size=18, weight="bold")).place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        
        # Alerta de Status (Mitigação do Risco)
        self.status_label = ctk.CTkLabel(self, text="⚠️ Status: Alerta Amarelo - Coleta Necessária",
                                        fg_color="#FFD700", text_color="#1F1F1F", corner_radius=8,
                                        font=ctk.CTkFont(size=14, weight="bold"), padx=10, pady=5)
        self.status_label.pack(pady=15)

        # Detalhes do PEV (dados integrados)
        detalhes_frame = ctk.CTkFrame(self, fg_color="#F0F0F0")
        detalhes_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(detalhes_frame, text=f"Endereço: {PEVS_DATA[0]['endereco']}", anchor="w", text_color="#1F1F1F").pack(fill="x", pady=2, padx=5)
        ctk.CTkLabel(detalhes_frame, text=f"Aceita: Lixo eletrônico, Recicláveis, Móveis...", anchor="w", text_color="#1F1F1F").pack(fill="x", pady=2, padx=5)

        # Botão para iniciar o fluxo de Prova Fotográfica
        action_button = ctk.CTkButton(self, text="Cheguei ao Ponto - Reportar Status",
                                      command=lambda: controller.show_frame("StatusFrame"),
                                      height=50, font=ctk.CTkFont(size=16, weight="bold"))
        action_button.pack(pady=30, padx=20, fill="x")

# (Classes StatusFrame, CameraFrame e ConfirmationFrame permanecem inalteradas, exceto pelo fg_color='white' para visibilidade)
# ... [Código das classes StatusFrame, CameraFrame, ConfirmationFrame - Para manter a concisão, assumo que você usará as versões anteriores com fg_color='#FFFFFF'] ...

class StatusFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent, fg_color="#FFFFFF")
        self.controller = controller
        ctk.CTkLabel(self, text="Qual é o Status atual do Ponto de Coleta?", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=30, padx=20)
        self.status_var = tk.StringVar(value="Tudo Certo!")
        opcoes = [
            ("🟢 Tudo Certo!", "Tudo Certo!", "green"),
            ("🟡 Precisa de Coleta (Quase Cheio)", "Quase Cheio", "orange"),
            ("🔴 LIXO LOTADO! - IMPOSSÍVEL DESCARTAR", "Lotado", "red"),
            ("❌ Ponto Fechado/Inexistente", "Fechado", "gray")
        ]
        for text, value, color in opcoes:
            radio_button = ctk.CTkRadioButton(self, text=text, variable=self.status_var, value=value, radiobutton_height=20, radiobutton_width=20, font=ctk.CTkFont(size=16), fg_color=color)
            radio_button.pack(anchor="w", pady=15, padx=40)
        ctk.CTkLabel(self, text=f"O que descartar: {MATERIAIS}", wraplength=300, justify="left", text_color="gray").pack(pady=20, padx=40)
        advance_button = ctk.CTkButton(self, text="Avançar para Comprovação", command=self.check_status_and_advance, height=50, font=ctk.CTkFont(size=16, weight="bold"))
        advance_button.pack(pady=30, padx=20, fill="x")
    def check_status_and_advance(self):
        if self.status_var.get() == "Lotado": self.controller.show_frame("CameraFrame")
        else: messagebox.showinfo("Reporte Enviado", f"Status '{self.status_var.get()}' reportado com sucesso. Obrigado!"); self.controller.show_frame("MapFrame")

class CameraFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent, fg_color="#1F1F1F")
        self.controller = controller
        header = ctk.CTkFrame(self, fg_color="#2C3E50", corner_radius=0, height=50)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Prova Fotográfica (Obrigatória)", text_color="white", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        ctk.CTkLabel(self, text="Tire uma foto clara do coletor transbordando para validar a coleta de emergência.", text_color="white", wraplength=300, font=ctk.CTkFont(size=14)).pack(pady=10)
        camera_view = ctk.CTkFrame(self, fg_color="#333333", height=380, width=380, corner_radius=0)
        camera_view.pack(pady=10)
        ctk.CTkLabel(camera_view, text="[VISUALIZAÇÃO DA CÂMERA | FOTO DO LIXO LOTADO]", text_color="#A9A9A9").place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        send_button = ctk.CTkButton(self, text="Enviar Prova e Alertar Comunidade", command=lambda: controller.show_frame("ConfirmationFrame"), height=50, font=ctk.CTkFont(size=16, weight="bold"))
        send_button.pack(pady=50, padx=20, fill="x")

class ConfirmationFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent, fg_color="#FFFFFF")
        self.controller = controller
        ctk.CTkLabel(self, text="✔️", text_color="green", font=ctk.CTkFont(size=150)).pack(pady=(100, 30))
        ctk.CTkLabel(self, text="SUCESSO!", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=10)
        ctk.CTkLabel(self, text="Sua comprovação acionou o alerta de coleta de emergência e o status do mapa foi atualizado.\nObrigado por ajudar!", wraplength=300, justify="center", font=ctk.CTkFont(size=18)).pack(pady=20)
        close_button = ctk.CTkButton(self, text="Fechar e Voltar ao Mapa", command=lambda: controller.show_frame("MapFrame"), height=50, font=ctk.CTkFont(size=16, weight="bold"))
        close_button.pack(pady=20, padx=20, fill="x")


# --- MÓDULO 2: Higiene Digital (ODS 3 - Automatizado) ---

class HygieneFrame(ctk.CTkFrame):
    """Módulo Automatizado de Alerta de Bem-Estar."""
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent, fg_color="#FFFFFF")
        self.controller = controller

        ctk.CTkLabel(self, text="💤 Alerta de Higiene Digital (ODS 3)", 
                     font=ctk.CTkFont(size=22, weight="bold"), text_color="#1F1F1F").pack(pady=20)

        ctk.CTkLabel(self, text="Este módulo monitora automaticamente o uso de tela e promove a saúde mental, baseando-se em sua rotina.", 
                     wraplength=300, justify="center", font=ctk.CTkFont(size=15)).pack(pady=5)
        
        # 1. VISUALIZAÇÃO DE INFORMAÇÃO AUTOMATIZADA
        info_frame = ctk.CTkFrame(self, fg_color="#E0E0E0")
        info_frame.pack(pady=30, padx=20, fill="x")
        
        ctk.CTkLabel(info_frame, text="Status Atual:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 5), padx=10, anchor="w")
        ctk.CTkLabel(info_frame, text="✅ Alerta de Sono ATIVADO", text_color="green", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=5, padx=10, anchor="w")
        ctk.CTkLabel(info_frame, text="Próximo alerta: 22:30h (Redução automática de brilho em 30 minutos).", wraplength=300).pack(pady=(5, 15), padx=10, anchor="w")

        # Dados e Insights
        ctk.CTkLabel(self, text="Insights da Semana (Simulação de BI):", 
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(40, 5), padx=20, anchor="w")
        
        ctk.CTkLabel(self, text="• 85% das noites, você cumpriu a meta de tela reduzida.", anchor="w").pack(pady=5, padx=30, fill="x")
        ctk.CTkLabel(self, text="• Média de sono: 7h 45min", anchor="w").pack(pady=5, padx=30, fill="x")
        ctk.CTkLabel(self, text="• Recomendação: Evite telas por 90 minutos antes de dormir.", anchor="w").pack(pady=5, padx=30, fill="x")


if __name__ == "__main__":
    app = App()
    app.mainloop()