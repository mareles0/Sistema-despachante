import customtkinter as ctk
import mysql.connector
from tkcalendar import DateEntry
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

class DespachanteSistema:
    def __init__(self):
        # Configuração de Estilo
        self.STYLE = {
            'theme_mode': "System",        # Opções: "System", "Dark", "Light"
            'color_theme': "blue",         # Opções: "blue", "green", "dark-blue"
            'background_color': "#FFFFFF", # Cor de fundo padrão
            'title_font': ("Roboto", 24),
            'button_font': ("Roboto", 12),
            'label_font': ("Roboto", 12),
            'entry_font': ("Roboto", 12),
            'border_width': 2,
            'padding': 10,
            'text_color': "#333333",       # Cor de texto padrão
            'delete_button_fg': "#FF5555", # Cor do botão deletar
            'delete_button_hover': "#FF0000" # Cor do botão deletar ao passar o mouse
        }

        # Aplicar tema do customtkinter
        ctk.set_appearance_mode(self.STYLE['theme_mode'])
        ctk.set_default_color_theme(self.STYLE['color_theme'])

        # Inicialização da Janela Principal
        self.root = ctk.CTk()
        self.root.title("Sistema de Gerenciamento - Despachante")
        self.root.state('zoomed')  # Maximizar a janela em modo janela tela cheia

        try:
            self.conectar_bd()
            self.criar_tabelas()
            self.criar_menu_principal()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inicializar o sistema: {e}")
            self.root.destroy()
            raise

    def conectar_bd(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Primeiro1@', 
                database='despachante'
            )
            self.cursor = self.conn.cursor()
            print("Conexão com o banco de dados estabelecida com sucesso!")
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")
            raise

    def criar_tabelas(self):
        """Cria as tabelas necessárias se não existirem"""
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS registros (
                id INT AUTO_INCREMENT PRIMARY KEY,
                placa VARCHAR(10) NOT NULL,
                chassi VARCHAR(50) NOT NULL,
                renavam VARCHAR(50) NOT NULL,
                nome_cliente VARCHAR(100) NOT NULL,
                cpf VARCHAR(14) NOT NULL,
                servico VARCHAR(100) NOT NULL,
                pagamento VARCHAR(50) NOT NULL,
                data DATE NOT NULL,
                observacoes TEXT
            )
            """
            self.cursor.execute(sql)
            self.conn.commit()
            print("Tabela criada/verificada com sucesso!")
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao criar tabelas: {err}")
            raise

    def criar_menu_principal(self):
        """Cria a interface principal com a listagem de registros"""
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Frame principal do menu
        frame_menu = ctk.CTkFrame(self.root, bg_color=self.STYLE['background_color'])
        frame_menu.pack(fill="both", expand=True, padx=self.STYLE['padding'], pady=self.STYLE['padding'])
        
        # Frame superior para título e botões
        frame_superior = ctk.CTkFrame(frame_menu, bg_color=self.STYLE['background_color'])
        frame_superior.pack(fill="x", padx=self.STYLE['padding'], pady=(self.STYLE['padding'], 5))
        
        # Título
        ctk.CTkLabel(
            frame_superior, 
            text="Sistema de Despachante", 
            font=self.STYLE['title_font'],
            text_color=self.STYLE['text_color']  # Cor do texto do título
        ).pack(side="top", pady=10)
        
        # Frame para botões
        frame_botoes = ctk.CTkFrame(frame_superior, bg_color=self.STYLE['background_color'])
        frame_botoes.pack(pady=10)
        
        # Botões do menu em linha horizontal
        ctk.CTkButton(
            frame_botoes, 
            text="Novo Cadastro", 
            font=self.STYLE['button_font'],
            command=self.tela_cadastro
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            frame_botoes, 
            text="Alterar Dados", 
            font=self.STYLE['button_font'],
            command=self.tela_alteracao
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            frame_botoes, 
            text="Sair", 
            font=self.STYLE['button_font'],
            command=self.root.destroy
        ).pack(side="left", padx=10)
        
        # Frame de busca por data
        frame_busca = ctk.CTkFrame(frame_menu, bg_color=self.STYLE['background_color'])
        frame_busca.pack(fill="x", padx=self.STYLE['padding'], pady=5)
        
        ctk.CTkLabel(
            frame_busca, 
            text="Filtrar por Data de Cadastro:", 
            font=self.STYLE['label_font'],
            text_color=self.STYLE['text_color']
        ).pack(side="left", padx=5)
        
        # Data inicial
        ctk.CTkLabel(
            frame_busca, 
            text="De:", 
            font=self.STYLE['label_font'],
            text_color=self.STYLE['text_color']
        ).pack(side="left", padx=5)
        self.data_inicial = DateEntry(
            frame_busca, 
            width=12, 
            background='darkblue',
            foreground='white', 
            borderwidth=self.STYLE['border_width'], 
            date_pattern='dd/mm/yyyy',
            font=self.STYLE['entry_font']
        )
        self.data_inicial.pack(side="left", padx=5)
        
        # Data final
        ctk.CTkLabel(
            frame_busca, 
            text="Até:", 
            font=self.STYLE['label_font'],
            text_color=self.STYLE['text_color']
        ).pack(side="left", padx=5)
        self.data_final = DateEntry(
            frame_busca, 
            width=12, 
            background='darkblue',
            foreground='white', 
            borderwidth=self.STYLE['border_width'], 
            date_pattern='dd/mm/yyyy',
            font=self.STYLE['entry_font']
        )
        self.data_final.pack(side="left", padx=5)
        
        ctk.CTkButton(
            frame_busca, 
            text="Filtrar", 
            font=self.STYLE['button_font'],
            command=self.buscar_por_data
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            frame_busca, 
            text="Mostrar Todos", 
            font=self.STYLE['button_font'],
            command=self.carregar_registros_recentes
        ).pack(side="left", padx=5)
        
        # Tabela de registros
        frame_tabela = ctk.CTkFrame(frame_menu, bg_color=self.STYLE['background_color'])
        frame_tabela.pack(fill="both", expand=True, padx=self.STYLE['padding'], pady=self.STYLE['padding'])
        
        # Criação da tabela
        self.criar_tabela(frame_tabela)
        
        # Carregar registros iniciais
        self.carregar_registros_recentes()

    def criar_tabela(self, parent):
        """Configura a Treeview para exibir os registros"""
        colunas = ("ID", "Placa", "Chassi", "Renavam", "Nome Cliente", "CPF", 
                   "Serviço", "Pagamento", "Data Cadastro", "Observações")
        
        self.tree = ttk.Treeview(parent, columns=colunas, show="tree headings")
        
        # Definir cabeçalhos e colunas seguindo padrões de configuração
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        
        self.tree.pack(fill="both", expand=True, side="left")
        
        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind para edição (duplo clique)
        self.tree.bind("<Double-1>", self.editar_registro)

    def carregar_registros_recentes(self):
        """Carrega os registros ordenados por data mais recente e agrupa por data"""
        try:
            sql = """
            SELECT id, placa, chassi, renavam, nome_cliente, cpf, 
                   servico, pagamento, DATE_FORMAT(data, '%d/%m/%Y') as data_fmt, 
                   observacoes 
            FROM registros 
            ORDER BY data DESC, id DESC
            """
            self.cursor.execute(sql)
            registros = self.cursor.fetchall()
            
            self.tree.delete(*self.tree.get_children())
            
            registros_por_data = {}
            for registro in registros:
                data = registro[8]  # Índice da coluna 'data_fmt'
                if data not in registros_por_data:
                    registros_por_data[data] = []
                registros_por_data[data].append(registro)
            
            for data, registros_dia in registros_por_data.items():
                parent = self.tree.insert("", "end", text=f"Data: {data} ({len(registros_dia)} registros)", open=True)
                for registro in registros_dia:
                    self.tree.insert(parent, "end", values=registro)
                    
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao carregar registros: {err}")

    def buscar_por_data(self):
        """Busca registros por intervalo de data e agrupa por data"""
        try:
            data_inicial_str = self.data_inicial.get_date().strftime('%d/%m/%Y')
            data_final_str = self.data_final.get_date().strftime('%d/%m/%Y')
            
            # Converter datas para o formato 'YYYY-MM-DD' para a consulta SQL
            data_inicial = datetime.strptime(data_inicial_str, '%d/%m/%Y').date()
            data_final = datetime.strptime(data_final_str, '%d/%m/%Y').date()
            
            sql = """
            SELECT id, placa, chassi, renavam, nome_cliente, cpf, 
                   servico, pagamento, DATE_FORMAT(data, '%d/%m/%Y') as data_fmt, 
                   observacoes 
            FROM registros 
            WHERE data BETWEEN %s AND %s 
            ORDER BY data DESC, id DESC
            """
            self.cursor.execute(sql, (data_inicial, data_final))
            registros = self.cursor.fetchall()
            
            self.tree.delete(*self.tree.get_children())
            
            registros_por_data = {}
            for registro in registros:
                data = registro[8]
                if data not in registros_por_data:
                    registros_por_data[data] = []
                registros_por_data[data].append(registro)
            
            for data, registros_dia in registros_por_data.items():
                parent = self.tree.insert("", "end", text=f"Data: {data} ({len(registros_dia)} registros)", open=True)
                for registro in registros_dia:
                    self.tree.insert(parent, "end", values=registro)
            
            if not registros:
                messagebox.showinfo("Informação", "Nenhum registro encontrado no período selecionado.")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao buscar registros: {err}")
        except ValueError as ve:
            messagebox.showerror("Erro", f"Formato de data inválido: {ve}")

    def tela_cadastro(self):
        """Cria a interface de cadastro de novos registros"""
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()
            
        frame_cadastro = ctk.CTkFrame(self.root, bg_color=self.STYLE['background_color'])
        frame_cadastro.pack(expand=True, fill="both", padx=self.STYLE['padding'], pady=self.STYLE['padding'])
        
        # Cabeçalho
        ctk.CTkLabel(
            frame_cadastro, 
            text="Novo Cadastro", 
            font=("Roboto", 20),
            text_color=self.STYLE['text_color']
        ).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Campos de cadastro
        campos = [
            ("Placa:", "placa_entry"),
            ("Chassi:", "chassi_entry"),
            ("Renavam:", "renavam_entry"),
            ("Nome do Cliente:", "nome_entry"),
            ("CPF:", "cpf_entry"),
            ("Serviço:", "servico_entry"),
            ("Pagamento:", "pagamento_entry")
        ]
        
        for i, (label, attr) in enumerate(campos, start=1):
            ctk.CTkLabel(
                frame_cadastro, 
                text=label, 
                font=self.STYLE['label_font'],
                text_color=self.STYLE['text_color']
            ).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ctk.CTkEntry(
                frame_cadastro, 
                width=300, 
                font=self.STYLE['entry_font']
            )
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            setattr(self, attr, entry)
        
        # Data
        ctk.CTkLabel(
            frame_cadastro, 
            text="Data:", 
            font=self.STYLE['label_font'],
            text_color=self.STYLE['text_color']
        ).grid(row=len(campos)+1, column=0, padx=5, pady=5, sticky="e")
        self.data_entry = DateEntry(
            frame_cadastro, 
            width=12, 
            background='darkblue',
            foreground='white', 
            borderwidth=self.STYLE['border_width'], 
            date_pattern='dd/mm/yyyy',
            font=self.STYLE['entry_font']
        )
        self.data_entry.grid(row=len(campos)+1, column=1, padx=5, pady=5, sticky="w")
        
        # Observações
        ctk.CTkLabel(
            frame_cadastro, 
            text="Observações:", 
            font=self.STYLE['label_font'],
            text_color=self.STYLE['text_color']
        ).grid(row=len(campos)+2, column=0, padx=5, pady=5, sticky="ne")
        self.obs_entry = tk.Text(frame_cadastro, width=40, height=10, font=self.STYLE['entry_font'])
        self.obs_entry.grid(row=len(campos)+2, column=1, padx=5, pady=5, sticky="w")
        
        # Botões
        frame_botoes = ctk.CTkFrame(frame_cadastro, bg_color=self.STYLE['background_color'])
        frame_botoes.grid(row=len(campos)+3, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(
            frame_botoes, 
            text="Salvar", 
            font=self.STYLE['button_font'],
            command=self.salvar_cadastro
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            frame_botoes, 
            text="Voltar", 
            font=self.STYLE['button_font'],
            command=self.criar_menu_principal
        ).pack(side="left", padx=10)

    def salvar_cadastro(self):
        """Salva o novo registro no banco de dados"""
        try:
            placa = self.placa_entry.get().strip().upper()
            chassi = self.chassi_entry.get().strip().upper()
            renavam = self.renavam_entry.get().strip().upper()
            nome = self.nome_entry.get().strip()
            cpf = self.cpf_entry.get().strip()
            servico = self.servico_entry.get().strip()
            pagamento = self.pagamento_entry.get().strip()
            data = self.data_entry.get_date()
            observacoes = self.obs_entry.get("1.0", "end-1c").strip()
            
            # Validação dos campos obrigatórios
            if not all([placa, chassi, renavam, nome, cpf, servico, pagamento, data]):
                messagebox.showwarning("Aviso", "Por favor, preencha todos os campos obrigatórios!")
                return
            
            # Inserir no banco de dados
            sql = """INSERT INTO registros 
                    (placa, chassi, renavam, nome_cliente, cpf, servico, 
                     pagamento, data, observacoes) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            self.cursor.execute(sql, (placa, chassi, renavam, nome, cpf, 
                                    servico, pagamento, data, observacoes))
            self.conn.commit()
            
            messagebox.showinfo("Sucesso", "Registro cadastrado com sucesso!")
            self.criar_menu_principal()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {err}")

    def tela_alteracao(self):
        """Cria a interface para alterar registros existentes"""
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()
            
        frame_alteracao = ctk.CTkFrame(self.root, bg_color=self.STYLE['background_color'])
        frame_alteracao.pack(expand=True, fill="both", padx=self.STYLE['padding'], pady=self.STYLE['padding'])
        
        # Cabeçalho
        ctk.CTkLabel(
            frame_alteracao, 
            text="Alterar Dados", 
            font=("Roboto", 20),
            text_color=self.STYLE['text_color']
        ).pack(pady=10)
        
        # Frame de busca
        frame_busca = ctk.CTkFrame(frame_alteracao, bg_color=self.STYLE['background_color'])
        frame_busca.pack(fill="x", padx=self.STYLE['padding'], pady=10)
        
        ctk.CTkLabel(
            frame_busca, 
            text="Buscar por:", 
            font=self.STYLE['label_font'],
            text_color=self.STYLE['text_color']
        ).pack(side="left", padx=5)
        self.campo_busca = ctk.CTkComboBox(
            frame_busca, 
            values=["Placa", "Chassi", "Renavam", "Nome", "CPF"],
            font=self.STYLE['entry_font']
        )
        self.campo_busca.pack(side="left", padx=5)
        
        self.busca_entry = ctk.CTkEntry(
            frame_busca, 
            width=200, 
            font=self.STYLE['entry_font']
        )
        self.busca_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            frame_busca, 
            text="Buscar", 
            font=self.STYLE['button_font'],
            command=self.buscar_alteracao
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            frame_busca, 
            text="Voltar", 
            font=self.STYLE['button_font'],
            command=self.criar_menu_principal
        ).pack(side="left", padx=5)
        
        # Tabela de resultados
        frame_tabela = ctk.CTkFrame(frame_alteracao, bg_color=self.STYLE['background_color'])
        frame_tabela.pack(fill="both", expand=True, padx=self.STYLE['padding'], pady=self.STYLE['padding'])
        
        self.criar_tabela(frame_tabela)

    def buscar_alteracao(self):
        """Realiza a busca para alteração de registros"""
        self.buscar()

    def buscar(self):
        """Busca registros com base no campo e valor fornecidos"""
        campo = self.campo_busca.get()
        valor = self.busca_entry.get().strip()
        
        if not campo or not valor:
            messagebox.showwarning("Aviso", "Selecione um campo e digite um valor para buscar!")
            return
            
        try:
            campo_bd = {
                "Placa": "placa",
                "Chassi": "chassi",
                "Renavam": "renavam",
                "Nome": "nome_cliente",
                "CPF": "cpf"
            }[campo]
            
            sql = f"""SELECT id, placa, chassi, renavam, nome_cliente, cpf, servico, pagamento, 
                     DATE_FORMAT(data, '%d/%m/%Y') as data_fmt, observacoes 
                     FROM registros 
                     WHERE {campo_bd} LIKE %s 
                     ORDER BY data DESC, id DESC"""
            self.cursor.execute(sql, (f"%{valor}%",))
            registros = self.cursor.fetchall()
            
            self.tree.delete(*self.tree.get_children())
            
            registros_por_data = {}
            for registro in registros:
                data = registro[8]
                if data not in registros_por_data:
                    registros_por_data[data] = []
                registros_por_data[data].append(registro)
            
            for data, registros_dia in registros_por_data.items():
                parent = self.tree.insert("", "end", text=f"Data: {data} ({len(registros_dia)} registros)", open=True)
                for registro in registros_dia:
                    self.tree.insert(parent, "end", values=registro)
                    
            if not registros:
                messagebox.showinfo("Informação", "Nenhum registro encontrado com os critérios de busca.")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao buscar: {err}")
        except KeyError:
            messagebox.showerror("Erro", "Campo de busca inválido.")

    def editar_registro(self, event):
        """Cria a interface para editar um registro selecionado"""
        selecionado = self.tree.focus()
        if not selecionado:
            return
        
        parent = self.tree.parent(selecionado)
        if parent:
            # É um registro individual
            valores = self.tree.item(selecionado, 'values')
            id_registro = valores[0]
            placa = valores[1]
            chassi = valores[2]
            renavam = valores[3]
            nome = valores[4]
            cpf = valores[5]
            servico = valores[6]
            pagamento = valores[7]
            data_str = valores[8]
            observacoes = valores[9]
            
            # Converter string de data para objeto date
            data_edit = datetime.strptime(data_str, '%d/%m/%Y').date()
            
            # Janela de edição
            janela_edicao = ctk.CTkToplevel(self.root)
            janela_edicao.title("Editar Registro")
            janela_edicao.state('zoomed')  # Maximizar a janela em modo janela tela cheia
            
            frame_edicao = ctk.CTkFrame(janela_edicao, bg_color=self.STYLE['background_color'])
            frame_edicao.pack(expand=True, fill="both", padx=self.STYLE['padding'], pady=self.STYLE['padding'])
            
            # Cabeçalho
            ctk.CTkLabel(
                frame_edicao, 
                text="Editar Registro", 
                font=("Roboto", 20),
                text_color=self.STYLE['text_color']
            ).grid(row=0, column=0, columnspan=2, pady=10)
            
            # Campos de edição
            campos = [
                ("Placa:", "placa_edit"),
                ("Chassi:", "chassi_edit"),
                ("Renavam:", "renavam_edit"),
                ("Nome do Cliente:", "nome_edit"),
                ("CPF:", "cpf_edit"),
                ("Serviço:", "servico_edit"),
                ("Pagamento:", "pagamento_edit")
            ]
            
            entries = {}
            valores_iniciais = [placa, chassi, renavam, nome, cpf, servico, pagamento]
            for i, (label, attr) in enumerate(campos, start=1):
                ctk.CTkLabel(
                    frame_edicao, 
                    text=label, 
                    font=self.STYLE['label_font'],
                    text_color=self.STYLE['text_color']
                ).grid(row=i, column=0, padx=5, pady=5, sticky="e")
                entry = ctk.CTkEntry(
                    frame_edicao, 
                    width=300, 
                    font=self.STYLE['entry_font']
                )
                entry.insert(0, valores_iniciais[i-1])
                entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
                entries[attr] = entry
            
            # Data
            ctk.CTkLabel(
                frame_edicao, 
                text="Data:", 
                font=self.STYLE['label_font'],
                text_color=self.STYLE['text_color']
            ).grid(row=len(campos)+1, column=0, padx=5, pady=5, sticky="e")
            self.data_edit = DateEntry(
                frame_edicao, 
                width=12, 
                background='darkblue',
                foreground='white', 
                borderwidth=self.STYLE['border_width'], 
                date_pattern='dd/mm/yyyy',
                font=self.STYLE['entry_font']
            )
            self.data_edit.set_date(data_edit)
            self.data_edit.grid(row=len(campos)+1, column=1, padx=5, pady=5, sticky="w")
            
            # Observações
            ctk.CTkLabel(
                frame_edicao, 
                text="Observações:", 
                font=self.STYLE['label_font'],
                text_color=self.STYLE['text_color']
            ).grid(row=len(campos)+2, column=0, padx=5, pady=5, sticky="ne")
            self.obs_edit = tk.Text(frame_edicao, width=40, height=10, font=self.STYLE['entry_font'])
            self.obs_edit.insert("1.0", observacoes if observacoes else "")
            self.obs_edit.grid(row=len(campos)+2, column=1, padx=5, pady=5, sticky="w")
            
            def salvar_edicao():
                """Salva as edições feitas no registro"""
                try:
                    placa_upd = entries["placa_edit"].get().strip().upper()
                    chassi_upd = entries["chassi_edit"].get().strip().upper()
                    renavam_upd = entries["renavam_edit"].get().strip().upper()
                    nome_upd = entries["nome_edit"].get().strip()
                    cpf_upd = entries["cpf_edit"].get().strip()
                    servico_upd = entries["servico_edit"].get().strip()
                    pagamento_upd = entries["pagamento_edit"].get().strip()
                    data_upd = self.data_edit.get_date()
                    observacoes_upd = self.obs_edit.get("1.0", "end-1c").strip()
                    
                    # Validação dos campos obrigatórios
                    if not all([placa_upd, chassi_upd, renavam_upd, nome_upd, cpf_upd, servico_upd, pagamento_upd, data_upd]):
                        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos obrigatórios!")
                        return
                    
                    # Atualizar no banco de dados
                    sql = """UPDATE registros 
                            SET placa=%s, chassi=%s, renavam=%s, nome_cliente=%s,
                                cpf=%s, servico=%s, pagamento=%s, data=%s, 
                                observacoes=%s 
                            WHERE id=%s"""
                                
                    valores_atualizados = [
                        placa_upd,
                        chassi_upd,
                        renavam_upd,
                        nome_upd,
                        cpf_upd,
                        servico_upd,
                        pagamento_upd,
                        data_upd,
                        observacoes_upd,
                        id_registro
                    ]
                    
                    self.cursor.execute(sql, valores_atualizados)
                    self.conn.commit()
                    messagebox.showinfo("Sucesso", "Registro atualizado com sucesso!")
                    janela_edicao.destroy()
                    self.carregar_registros_recentes()
                    
                except mysql.connector.Error as err:
                    messagebox.showerror("Erro", f"Erro ao atualizar: {err}")
                
            def deletar_registro():
                """Deleta o registro selecionado do banco de dados"""
                try:
                    # Confirmação antes de deletar
                    if messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar este registro?"):
                        sql = "DELETE FROM registros WHERE id = %s"
                        self.cursor.execute(sql, (id_registro,))
                        self.conn.commit()
                        messagebox.showinfo("Sucesso", "Registro deletado com sucesso!")
                        janela_edicao.destroy()
                        self.carregar_registros_recentes()
                except mysql.connector.Error as err:
                    messagebox.showerror("Erro", f"Erro ao deletar registro: {err}")

            # Botões
            frame_botoes = ctk.CTkFrame(frame_edicao, bg_color=self.STYLE['background_color'])
            frame_botoes.grid(row=len(campos)+3, column=0, columnspan=2, pady=20)
            
            ctk.CTkButton(
                frame_botoes, 
                text="Salvar", 
                font=self.STYLE['button_font'],
                command=salvar_edicao
            ).pack(side="left", padx=10)
            ctk.CTkButton(
                frame_botoes, 
                text="Deletar", 
                font=self.STYLE['button_font'],
                fg_color=self.STYLE['delete_button_fg'],  # Cor do botão deletar
                hover_color=self.STYLE['delete_button_hover'],  # Cor do botão deletar ao passar o mouse
                command=deletar_registro
            ).pack(side="left", padx=10)
            ctk.CTkButton(
                frame_botoes, 
                text="Cancelar", 
                font=self.STYLE['button_font'],
                command=janela_edicao.destroy
            ).pack(side="left", padx=10)

    def executar(self):
        """Executa a aplicação"""
        self.root.mainloop()
        
    def __del__(self):
        """Destrutor para garantir o fechamento da conexão"""
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
                print("Conexão com o banco de dados fechada.")
        except Exception as e:
            print(f"Erro ao fechar conexão: {e}")

if __name__ == "__main__":
    try:
        app = DespachanteSistema()
        app.executar()
    except Exception as e:
        print(f"Erro fatal: {e}")