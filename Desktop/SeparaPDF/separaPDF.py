import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter

arquivo_pdf = ""
pasta_destino = ""

def parse_paginas(texto, total_paginas):
    paginas = set()
    partes = texto.replace(" ", "").split(',')
    for parte in partes:
        if '-' in parte:
            inicio, fim = parte.split('-')
            paginas.update(range(int(inicio), int(fim)+1))
        else:
            paginas.add(int(parte))
    return sorted([p for p in paginas if 1 <= p <= total_paginas])

def selecionar_pdf():
    global arquivo_pdf
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if arquivo:
        arquivo_pdf = arquivo
        nome_pdf.set(f"PDF: {os.path.basename(arquivo)}")
        checar_ativacao_botao()

def selecionar_pasta():
    global pasta_destino
    pasta = filedialog.askdirectory(
        title="Selecione a pasta de destino"
    )
    if pasta:
        pasta_destino = pasta
        label_pasta.set(f"Pasta: {pasta}")
        checar_ativacao_botao()

def checar_ativacao_botao():
    if arquivo_pdf and pasta_destino:
        botao_confirmar.config(state="normal")
    else:
        botao_confirmar.config(state="disabled")

def executar_separacao():
    if not arquivo_pdf:
        messagebox.showwarning("Aviso", "Selecione um arquivo PDF.")
        return
    if not pasta_destino:
        messagebox.showwarning("Aviso", "Selecione uma pasta de destino.")
        return

    try:
        leitor = PdfReader(arquivo_pdf)
        total_paginas = len(leitor.pages)

        if var_usar_paginas.get():
            texto_paginas = entrada_paginas.get()
            if not texto_paginas.strip():
                messagebox.showwarning("Aviso", "Informe as páginas desejadas.")
                return
            paginas = parse_paginas(texto_paginas, total_paginas)
            if not paginas:
                messagebox.showwarning("Aviso", "Nenhuma página válida foi informada.")
                return
        else:
            paginas = list(range(1, total_paginas + 1))

        for p in paginas:
            escritor = PdfWriter()
            escritor.add_page(leitor.pages[p - 1])
            nome_saida = os.path.join(pasta_destino, f"pagina_{p}.pdf")
            with open(nome_saida, "wb") as f:
                escritor.write(f)

        messagebox.showinfo("Sucesso", f"{len(paginas)} página(s) foram salvas em:\n{pasta_destino}")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def alternar_entrada():
    if var_usar_paginas.get():
        entrada_paginas.configure(state="normal")
    else:
        entrada_paginas.delete(0, tk.END)
        entrada_paginas.configure(state="disabled")

janela = tk.Tk()
janela.title("Separador de PDF por Página")
janela.geometry("500x360")
janela.resizable(False, False)

frame = tk.Frame(janela, padx=20, pady=20)
frame.pack(expand=True)

btn_pdf = tk.Button(frame, text="Selecionar PDF", command=selecionar_pdf, width=25, bg="#2196F3", fg="white")
btn_pdf.pack(pady=5)

nome_pdf = tk.StringVar()
label_pdf = tk.Label(frame, textvariable=nome_pdf, fg="blue")
label_pdf.pack()

btn_pasta = tk.Button(frame, text="Selecionar Pasta de Destino", command=selecionar_pasta, width=25, bg="#9C27B0", fg="white")
btn_pasta.pack(pady=5)

label_pasta = tk.StringVar()
label_pasta.set("Pasta: ")
label_pasta_info = tk.Label(frame, textvariable=label_pasta, fg="darkgreen")
label_pasta_info.pack()

var_usar_paginas = tk.BooleanVar(value=False)
check_paginas = tk.Checkbutton(frame, text="Selecionar páginas específicas", variable=var_usar_paginas, command=alternar_entrada)
check_paginas.pack(pady=5)

label_paginas = tk.Label(frame, text="Páginas (ex: 1,3,5-7):")
label_paginas.pack()

entrada_paginas = tk.Entry(frame, width=30, state="disabled")
entrada_paginas.pack(pady=5)

botao_confirmar = tk.Button(
    frame,
    text="Separar PDF",
    command=executar_separacao,
    height=2,
    width=30,
    state="disabled",
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold")
)
botao_confirmar.pack(pady=15)

janela.mainloop()
