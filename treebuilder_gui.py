import os
import base64
import tkinter as tk
from tkinter import filedialog, messagebox

# ======================================
# Ícone embutido
# ======================================

ICON_BASE64 = """
iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAQAAAAAYLlVAAAAl0lEQVR4Ae3WMQ6AIAxE0Xv/p9sE
xCBrum1BgFiSVqSogn+CA0nVddOcxXS6AMDttuPAoBs+K6TfGsDz3jACzmwVsQtAT5ArhcXd1LSe
BF3nf6/DrATguPmyAnbcDFSyCYwiVQi+GqOR/mdrIW6DCQE4kMAAETaGEKMFAAAi6iKCCGGAACoo
IoIYYAAKiiighhgAAqKKKCGGAAAqKCKCGGAACooIoIYYAAKiiighhgAAqKKKCGGAAAqKCKCGGAAAq
qA9H0AB2T9nS3AAAAABJRU5ErkJggg==
"""

def aplicar_icone(janela):
    try:
        icon_data = base64.b64decode(ICON_BASE64)
        icon = tk.PhotoImage(data=icon_data)
        janela.iconphoto(True, icon)
    except:
        pass


# ======================================
# Interpretar estrutura
# ======================================

def interpretar_arvore(texto):

    linhas = texto.splitlines()
    estrutura = []

    for linha in linhas:

        linha = linha.rstrip()

        if not linha.strip():
            continue

        nivel = linha.count("│") + linha.count("    ")

        nome = (
            linha.replace("├──", "")
            .replace("└──", "")
            .replace("│", "")
            .strip()
        )

        estrutura.append((nivel, nome))

    return estrutura


# ======================================
# Criar estrutura
# ======================================

def criar_estrutura():

    texto = area_texto.get("1.0", tk.END)

    if not texto.strip():
        messagebox.showwarning("Aviso", "Cole ou carregue uma estrutura primeiro.")
        return

    pasta_destino = filedialog.askdirectory(title="Escolha onde criar o projeto")

    if not pasta_destino:
        return

    estrutura = interpretar_arvore(texto)

    raiz = estrutura[0][1]
    caminho_raiz = os.path.join(pasta_destino, raiz)

    try:
        os.makedirs(caminho_raiz, exist_ok=True)
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return

    pilha = [(0, caminho_raiz)]

    for nivel, nome in estrutura[1:]:

        while pilha and pilha[-1][0] >= nivel:
            pilha.pop()

        caminho_pai = pilha[-1][1]
        caminho_atual = os.path.join(caminho_pai, nome)

        if "." in nome:
            open(caminho_atual, "w").close()
        else:
            os.makedirs(caminho_atual, exist_ok=True)

        pilha.append((nivel, caminho_atual))

    messagebox.showinfo("Sucesso", f"Estrutura criada em:\n{caminho_raiz}")


# ======================================
# Utilitários
# ======================================

def carregar_arquivo():

    caminho = filedialog.askopenfilename(
        title="Selecionar arquivo",
        filetypes=[("Arquivos de texto", "*.txt")]
    )

    if not caminho:
        return

    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()

    area_texto.delete("1.0", tk.END)
    area_texto.insert(tk.END, conteudo)


def exemplo_estrutura():

    exemplo = """
meu_projeto/
├── app/
│   ├── main.py
│   ├── auth.py
│   └── utils.py
├── data/
├── output/
├── logs/
└── README.md
"""

    area_texto.delete("1.0", tk.END)
    area_texto.insert(tk.END, exemplo.strip())


def limpar_editor():
    area_texto.delete("1.0", tk.END)


def sobre():

    messagebox.showinfo(
        "Sobre o TreeBuilder",
        """
TreeBuilder v1.1

Autor:
Moisés Felipe Costa Carvalho

Email:
moisescarvalho33@gmail.com

GitHub:
https://github.com/mDEV33br

Ferramenta open source para geração
de estruturas de projetos.
"""
    )


# ======================================
# Interface
# ======================================

janela = tk.Tk()
janela.title("TreeBuilder v1.1")
janela.geometry("700x500")
janela.resizable(False, False)

aplicar_icone(janela)


# ======================================
# Menu
# ======================================

menu_bar = tk.Menu(janela)

menu_arquivo = tk.Menu(menu_bar, tearoff=0)
menu_arquivo.add_command(label="Sair", command=janela.quit)
menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)

menu_ajuda = tk.Menu(menu_bar, tearoff=0)
menu_ajuda.add_command(label="Sobre", command=sobre)
menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)

janela.config(menu=menu_bar)


# ======================================
# Título
# ======================================

titulo = tk.Label(
    janela,
    text="TreeBuilder v1.1",
    font=("Arial", 18, "bold")
)

titulo.pack(pady=(8,2))


descricao = tk.Label(
    janela,
    text="Gerador de Estrutura de Pastas e Arquivos\nFerramenta para criar rapidamente estruturas de projetos a partir de árvores de diretórios",
    font=("Arial", 9),
    justify="center"
)

descricao.pack(pady=(0,6))


# ======================================
# PASSO 1
# ======================================

frame_passo1 = tk.Frame(janela)
frame_passo1.pack(pady=2)

label_passo1 = tk.Label(
    frame_passo1,
    text="PASSO 1: Cole sua estrutura ou carregue um arquivo *.txt",
    font=("Arial", 9)
)

label_passo1.grid(row=0, column=0, padx=5)

botao_carregar = tk.Button(
    frame_passo1,
    text="Carregar arquivo .txt",
    command=carregar_arquivo
)

botao_carregar.grid(row=0, column=1, padx=5)


# ======================================
# PASSO 2
# ======================================

label_passo2 = tk.Label(
    janela,
    text="PASSO 2: Clique em 'Criar Estrutura' e escolha a pasta onde o projeto será criado.",
    font=("Arial", 9)
)

label_passo2.pack(pady=2)


# ======================================
# Editor com Scroll
# ======================================

label_editor = tk.Label(
    janela,
    text="Cole aqui a estrutura a ser criada:",
    font=("Arial", 9, "bold")
)

label_editor.pack()

frame_editor = tk.Frame(janela)
frame_editor.pack(padx=10, pady=6)

scrollbar = tk.Scrollbar(frame_editor)

area_texto = tk.Text(
    frame_editor,
    height=14,
    width=80,
    yscrollcommand=scrollbar.set
)

scrollbar.config(command=area_texto.yview)

scrollbar.pack(side="right", fill="y")
area_texto.pack(side="left", fill="both")


# ======================================
# Botões
# ======================================

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=3)

botao_criar = tk.Button(
    frame_botoes,
    text="Criar Estrutura",
    width=18,
    command=criar_estrutura
)

botao_criar.grid(row=0, column=0, padx=5)

botao_exemplo = tk.Button(
    frame_botoes,
    text="Exemplo de Estrutura",
    width=18,
    command=exemplo_estrutura
)

botao_exemplo.grid(row=0, column=1, padx=5)

botao_limpar = tk.Button(
    frame_botoes,
    text="Limpar Editor",
    width=18,
    command=limpar_editor
)

botao_limpar.grid(row=0, column=2, padx=5)


# ======================================
# Rodapé
# ======================================

rodape = tk.Label(
    janela,
    text="Projeto open source",
    font=("Arial", 8)
)

rodape.pack(pady=3)


janela.mainloop()