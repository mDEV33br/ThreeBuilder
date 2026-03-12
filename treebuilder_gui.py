import os
import tkinter as tk
from tkinter import filedialog, messagebox


APP_TITLE = "TreeBuilder v1.2"
APP_DESC = "Gerador de Estrutura de Pastas e Arquivos - Ferramenta para criar rapidamente estruturas de projetos a partir de árvores de diretórios"


class TreeBuilderApp:

    def __init__(self, root):

        self.root = root
        root.title(APP_TITLE)
        root.geometry("600x520")
        root.resizable(False, False)

        # ----------------------------
        # Título
        # ----------------------------

        titulo = tk.Label(
            root,
            text=APP_TITLE,
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=(10, 0))

        descricao = tk.Label(
            root,
            text=APP_DESC,
            font=("Arial", 9)
        )
        descricao.pack(pady=(0, 10))

        # ----------------------------
        # Passo 1
        # ----------------------------

        passo1 = tk.Frame(root)
        passo1.pack(fill="x", padx=10)

        label1 = tk.Label(
            passo1,
            text="1️⃣ Cole sua estrutura no campo abaixo ou carregue um arquivo .txt"
        )
        label1.pack(side="left")

        botao_carregar = tk.Button(
            passo1,
            text="Carregar .txt",
            command=self.carregar_txt
        )
        botao_carregar.pack(side="right")

        # ----------------------------
        # Passo 2
        # ----------------------------

        label2 = tk.Label(
            root,
            text="2️⃣ Escolha a pasta onde deseja criar a estrutura"
        )
        label2.pack(anchor="w", padx=10, pady=(5, 0))

        self.pasta_destino = tk.Entry(root)
        self.pasta_destino.pack(fill="x", padx=10, pady=5)

        botao_pasta = tk.Button(
            root,
            text="Selecionar Pasta",
            command=self.selecionar_pasta
        )
        botao_pasta.pack(pady=(0, 10))

        # ----------------------------
        # Editor
        # ----------------------------

        label_editor = tk.Label(
            root,
            text="Cole aqui a estrutura a ser criada:"
        )
        label_editor.pack(anchor="w", padx=10)

        frame_editor = tk.Frame(root)
        frame_editor.pack(fill="both", expand=True, padx=10)

        self.editor = tk.Text(frame_editor, height=14)
        self.editor.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_editor, command=self.editor.yview)
        scrollbar.pack(side="right", fill="y")

        self.editor.config(yscrollcommand=scrollbar.set)

        # ----------------------------
        # Botões
        # ----------------------------

        frame_botoes = tk.Frame(root)
        frame_botoes.pack(pady=10)

        botao_criar = tk.Button(
            frame_botoes,
            text="Criar Estrutura",
            width=20,
            command=self.criar_estrutura
        )
        botao_criar.grid(row=0, column=0, padx=5)

        botao_exemplo = tk.Button(
            frame_botoes,
            text="Exemplo de Estrutura",
            width=20,
            command=self.exemplo
        )
        botao_exemplo.grid(row=0, column=1, padx=5)

        botao_limpar = tk.Button(
            frame_botoes,
            text="Limpar Editor",
            width=20,
            command=self.limpar_editor
        )
        botao_limpar.grid(row=0, column=2, padx=5)

        # ----------------------------
        # Rodapé
        # ----------------------------

        rodape = tk.Label(
            root,
            text="Projeto open source",
            font=("Arial", 8)
        )
        rodape.pack(pady=(0, 10))

        # ----------------------------
        # Menu
        # ----------------------------

        menu = tk.Menu(root)
        root.config(menu=menu)

        menu_arquivo = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Arquivo", menu=menu_arquivo)

        menu_arquivo.add_command(label="Carregar .txt", command=self.carregar_txt)
        menu_arquivo.add_command(label="Limpar Editor", command=self.limpar_editor)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=root.quit)

        menu_ajuda = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Ajuda", menu=menu_ajuda)

        menu_ajuda.add_command(label="Sobre", command=self.sobre)

    # -----------------------------------------------------

    def selecionar_pasta(self):

        pasta = filedialog.askdirectory()

        if pasta:
            self.pasta_destino.delete(0, tk.END)
            self.pasta_destino.insert(0, pasta)

    # -----------------------------------------------------

    def carregar_txt(self):

        arquivo = filedialog.askopenfilename(
            filetypes=[("Arquivos de texto", "*.txt")]
        )

        if not arquivo:
            return

        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()

        self.editor.delete("1.0", tk.END)
        self.editor.insert(tk.END, conteudo)

    # -----------------------------------------------------

    def limpar_editor(self):

        self.editor.delete("1.0", tk.END)

    # -----------------------------------------------------

    def exemplo(self):

        exemplo = """ProjetoExemplo/
├── main.py
├── README.md
├── requirements.txt
├── src/
│   ├── app.py
│   └── utils.py
├── tests/
│   └── test_app.py
└── docs/
    └── manual.md
"""

        self.editor.delete("1.0", tk.END)
        self.editor.insert(tk.END, exemplo)

    # -----------------------------------------------------

    def sobre(self):

        texto = """
TreeBuilder v1.2

Ferramenta open source para gerar rapidamente
estruturas de pastas e arquivos.

Autor:
Moisés Felipe Costa Carvalho

GitHub:
https://github.com/mDEV33br

Contato:
moisescarvalho33@gmail.com
"""

        messagebox.showinfo("Sobre", texto)

    # -----------------------------------------------------

    def criar_estrutura(self):

        destino = self.pasta_destino.get().strip()

        if not destino:
            messagebox.showerror("Erro", "Selecione uma pasta destino.")
            return

        linhas = self.editor.get("1.0", tk.END).splitlines()

        pilha = []

        for linha in linhas:

            linha = linha.rstrip()

            if not linha:
                continue

            # Ignorar comentários
            if linha.strip().startswith("#"):
                continue

            # Ignorar textos explicativos
            if linha.strip().startswith("("):
                continue

            nivel = linha.count("│")

            nome = linha.replace("│", "")
            nome = nome.replace("├──", "")
            nome = nome.replace("└──", "")
            nome = nome.strip()

            if not nome:
                continue

            if nivel == 0:

                caminho = os.path.join(destino, nome)

                if nome.endswith("/"):
                    os.makedirs(caminho, exist_ok=True)
                else:
                    open(caminho, "a").close()

                pilha = [(nivel, caminho)]

                continue

            while pilha and pilha[-1][0] >= nivel:
                pilha.pop()

            if not pilha:
                continue

            caminho_pai = pilha[-1][1]

            caminho = os.path.join(caminho_pai, nome)

            if nome.endswith("/"):

                os.makedirs(caminho, exist_ok=True)

                pilha.append((nivel, caminho))

            else:

                open(caminho, "a").close()

        messagebox.showinfo("Sucesso", "Estrutura criada com sucesso!")


# ---------------------------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = TreeBuilderApp(root)

    root.mainloop()
