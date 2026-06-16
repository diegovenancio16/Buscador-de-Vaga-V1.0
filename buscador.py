from concurrent.futures import ThreadPoolExecutor

from vagas.remotar import buscar_remotar
from vagas.indeed import buscar_indeed
from vagas.linkedin import buscar_linkedin

from filtros import calcular_score, vaga_valida


def buscar_site(funcao, nome):

    try:

        print(f"Buscando {nome}...")

        vagas = funcao()

        print(f"{nome}: {len(vagas)} vagas")

        return vagas

    except Exception as erro:

        print(f"Erro em {nome}: {erro}")

        return []


def buscar_vagas_remotas():

    vagas = []

    with ThreadPoolExecutor(max_workers=3) as executor:

        tarefas = [

            executor.submit(
                buscar_site,
                buscar_remotar,
                "Remotar"
            ),

            executor.submit(
                buscar_site,
                buscar_indeed,
                "Indeed"
            ),

            executor.submit(
                buscar_site,
                buscar_linkedin,
                "LinkedIn"
            )

        ]

        for tarefa in tarefas:

            vagas.extend(tarefa.result())

    vagas_unicas = []

    links = set()

    for vaga in vagas:

        if vaga["link"] not in links:

            links.add(vaga["link"])

            if not vaga_valida(vaga):
                continue

            vaga["score"] = calcular_score(vaga)

            vagas_unicas.append(vaga)

    vagas_unicas.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return vagas_unicas