import customtkinter as ctk
import pandas as pd
import webbrowser

from buscador import buscar_vagas_remotas
from candidatura import aplicar_vaga

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.geometry("1100x700")
app.title("Job Bot - TI Júnior")

titulo = ctk.CTkLabel(
    app,
    text="Buscador de Vagas TI",
    font=("Arial", 34)
)

titulo.pack(pady=20)

lista_box = ctk.CTkTextbox(
    app,
    width=1000,
    height=450,
    font=("Arial", 16)
)

lista_box.pack(pady=20)

status_label = ctk.CTkLabel(
    app,
    text="Aguardando busca...",
    font=("Arial", 16)
)

status_label.pack(pady=5)

vagas_encontradas = []

def buscar_vagas():

    global vagas_encontradas

    status_label.configure(
        text="Buscando vagas..."
    )

    app.update()

    lista_box.delete("1.0", "end")

    vagas = buscar_vagas_remotas()

    vagas_encontradas = vagas

    if not vagas:

        lista_box.insert(
            "end",
            "Nenhuma vaga encontrada."
        )

        status_label.configure(
            text="Nenhuma vaga encontrada."
        )

        return

    df = pd.DataFrame(vagas)

    df.to_excel(
        "vagas.xlsx",
        index=False
    )

    for i, vaga in enumerate(vagas):

        lista_box.insert(
            "end",
            f"[{i}] ⭐{vaga['score']} [{vaga['fonte']}] {vaga['titulo']}\n"
        )

        lista_box.insert(
            "end",
            f"{vaga['link']}\n\n"
        )

    status_label.configure(
        text=f"{len(vagas)} vagas encontradas."
    )

def abrir_vaga():

    try:

        texto = lista_box.get(
            "sel.first",
            "sel.last"
        )

        indice = int(
            texto.split("]")[0]
            .replace("[", "")
        )

        vaga = vagas_encontradas[indice]

        link = vaga["link"]

        if not link.startswith("http"):

            status_label.configure(
                text="Link inválido."
            )

            return

        status_label.configure(
            text="Abrindo candidatura..."
        )

        aplicar_vaga(link)

    except Exception as erro:

        status_label.configure(
            text=f"Erro: {erro}"
        )

frame_botoes = ctk.CTkFrame(app)

frame_botoes.pack(pady=10)

botao_buscar = ctk.CTkButton(
    frame_botoes,
    text="Buscar Vagas",
    command=buscar_vagas,
    width=200,
    height=50,
    font=("Arial", 18)
)

botao_buscar.grid(
    row=0,
    column=0,
    padx=10
)

botao_abrir = ctk.CTkButton(
    frame_botoes,
    text="Abrir Vaga",
    command=abrir_vaga,
    width=200,
    height=50,
    font=("Arial", 18)
)

botao_abrir.grid(
    row=0,
    column=1,
    padx=10
)

app.mainloop()