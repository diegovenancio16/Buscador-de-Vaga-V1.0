from playwright.sync_api import sync_playwright

from config import *

CAMINHO_CHROME = r"C:\Users\Usuario\AppData\Local\Google\Chrome\User Data"

def preencher_campo(pagina, seletores, valor):

    for seletor in seletores:

        try:

            campo = pagina.locator(seletor).first

            if campo.is_visible():

                campo.fill(valor)

                print(f"Preenchido: {valor}")

                return True

        except:
            pass

    return False

def aplicar_vaga(link):

    with sync_playwright() as p:

        contexto = p.chromium.launch_persistent_context(
            user_data_dir=CAMINHO_CHROME,
            headless=False,
            slow_mo=400
        )

        pagina = contexto.new_page()

        pagina.goto(link, timeout=60000)

        pagina.wait_for_timeout(5000)

        botoes = pagina.locator("button").all()

        palavras = [
            "apply",
            "easy apply",
            "candidatar",
            "candidate-se",
            "inscrever",
            "continuar",
            "apply now",
            "acessar"
        ]

        for botao in botoes:

            try:

                texto = botao.inner_text().lower()

                if any(
                    palavra in texto
                    for palavra in palavras
                ):

                    print(f"Botão encontrado: {texto}")

                    botao.click()

                    pagina.wait_for_timeout(5000)

                    break

            except:
                pass

        preencher_campo(
            pagina,
            [
                'input[name="name"]',
                'input[type="text"]'
            ],
            NOME
        )

        preencher_campo(
            pagina,
            [
                'input[type="email"]'
            ],
            EMAIL
        )

        preencher_campo(
            pagina,
            [
                'input[type="tel"]'
            ],
            TELEFONE
        )

        try:

            upload = pagina.locator(
                'input[type="file"]'
            ).first

            upload.set_input_files(CURRICULO)

            print("Currículo enviado!")

        except:
            print("Campo de upload não encontrado.")

        pagina.wait_for_timeout(20000)

        contexto.close()