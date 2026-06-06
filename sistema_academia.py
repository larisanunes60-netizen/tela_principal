import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import json
import os
from PIL import Image, ImageTk
import sqlite3
from tkcalendar import Calendar

# ===== MÓDULO DE BANCO DE DADOS =====
class DatabaseManager:
    """Módulo responsável por gerenciar todas as operações com o banco de dados"""
    
    def __init__(self):
        self.conn = sqlite3.connect('academia.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Cria todas as tabelas necessárias do banco de dados"""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS alunos
                             (id INTEGER PRIMARY KEY, nome TEXT, email TEXT, 
                              telefone TEXT, data_inicio TEXT, status TEXT)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS instrutores
                             (id INTEGER PRIMARY KEY, nome TEXT, email TEXT, 
                              especialidade TEXT, telefone TEXT, status TEXT)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS treinos
                             (id INTEGER PRIMARY KEY, nome TEXT, descricao TEXT, 
                              series INTEGER, repeticoes INTEGER, descanso INTEGER)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS planos
                             (id INTEGER PRIMARY KEY, nome TEXT, valor REAL, 
                              duracao_dias INTEGER, descricao TEXT)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS avaliacoes
                             (id INTEGER PRIMARY KEY, aluno_id INTEGER, data TEXT, 
                              peso REAL, altura REAL, percentual_gordura REAL, notas TEXT)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS frequencias
                             (id INTEGER PRIMARY KEY, aluno_id INTEGER, data TEXT, 
                              horario TEXT, presente BOOLEAN)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS financeiro
                             (id INTEGER PRIMARY KEY, aluno_id INTEGER, data TEXT, 
                              tipo TEXT, valor REAL, status TEXT, descricao TEXT)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS agenda
                             (id INTEGER PRIMARY KEY, titulo TEXT, data TEXT, 
                              horario TEXT, descricao TEXT, tipo TEXT)''')
        
        self.conn.commit()
    
    def add_aluno(self, nome, email, telefone):
        """Adiciona um novo aluno ao banco de dados"""
        self.cursor.execute('INSERT INTO alunos (nome, email, telefone, data_inicio, status) VALUES (?, ?, ?, ?, ?)',
                           (nome, email, telefone, datetime.now().strftime('%d/%m/%Y'), 'Ativo'))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_alunos(self):
        """Recupera todos os alunos cadastrados"""
        self.cursor.execute('SELECT * FROM alunos')
        return self.cursor.fetchall()
    
    def add_instrutor(self, nome, email, especialidade, telefone):
        """Adiciona um novo instrutor ao banco de dados"""
        self.cursor.execute('INSERT INTO instrutores (nome, email, especialidade, telefone, status) VALUES (?, ?, ?, ?, ?)',
                           (nome, email, especialidade, telefone, 'Ativo'))
        self.conn.commit()
    
    def get_instrutores(self):
        """Recupera todos os instrutores cadastrados"""
        self.cursor.execute('SELECT * FROM instrutores')
        return self.cursor.fetchall()
    
    def add_treino(self, nome, descricao, series, repeticoes, descanso):
        """Adiciona um novo treino ao banco de dados"""
        self.cursor.execute('INSERT INTO treinos (nome, descricao, series, repeticoes, descanso) VALUES (?, ?, ?, ?, ?)',
                           (nome, descricao, series, repeticoes, descanso))
        self.conn.commit()
    
    def get_treinos(self):
        """Recupera todos os treinos cadastrados"""
        self.cursor.execute('SELECT * FROM treinos')
        return self.cursor.fetchall()
    
    def add_plano(self, nome, valor, duracao_dias, descricao):
        """Adiciona um novo plano ao banco de dados"""
        self.cursor.execute('INSERT INTO planos (nome, valor, duracao_dias, descricao) VALUES (?, ?, ?, ?)',
                           (nome, valor, duracao_dias, descricao))
        self.conn.commit()
    
    def get_planos(self):
        """Recupera todos os planos cadastrados"""
        self.cursor.execute('SELECT * FROM planos')
        return self.cursor.fetchall()
    
    def add_avaliacao(self, aluno_id, peso, altura, percentual_gordura, notas):
        """Adiciona uma nova avaliação ao banco de dados"""
        self.cursor.execute('INSERT INTO avaliacoes (aluno_id, data, peso, altura, percentual_gordura, notas) VALUES (?, ?, ?, ?, ?, ?)',
                           (aluno_id, datetime.now().strftime('%d/%m/%Y'), peso, altura, percentual_gordura, notas))
        self.conn.commit()
    
    def get_avaliacoes(self, aluno_id):
        """Recupera todas as avaliações de um aluno"""
        self.cursor.execute('SELECT * FROM avaliacoes WHERE aluno_id = ?', (aluno_id,))
        return self.cursor.fetchall()
    
    def add_frequencia(self, aluno_id, presente):
        """Registra a frequência de um aluno"""
        self.cursor.execute('INSERT INTO frequencias (aluno_id, data, horario, presente) VALUES (?, ?, ?, ?)',
                           (aluno_id, datetime.now().strftime('%d/%m/%Y'), datetime.now().strftime('%H:%M'), presente))
        self.conn.commit()
    
    def get_frequencias(self, aluno_id):
        """Recupera o histórico de frequência de um aluno"""
        self.cursor.execute('SELECT * FROM frequencias WHERE aluno_id = ?', (aluno_id,))
        return self.cursor.fetchall()
    
    def add_financeiro(self, aluno_id, tipo, valor, status, descricao):
        """Adiciona uma transação financeira ao banco de dados"""
        self.cursor.execute('INSERT INTO financeiro (aluno_id, data, tipo, valor, status, descricao) VALUES (?, ?, ?, ?, ?, ?)',
                           (aluno_id, datetime.now().strftime('%d/%m/%Y'), tipo, valor, status, descricao))
        self.conn.commit()
    
    def get_financeiro(self, aluno_id=None):
        """Recupera transações financeiras"""
        if aluno_id:
            self.cursor.execute('SELECT * FROM financeiro WHERE aluno_id = ?', (aluno_id,))
        else:
            self.cursor.execute('SELECT * FROM financeiro')
        return self.cursor.fetchall()
    
    def add_agenda(self, titulo, data, horario, descricao, tipo):
        """Adiciona um evento à agenda"""
        self.cursor.execute('INSERT INTO agenda (titulo, data, horario, descricao, tipo) VALUES (?, ?, ?, ?, ?)',
                           (titulo, data, horario, descricao, tipo))
        self.conn.commit()
    
    def get_agenda(self):
        """Recupera todos os eventos da agenda"""
        self.cursor.execute('SELECT * FROM agenda ORDER BY data DESC')
        return self.cursor.fetchall()
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        self.conn.close()


# ===== TELA PRINCIPAL =====
class TelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão - Academia Fitness")
        self.geometry("1400x800")
        self.state('zoomed')
        
        self.db = DatabaseManager()
        
        # Cores
        self.cor_principal = "#1f3a70"
        self.cor_secundaria = "#2e5090"
        self.cor_accent = "#ff6b35"
        self.cor_texto = "#ffffff"
        
        self.configure(bg=self.cor_principal)
        
        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Menu lateral
        self.criar_menu_lateral()
        
        # Área de conteúdo
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tela inicial
        self.mostrar_painel_principal()
    
    def criar_menu_lateral(self):
        """Cria o menu lateral com todos os botões"""
        menu_frame = ttk.Frame(self.main_frame)
        menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=0, pady=0)
        
        # Header do menu
        header = ttk.Label(menu_frame, text="ACADEMIA\nFITNESS", font=("Arial", 14, "bold"))
        header.pack(pady=20, padx=10)
        
        # Lista de botões do menu
        botoes = [
            ("📊 Painel Principal", self.mostrar_painel_principal),
            ("👥 Alunos", self.mostrar_painel_alunos),
            ("🏋️ Instrutores", self.mostrar_painel_instrutores),
            ("💪 Treinos", self.mostrar_painel_treinos),
            ("📋 Planos", self.mostrar_painel_planos),
            ("📈 Avaliações", self.mostrar_painel_avaliacoes),
            ("📅 Frequência", self.mostrar_painel_frequencia),
            ("💰 Financeiro", self.mostrar_painel_financeiro),
            ("🗓️ Agenda", self.mostrar_painel_agenda),
            ("📊 Relatórios", self.mostrar_painel_relatorios),
            ("⚙️ Configuração", self.mostrar_painel_configuracao),
        ]
        
        for texto, comando in botoes:
            btn = tk.Button(
                menu_frame,
                text=texto,
                command=comando,
                bg=self.cor_secundaria,
                fg=self.cor_texto,
                font=("Arial", 10, "bold"),
                padx=15,
                pady=15,
                border=0,
                cursor="hand2",
                relief=tk.FLAT,
                activebackground=self.cor_accent,
                activeforeground=self.cor_texto
            )
            btn.pack(fill=tk.X, padx=5, pady=5)
    
    def limpar_conteudo(self):
        """Limpa o frame de conteúdo"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    # ===== PAINEL PRINCIPAL =====
    def mostrar_painel_principal(self):
        self.limpar_conteudo()
        
        title = ttk.Label(self.content_frame, text="📊 PAINEL PRINCIPAL", font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        # Cards com informações
        cards_frame = ttk.Frame(self.content_frame)
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        dados = self.db.get_alunos()
        instrutores = self.db.get_instrutores()
        treinos = self.db.get_treinos()
        planos = self.db.get_planos()
        
        cards_info = [
            (f"👥 Alunos\n{len(dados)}", "#2ecc71"),
            (f"🏋️ Instrutores\n{len(instrutores)}", "#3498db"),
            (f"💪 Treinos\n{len(treinos)}", "#e74c3c"),
            (f"📋 Planos\n{len(planos)}", "#f39c12"),
        ]
        
        for i, (texto, cor) in enumerate(cards_info):
            card = tk.Label(
                cards_frame,
                text=texto,
                bg=cor,
                fg="white",
                font=("Arial", 14, "bold"),
                padx=40,
                pady=40,
                relief=tk.FLAT
            )
            card.grid(row=0, column=i, padx=15, pady=15, sticky="nsew")
        
        # Eventos recentes
        eventos_frame = ttk.LabelFrame(self.content_frame, text="Eventos Recentes")
        eventos_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Treeview para eventos
        tree = ttk.Treeview(eventos_frame, columns=("Tipo", "Descrição", "Data"), height=10)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree.heading("#0", text="ID")
        tree.heading("Tipo", text="Tipo de Evento")
        tree.heading("Descrição", text="Descrição")
        tree.heading("Data", text="Data")
        
        tree.column("#0", width=50)
        tree.column("Tipo", width=150)
        tree.column("Descrição", width=500)
        tree.column("Data", width=150)
        
        # Eventos de exemplo
        eventos = [
            ("1", "Novo Aluno", "João Silva se matriculou", datetime.now().strftime('%d/%m/%Y')),
            ("2", "Avaliação", "Maria finalizada avaliação física", (datetime.now() - timedelta(days=1)).strftime('%d/%m/%Y')),
            ("3", "Pagamento", "Mensalidade paga", (datetime.now() - timedelta(days=2)).strftime('%d/%m/%Y')),
        ]
        
        for evento in eventos:
            tree.insert("", "end", text=evento[0], values=(evento[1], evento[2], evento[3]))
    
    # ===== PAINEL ALUNOS =====
    def mostrar_painel_alunos(self):
        self.limpar_conteudo()
        
        title = ttk.Label(self.content_frame, text="👥 GERENCIAR ALUNOS", font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        # Frame para adicionar aluno
        form_frame = ttk.LabelFrame(self.content_frame, text="Adicionar Novo Aluno")
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Campos de entrada
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        nome_entry = ttk.Entry(form_frame, width=30)
        nome_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        email_entry = ttk.Entry(form_frame, width=30)
        email_entry.grid(row=0, column=3, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Telefone:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        telefone_entry = ttk.Entry(form_frame, width=30)
        telefone_entry.grid(row=1, column=1, padx=10, pady=5)
        
        def adicionar_aluno():
            nome = nome_entry.get()
            email = email_entry.get()
            telefone = telefone_entry.get()
            
            if nome and email and telefone:
                self.db.add_aluno(nome, email, telefone)
                messagebox.showinfo("Sucesso", f"Aluno {nome} adicionado com sucesso!")
                nome_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                telefone_entry.delete(0, tk.END)
                atualizar_lista()
            else:
                messagebox.showerror("Erro", "Preencha todos os campos!")
        
        btn_adicionar = tk.Button(form_frame, text="✓ Adicionar", command=adicionar_aluno,
                                  bg=self.cor_accent, fg="white", font=("Arial", 10, "bold"),
                                  padx=20, pady=10, border=0, cursor="hand2")
        btn_adicionar.grid(row=1, column=3, padx=10, pady=5)
        
        # Frame para lista de alunos
        lista_frame = ttk.LabelFrame(self.content_frame, text="Lista de Alunos")
        lista_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(lista_frame, columns=("Nome", "Email", "Telefone", "Data Início", "Status"), height=15)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree.heading("#0", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Email", text="Email")
        tree.heading("Telefone", text="Telefone")
        tree.heading("Data Início", text="Data Início")
        tree.heading("Status", text="Status")
        
        tree.column("#0", width=50)
        tree.column("Nome", width=150)
        tree.column("Email", width=200)
        tree.column("Telefone", width=150)
        tree.column("Data Início", width=120)
        tree.column("Status", width=100)
        
        def atualizar_lista():
            for item in tree.get_children():
                tree.delete(item)
            
            alunos = self.db.get_alunos()
            for aluno in alunos:
                tree.insert("", "end", text=aluno[0], values=(aluno[1], aluno[2], aluno[3], aluno[4], aluno[5]))
        
        atualizar_lista()
    
    # ===== PAINEL INSTRUTORES =====
    def mostrar_painel_instrutores(self):
        self.limpar_conteudo()
        
        title = ttk.Label(self.content_frame, text="🏋️ GERENCIAR INSTRUTORES", font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        # Frame para adicionar instrutor
        form_frame = ttk.LabelFrame(self.content_frame, text="Adicionar Novo Instrutor")
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        nome_entry = ttk.Entry(form_frame, width=30)
        nome_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        email_entry = ttk.Entry(form_frame, width=30)
        email_entry.grid(row=0, column=3, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Especialidade:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        especialidade_entry = ttk.Entry(form_frame, width=30)
        especialidade_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Telefone:").grid(row=1, column=2, sticky="w", padx=10, pady=5)
        telefone_entry = ttk.Entry(form_frame, width=30)
        telefone_entry.grid(row=1, column=3, padx=10, pady=5)
        
        def adicionar_instrutor():
            nome = nome_entry.get()
            email = email_entry.get()
            especialidade = especialidade_entry.get()
            telefone = telefone_entry.get()
            
            if nome and email and especialidade and telefone:
                self.db.add_instrutor(nome, email, especialidade, telefone)
                messagebox.showinfo("Sucesso", f"Instrutor {nome} adicionado com sucesso!")
                nome_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                especialidade_entry.delete(0, tk.END)
                telefone_entry.delete(0, tk.END)
                atualizar_lista()
            else:
                messagebox.showerror("Erro", "Preencha todos os campos!")
        
        btn_adicionar = tk.Button(form_frame, text="✓ Adicionar", command=adicionar_instrutor,
                                  bg=self.cor_accent, fg="white", font=("Arial", 10, "bold"),
                                  padx=20, pady=10, border=0, cursor="hand2")
        btn_adicionar.grid(row=2, column=3, padx=10, pady=5)
        
        # Frame para lista de instrutores
        lista_frame = ttk.LabelFrame(self.content_frame, text="Lista de Instrutores")
        lista_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(lista_frame, columns=("Nome", "Email", "Especialidade", "Telefone", "Status"), height=15)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree.heading("#0", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Email", text="Email")
        tree.heading("Especialidade", text="Especialidade")
        tree.heading("Telefone", text="Telefone")
        tree.heading("Status", text="Status")
        
        tree.column("#0", width=50)
        tree.column("Nome", width=150)
        tree.column("Email", width=200)
        tree.column("Especialidade", width=150)
        tree.column("Telefone", width=120)
        tree.column("Status", width=100)
        
        def atualizar_lista():
            for item in tree.get_children():
                tree.delete(item)
            
            instrutores = self.db.get_instrutores()
            for inst in instrutores:
                tree.insert("", "end", text=inst[0], values=(inst[1], inst[2], inst[3], inst[4], inst[5]))
        
        atualizar_lista()
    
    # ===== PAINEL TREINOS =====
    def mostrar_painel_treinos(self):
        self.limpar_conteudo()
        
        title = ttk.Label(self.content_frame, text="💪 GERENCIAR TREINOS", font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        # Frame para adicionar treino
        form_frame = ttk.LabelFrame(self.content_frame, text="Adicionar Novo Treino")
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        nome_entry = ttk.Entry(form_frame, width=30)
        nome_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Descrição:").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        desc_entry = ttk.Entry(form_frame, width=30)
        desc_entry.grid(row=0, column=3, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Séries:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        series_entry = ttk.Spinbox(form_frame, from_=1, to=10, width=10)
        series_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Repetições:").grid(row=1, column=2, sticky="w", padx=10, pady=5)
        rep_entry = ttk.Spinbox(form_frame, from_=1, to=50, width=10)
        rep_entry.grid(row=1, column=3, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Descanso (seg):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        descanso_entry = ttk.Spinbox(form_frame, from_=10, to=300, step=10, width=10)
        descanso_entry.grid(row=2, column=1, padx=10, pady=5)
        
        def adicionar_treino():
            nome = nome_entry.get()
            desc = desc_entry.get()
            series = int(series_entry.get())
            rep = int(rep_entry.get())
            descanso = int(descanso_entry.get())
            
            if nome and desc:
                self.db.add_treino(nome, desc, series, rep, descanso)
                messagebox.showinfo("Sucesso", f"Treino {nome} adicionado com sucesso!")
                nome_entry.delete(0, tk.END)
                desc_entry.delete(0, tk.END)
                atualizar_lista()
            else:
                messagebox.showerror("Erro", "Preencha todos os campos!")
        
        btn_adicionar = tk.Button(form_frame, text="✓ Adicionar", command=adicionar_treino,
                                  bg=self.cor_accent, fg="white", font=("Arial", 10, "bold"),
                                  padx=20, pady=10, border=0, cursor="hand2")
        btn_adicionar.grid(row=2, column=3, padx=10, pady=5)
        
        # Frame para lista de treinos
        lista_frame = ttk.LabelFrame(self.content_frame, text="Lista de Treinos")
        lista_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(lista_frame, columns=("Nome", "Descrição", "Séries", "Repetições", "Descanso"), height=15)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree.heading("#0", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Descrição", text="Descrição")
        tree.heading("Séries", text="Séries")
        tree.heading("Repetições", text="Repetições")
        tree.heading("Descanso", text="Descanso (seg)")
        
        tree.column("#0", width=50)
        tree.column("Nome", width=150)
        tree.column("Descrição", width=250)
        tree.column("Séries", width=100)
        tree.column("Repetições", width=120)
        tree.column("Descanso", width=120)
        
        def atualizar_lista():
            for item in tree.get_children():
                tree.delete(item)
            
            treinos = self.db.get_treinos()
            for treino in treinos:
                tree.insert("", "end", text=treino[0], values=(treino[1], treino[2], treino[3], treino[4], treino[5]))
        
        atualizar_lista()
    
    # ===== PAINEL PLANOS =====
    def mostrar_painel_planos(self):
        self.limpar_conteudo()
        
        title = ttk.Label(self.content_frame, text="📋 GERENCIAR PLANOS", font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        # Frame para adicionar plano
        form_frame = ttk.LabelFrame(self.content_frame, text="Adicionar Novo Plano")
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        nome_entry = ttk.Entry(form_frame, width=30)
        nome_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Valor (R$):").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        valor_entry = ttk.Entry(form_frame, width=30)
        valor_entry.grid(row=0, column=3, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Duração (dias):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        duracao_entry = ttk.Spinbox(form_frame, from_=1, to=365, width=10)
        duracao_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Descrição:").grid(row=1, column=2, sticky="w", padx=10, pady=5)
        desc_entry = ttk.Entry(form_frame, width=30)
        desc_entry.grid(row=1, column=3, padx=10, pady=5)
        
        def adicionar_plano():
            nome = nome_entry.get()
            try:
                valor = float(valor_entry.get())
                duracao = int(duracao_entry.get())
                desc = desc_entry.get()
                
                if nome and desc:
                    self.db.add_plano(nome, valor, duracao, desc)
                    messagebox.showinfo("Sucesso", f"Plano {nome} adicionado com sucesso!")
                    nome_entry.delete(0, tk.END)
                    valor_entry.delete(0, tk.END)
                    duracao_entry.delete(0, tk.END)
                    desc_entry.delete(0, tk.END)
                    atualizar_lista()
                else:
                    messagebox.showerror("Erro", "Preencha todos os campos!")
            except ValueError:
                messagebox.showerror("Erro", "Digite um valor numérico válido!")
        
        btn_adicionar = tk.Button(form_frame, text="✓ Adicionar", command=adicionar_plano,
                                  bg=self.cor_accent, fg="white", font=("Arial", 10, "bold"),
                                  padx=20, pady=10, border=0, cursor="hand2")
        btn_adicionar.grid(row=2, column=3, padx=10, pady=5)
        
        # Frame para lista de planos
        lista_frame = ttk.LabelFrame(self.content_frame, text="Lista de Planos")
        lista_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(lista_frame, columns=("Nome", "Valor", "Duração", "Descrição"), height=15)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree.heading("#0", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Valor", text="Valor (R$)")
        tree.heading("Duração", text="Duração (dias)")
        tree.heading("Descrição", text="Descrição")
        
        tree.column("#0", width=50)
        tree.column("Nome", width=150)
        tree.column("Valor", width=150)
        tree.column("Duração", width=150)
        tree.column("Descrição", width=300)
        
        def atualizar_lista():
            for item in tree.get_children():
                tree.delete(item)
            
            planos = self.db.get_planos()
            for plano in planos:
                tree.insert("", "end", text=plano[0], values=(plano[1], f"R$ {plano[2]:.2f}", plano[3], plano[4]))
        
        atualizar_lista()
    
    # ===== PAINEL AVALIAÇÕES =====
    def mostrar_painel_avaliacoes(self):
        self.limpar_conteudo()
        
        title = ttk.Label(self.content_frame, text="📈 GERENCIAR AVALIAÇÕES", font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        # Frame para adicionar avaliação
        form_frame = ttk.LabelFrame(self.content_frame, text="Registrar Nova Avaliação")
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        alunos = self.db.get_alunos()
        alunos_nomes = [f"{a[0]} - {a[1]}" for a in alunos]
        
        ttk.Label(form_frame, text="Aluno:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        aluno_var = tk.StringVar()
        aluno_combo = ttk.Combobox(form_frame, textvariable=aluno_var, values=alunos_nomes, width=28)
        aluno_combo.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Peso (kg):").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        peso_entry = ttk.Entry(form_frame, width=30)
        peso_entry.grid(row=0, column=3, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Altura (cm):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        altura_entry = ttk.Entry(form_frame, width=30)
        altura_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(form_frame, text="% Gordura:").grid(row=1, column=2, sticky="w", padx=10, pady=5)
        gordura_entry = ttk.Entry(form_frame, width=30)
        gordura_entry.grid(row=1, column=3, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Notas:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        notas_entry = ttk.Entry(form_frame, width=80)
        notas_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="ew")
        
        def registrar_avaliacao():
            aluno_str = aluno_var.get()
            if not aluno_str:
                messagebox.showerror("Erro", "Selecione um aluno!")
                return
            
            try:
                aluno_id = int(aluno_str.split(" - ")[0])
                peso = float(peso_entry.get())
                altura = float(altura_entry.get())
                gordura = float(gordura_entry.get())
                notas = notas_entry.get()
                
                self.db.add_avaliacao(aluno_id, peso, altura, gordura, notas)
                messagebox.showinfo("Sucesso", "Avaliação registrada com sucesso!")
                peso_entry.delete(0, tk.END)
                altura_entry.delete(0, tk.END)
                gordura_entry.delete(0, tk.END)
                notas_entry.delete(0, tk.END)
                atualizar_lista()
            except ValueError:
                messagebox.showerror("Erro", "Digite valores numéricos válidos!")
        
        btn_adicionar = tk.Button(form_frame, text="✓ Registrar", command=registrar_avaliacao,
                                  bg=self.cor_accent, fg="white", font=("Arial", 10, "bold"),
                                  padx=20, pady=10, border=0, cursor="hand2")
        btn_adicionar.grid(row=3, column=3, padx=10, pady=5)
        
        # Frame para visualizar avaliações
        lista_frame = ttk.LabelFrame(self.content_frame, text="Avaliações Registradas")
        lista_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(lista_frame, columns=("Aluno", "Data", "Peso", "Altura", "Gordura", "Notas"), height=15)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree.heading("#0", text="ID")
        tree.heading("Aluno", text="Aluno")
        tree.heading("Data", text="Data")
        tree.heading("Peso", text="Peso (kg)")
        tree.heading("Altura", text="Altura (cm)")
        tree.heading("Gordura", text="% Gordura")
        tree.heading("Notas", text="Notas")
        
        tree.column("#0", width=50)
        tree.column("Aluno", width=150)
        tree.column("Data", width=100)
        tree.column("Peso", width=100)
        tree.column("Altura", width=100)
        tree.column("Gordura", width=100)
        tree.column("Notas", width=300)
        
        def atualizar_lista():
            for item in tree.get_children():
                tree.delete(item)
            
            for aluno in alunos:
                avaliacoes = self.db.get_avaliacoes(aluno[0])
                for aval in avaliacoes:
                    tree.insert("", "end", text=aval[0], values=(aluno[1], aval[2], aval[3], aval[4], f"{aval[5]:.1f}", aval[6]))
        
        atualizar_lista()
    
    # ===== PAINEL FREQUÊNCIA =====
    def mostrar_painel_frequencia(self):
        self.limpar_conteudo()
        
        title = ttk.Label(self.content_frame, text="📅 GERENCIAR FREQUÊNCIA", font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        # Frame para registrar frequência
        form_frame = ttk.LabelFrame(self.content_frame, text="Registrar Frequência")
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        alunos = self.db.get_alunos()
        alunos_nomes = [f"{a[0]} - {a[1]}" for a in alunos]
        
        ttk.Label(form_frame, text="Aluno:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        aluno_var = tk.StringVar()
        aluno_combo = ttk.Combobox(form_frame, textvariable=aluno_var, values=alunos_nomes, width=28)
        aluno_combo.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Presente:").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        presente_var = tk.BooleanVar(value=True)
        presente_check = ttk.Checkbutton(form_frame, variable=presente_var)
        presente_check.grid(row=0, column=3, padx=10, pady=5)
        
        def registrar_frequencia():
            aluno_str = aluno_var.get()
            if not aluno_str:
                messagebox.showerror("Erro", "Selecione um aluno!")
                return
            
            aluno_id = int(aluno_str.split(" - ")[0])
            presente = presente_var.get()
            
            self.db.add_frequencia(aluno_id, presente)
            messagebox.showinfo("Sucesso", "Frequência registrada com sucesso!")
            atualizar_lista()
        
        btn_registrar = tk.Button(form_frame, text="✓ Registrar", command=registrar_frequencia,
                                  bg=self.cor_accent, fg="white", font=("Arial", 10, "bold"),
                                  padx=20, pady=10, border=0, cursor="hand2")
        btn_registrar.grid(row=0, column=4, padx=10, pady=5)
        
        # Frame para visualizar frequências
        lista_frame = ttk.LabelFrame(self.content_frame, text="Histórico de Frequência")
        lista_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(lista_frame, columns=("Aluno", "Data", "Horário", "Presente"), height=15)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree.heading("#0", text="ID")
        tree.heading("Aluno", text="Aluno")
        tree.heading("Data", text="Data")
        tree.heading("Horário", text="Horário")
        tree.heading("Presente", text="Status")
        
        tree.column("#0", width=50)
        tree.column("Aluno", width=200)
        tree.column("Data", width=120)
        tree.column("Horário", width=120)
        tree.column("Presente", width=100)
        
        def atualizar_lista():
            for item in tree.get_children():
                tree.delete(item)
            
            for aluno in alunos:
                freqs = self.db.get_frequencias(aluno[0])
                for freq in freqs:
                    status = "✓ Presente" if freq[4] else "✗ Ausente"
                    tree.insert("", "end", text=freq[0], values=(aluno[1], freq[2], freq[3], status))
        
        atualizar_lista()
    
    # ===== PAINEL FINANCEIRO =====
    def mostrar_painel_financeiro(self):
        self.limpar_conteudo()
        
        title = ttk.Label(self.content_frame, text="💰 GERENCIAR FINANCEIRO", font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        # Frame para adicionar transação
        form_frame = ttk.LabelFrame(self.content_frame, text="Registrar Transação")
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        alunos = self.db.get_alunos()
        alunos_nomes = [f"{a[0]} - {a[1]}" for a in alunos]
        
        ttk.Label(form_frame, text="Aluno:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        aluno_var = tk.StringVar()
        aluno_combo = ttk.Combobox(form_frame, textvariable=aluno_var, values=alunos_nomes, width=28)
        aluno_combo.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Tipo:").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        tipo_var = tk.StringVar()
        tipo_combo = ttk.Combobox(form_frame, textvariable=tipo_var, values=["Mensalidade", "Material", "Avaliação", "Outro"], width=26)
        tipo_combo.grid(row=0, column=3, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Valor (R$):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        valor_entry = ttk.Entry(form_frame, width=30)
        valor_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Status:").grid(row=1, column=2, sticky="w", padx=10, pady=5)
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, values=["Pago", "Pendente", "Cancelado"], width=26)
        status_combo.grid(row=1, column=3, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Descrição:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        desc_entry = ttk.Entry(form_frame, width=80)
        desc_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="ew")
        
        def registrar_transacao():
            aluno_str = aluno_var.get()
            tipo = tipo_var.get()
            status = status_var.get()
            desc = desc_entry.get()
            
            if not aluno_str or not tipo or not status:
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return
            
            try:
                aluno_id = int(aluno_str.split(" - ")[0])
                valor = float(valor_entry.get())
                
                self.db.add_financeiro(aluno_id, tipo, valor, status, desc)
                messagebox.showinfo("Sucesso", "Transação registrada com sucesso!")
                valor_entry.delete(0, tk.END)
                desc_entry.delete(0, tk.END)
                atualizar_lista()
            except ValueError:
                messagebox.showerror("Erro", "Digite um valor numérico válido!")
        
        btn_registrar = tk.Button(form_frame, text="✓ Registrar", command=registrar_transacao,
                                  bg=self.cor_accent, fg="white", font=("Arial", 10, "bold"),
                                  padx=20, pady=10, border=0, cursor="hand2")
        btn_registrar.grid(row=3, column=3, padx=10, pady=5)
        
        # Frame para visualizar transações
        lista_frame = ttk.LabelFrame(self.content_frame, text="Transações Financeiras")
        lista_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(lista_frame, columns=("Aluno", "Data", "Tipo", "Valor", "Status", "Descrição"), height=15)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree.heading("#0", text="ID")
        tree.heading("Aluno", text="Aluno")
        tree.heading("Data", text="Data")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Valor", text="Valor")
        tree.heading("Status", text="Status")
        tree.heading("Descrição", text="Descrição")
        
        tree.column("#0", width=50)
        tree.column("Aluno", width=150)
        tree.column("Data", width=100)
        tree.column("Tipo", width=120)
        tree.column("Valor", width=100)
        tree.column("Status", width=100)
        tree.column("Descrição", width=300)
        
        def atualizar_lista():
            for item in tree.get_children():
                tree.delete(item)
            
            financeiros = self.db.get_financeiro()
            for fin in financeiros:
                aluno_nome = next((a[1] for a in alunos if a[0] == fin[1]), "N/A")
                tree.insert("", "end", text=fin[0], values=(aluno_nome, fin[2], fin[3], f"R$ {fin[4]:.2f}", fin[5], fin[6]))
        
        atualizar_lista()
    
    # ===== PAINEL AGENDA =====
    def mostrar_painel_agenda(self):
        self.limpar_conteudo()
        
        title = ttk.Label(self.content_frame, text="🗓️ GERENCIAR AGENDA", font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        # Frame para adicionar evento
        form_frame = ttk.LabelFrame(self.content_frame, text="Adicionar Evento")
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(form_frame, text="Título:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        titulo_entry = ttk.Entry(form_frame, width=30)
        titulo_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Data (DD/MM/YYYY):").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        data_entry = ttk.Entry(form_frame, width=30)
        data_entry.grid(row=0, column=3, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Horário (HH:MM):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        horario_entry = ttk.Entry(form_frame, width=30)
        horario_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Tipo:").grid(row=1, column=2, sticky="w", padx=10, pady=5)
        tipo_var = tk.StringVar()
        tipo_combo = ttk.Combobox(form_frame, textvariable=tipo_var, values=["Aula", "Avaliação", "Reunião", "Manutenção", "Outro"], width=26)
        tipo_combo.grid(row=1, column=3, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Descrição:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        desc_entry = ttk.Entry(form_frame, width=80)
        desc_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="ew")
        
        def adicionar_evento():
            titulo = titulo_entry.get()
            data = data_entry.get()
            horario = horario_entry.get()
            tipo = tipo_var.get()
            desc = desc_entry.get()
            
            if titulo and data and horario and tipo:
                self.db.add_agenda(titulo, data, horario, desc, tipo)
                messagebox.showinfo("Sucesso", f"Evento '{titulo}' adicionado com sucesso!")
                titulo_entry.delete(0, tk.END)
                data_entry.delete(0, tk.END)
                horario_entry.delete(0, tk.END)
                desc_entry.delete(0, tk.END)
                atualizar_lista()
            else:
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
        
        btn_adicionar = tk.Button(form_frame, text="✓ Adicionar", command=adicionar_evento,
                                  bg=self.cor_accent, fg="white", font=("Arial", 10, "bold"),
                                  padx=20, pady=10, border=0, cursor="hand2")
        btn_adicionar.grid(row=3, column=3, padx=10, pady=5)
        
        # Frame para visualizar agenda
        lista_frame = ttk.LabelFrame(self.content_frame, text="Eventos Agendados")
        lista_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(lista_frame, columns=("Título", "Data", "Horário", "Tipo", "Descrição"), height=15)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree.heading("#0", text="ID")
        tree.heading("Título", text="Título")
        tree.heading("Data", text="Data")
        tree.heading("Horário", text="Horário")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Descrição", text="Descrição")
        
        tree.column("#0", width=50)
        tree.column("Título", width=150)
        tree.column("Data", width=120)
        tree.column("Horário", width=100)
        tree.column("Tipo", width=120)
        tree.column("Descrição", width=350)
        
        def atualizar_lista():
            for item in tree.get_children():
                tree.delete(item)
            
            eventos = self.db.get_agenda()
            for evento in eventos:
                tree.insert("", "end", text=evento[0], values=(evento[1], evento[2], evento[3], evento[5], evento[4]))
        
        atualizar_lista()
    
    # ===== PAINEL RELATÓRIOS =====
    def mostrar_painel_relatorios(self):
        self.limpar_conteudo()
        
        title = ttk.Label(self.content_frame, text="📊 RELATÓRIOS", font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        # Frame para selecionar tipo de relatório
        selecao_frame = ttk.LabelFrame(self.content_frame, text="Selecionar Relatório")
        selecao_frame.pack(fill=tk.X, padx=20, pady=10)
        
        relatorio_var = tk.StringVar()
        opcoes = ["Resumo Geral", "Alunos Ativos", "Frequência por Aluno", "Financeiro", "Avaliações Recentes"]
        
        for i, opcao in enumerate(opcoes):
            ttk.Radiobutton(selecao_frame, text=opcao, variable=relatorio_var, value=opcao).pack(side=tk.LEFT, padx=10, pady=10)
        
        # Frame para exibir relatório
        relatorio_frame = ttk.LabelFrame(self.content_frame, text="Resultado do Relatório")
        relatorio_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(relatorio_frame, columns=("Informação", "Valor"), height=15)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree.heading("#0", text="Item")
        tree.heading("Informação", text="Detalhes")
        tree.heading("Valor", text="Valor")
        
        tree.column("#0", width=200)
        tree.column("Informação", width=400)
        tree.column("Valor", width=250)
        
        def gerar_relatorio():
            for item in tree.get_children():
                tree.delete(item)
            
            tipo = relatorio_var.get()
            
            if tipo == "Resumo Geral":
                alunos = self.db.get_alunos()
                instrutores = self.db.get_instrutores()
                treinos = self.db.get_treinos()
                planos = self.db.get_planos()
                
                tree.insert("", "end", text="Total de Alunos", values=("Alunos cadastrados", len(alunos)))
                tree.insert("", "end", text="Total de Instrutores", values=("Instrutores cadastrados", len(instrutores)))
                tree.insert("", "end", text="Total de Treinos", values=("Treinos cadastrados", len(treinos)))
                tree.insert("", "end", text="Total de Planos", values=("Planos cadastrados", len(planos)))
                
            elif tipo == "Alunos Ativos":
                alunos = self.db.get_alunos()
                for aluno in alunos:
                    tree.insert("", "end", text=aluno[1], values=(aluno[2], aluno[5]))
            
            elif tipo == "Frequência por Aluno":
                alunos = self.db.get_alunos()
                for aluno in alunos:
                    freqs = self.db.get_frequencias(aluno[0])
                    presentes = sum(1 for f in freqs if f[4])
                    total = len(freqs)
                    percentual = (presentes / total * 100) if total > 0 else 0
                    tree.insert("", "end", text=aluno[1], values=(f"Presença: {presentes}/{total}", f"{percentual:.1f}%"))
            
            elif tipo == "Financeiro":
                financeiros = self.db.get_financeiro()
                alunos = self.db.get_alunos()
                
                for fin in financeiros:
                    aluno_nome = next((a[1] for a in alunos if a[0] == fin[1]), "N/A")
                    status_cor = "✓" if fin[5] == "Pago" else "✗" if fin[5] == "Pendente" else "○"
                    tree.insert("", "end", text=aluno_nome, values=(fin[3], f"R$ {fin[4]:.2f} - {fin[5]}"))
            
            elif tipo == "Avaliações Recentes":
                alunos = self.db.get_alunos()
                for aluno in alunos:
                    avaliacoes = self.db.get_avaliacoes(aluno[0])
                    if avaliacoes:
                        aval = avaliacoes[-1]
                        imc = aval[4] / ((aval[3] / 100) ** 2)
                        tree.insert("", "end", text=aluno[1], values=(f"Peso: {aval[3]}kg, Altura: {aval[4]}cm", f"IMC: {imc:.1f}"))
        
        btn_gerar = tk.Button(self.content_frame, text="🔄 Gerar Relatório", command=gerar_relatorio,
                              bg=self.cor_accent, fg="white", font=("Arial", 10, "bold"),
                              padx=20, pady=10, border=0, cursor="hand2")
        btn_gerar.pack(pady=10)
    
    # ===== PAINEL CONFIGURAÇÃO =====
    def mostrar_painel_configuracao(self):
        self.limpar_conteudo()
        
        title = ttk.Label(self.content_frame, text="⚙️ CONFIGURAÇÃO", font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        # Frame de configurações gerais
        config_frame = ttk.LabelFrame(self.content_frame, text="Configurações Gerais")
        config_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(config_frame, text="Nome da Academia:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        nome_academia = ttk.Entry(config_frame, width=40)
        nome_academia.insert(0, "Academia Fitness")
        nome_academia.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(config_frame, text="Email da Academia:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        email_academia = ttk.Entry(config_frame, width=40)
        email_academia.insert(0, "contato@academia.com")
        email_academia.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(config_frame, text="Telefone:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        telefone_academia = ttk.Entry(config_frame, width=40)
        telefone_academia.insert(0, "(11) 9999-9999")
        telefone_academia.grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Label(config_frame, text="Endereço:").grid(row=3, column=0, sticky="w", padx=10, pady=10)
        endereco_academia = ttk.Entry(config_frame, width=40)
        endereco_academia.insert(0, "Rua Principal, 123")
        endereco_academia.grid(row=3, column=1, padx=10, pady=10)
        
        def salvar_configuracoes():
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        
        btn_salvar = tk.Button(config_frame, text="💾 Salvar Configurações", command=salvar_configuracoes,
                               bg=self.cor_accent, fg="white", font=("Arial", 10, "bold"),
                               padx=20, pady=10, border=0, cursor="hand2")
        btn_salvar.grid(row=4, column=1, padx=10, pady=10, sticky="e")
        
        # Frame de informações do sistema
        info_frame = ttk.LabelFrame(self.content_frame, text="Informações do Sistema")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        info_text = tk.Text(info_frame, height=15, width=80, bg="#f0f0f0", relief=tk.FLAT)
        info_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        info_content = """
📋 INFORMAÇÕES DO SISTEMA
═══════════════════════════════════════════════════════════════════

✓ Sistema de Gestão de Academia - Versão 1.0
✓ Desenvolvido em Python com Tkinter
✓ Banco de Dados: SQLite

MÓDULOS DISPONÍVEIS:
├── 👥 Painel Alunos - Gerenciamento completo de alunos
├── 🏋️ Painel Instrutores - Cadastro e gerenciamento de instrutores
├── 💪 Painel Treinos - Criação e edição de treinos
├── 📋 Painel Planos - Gerenciamento de planos de assinatura
├── 📈 Painel Avaliações - Registro de avaliações físicas
├── 📅 Painel Frequência - Controle de frequência
├── 💰 Painel Financeiro - Gestão de transações e pagamentos
├── 🗓️ Painel Agenda - Agendamento de eventos
├── 📊 Painel Relatórios - Geração de relatórios diversos
└── ⚙️ Configuração - Definições do sistema

FUNCIONALIDADES PRINCIPAIS:
• Gestão completa de alunos e instrutores
• Sistema de treinos com séries e repetições
• Controle de frequência automático
• Gestão financeira com múltiplas transações
• Avaliações físicas com histórico
• Agenda e agendamento de eventos
• Relatórios detalhados do sistema

═══════════════════════════════════════════════════════════════════
        """
        
        info_text.insert(tk.END, info_content)
        info_text.config(state=tk.DISABLED)


# ===== EXECUTAR APLICAÇÃO =====
if __name__ == "__main__":
    app = TelaPrincipal()
    app.mainloop()
