import os
from tkinter import Tk, filedialog, messagebox
from pypdf import PdfReader, PdfWriter

def separar_pdf():
    # Oculta a janela principal do tkinter
    root = Tk()
    root.withdraw()

    # Seleciona o arquivo PDF
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )

    if not arquivo:
        return

    # Seleciona a pasta de destino
    pasta_saida = filedialog.askdirectory(
        title="Selecione a pasta de destino para os arquivos PDF separados"
    )

    if not pasta_saida:
        return

    try:
        leitor = PdfReader(arquivo)
        total_paginas = len(leitor.pages)

        for i, pagina in enumerate(leitor.pages):
            escritor = PdfWriter()
            escritor.add_page(pagina)

            nome_saida = os.path.join(pasta_saida, f"pagina_{i+1}.pdf")
            with open(nome_saida, "wb") as f:
                escritor.write(f)

        messagebox.showinfo("Sucesso", f"{total_paginas} arquivos foram salvos em:\n{pasta_saida}")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Executa o programa
separar_pdf()
