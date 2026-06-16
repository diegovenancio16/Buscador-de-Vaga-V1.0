def calcular_score(vaga):

    titulo = vaga["titulo"].lower()

    score = 0

    palavras_boas = {
        "junior": 30,
        "júnior": 30,
        "jr": 30,
        "trainee": 25,
        "remoto": 20,
        "home office": 20,
        "python": 15,
        "react": 15,
        "frontend": 10,
        "backend": 10,
        "fullstack": 10,
        "full stack": 10,
        ".net": 10,
        "java": 10,
        "sem experiência": 40,
        "easy apply": 25
    }

    palavras_ruins = {
        "senior": -50,
        "sênior": -50,
        "pleno": -40,
        "coordenador": -60,
        "gerente": -80,
        "vendas": -100,
        "comercial": -100,
        "marketing": -100,
        "rh": -100,
        "atendente": -100
    }

    for palavra, pontos in palavras_boas.items():

        if palavra in titulo:
            score += pontos

    for palavra, pontos in palavras_ruins.items():

        if palavra in titulo:
            score += pontos

    return score

def vaga_valida(vaga):

    titulo = vaga["titulo"].lower()

    obrigatorias = [
        "dev",
        "desenvolvedor",
        "developer",
        "frontend",
        "backend",
        "fullstack",
        "full stack",
        "react",
        "python",
        ".net",
        "java"
    ]

    return any(
        palavra in titulo
        for palavra in obrigatorias
    )