def gerar_prompt(data):
    turmas_list = data.get("Turmas", [])
    regras_optativas = list(data.get("Regras", []))

    prompt = []
    prompt.append("Você é um assistente especializado em montar horários escolares.")
    prompt.append("Use os dados abaixo para gerar quadros de aulas semanais para cada turma.")
    prompt.append("Cada turma tem aulas em dias e turnos específicos, com número fixo de aulas por dia.")

    professores = {}  # Vamos agrupar os professores aqui por ID único

    # TURMAS
    prompt.append("\n📚 Turmas:")
    for turma in turmas_list:
        nome_turma = turma["nome"]
        turno = turma.get("turno", "Não especificado")
        dias_de_aula = turma.get("dias_de_aula", "Não especificado")
        horarios = turma.get("horarios", [])

        prompt.append(f"\nTurma {nome_turma} ({turno}) - Dias: {dias_de_aula} - Horários: {', '.join(horarios)}")
        prompt.append("Disciplinas e Aulas Semanais:")

        for disciplina in turma.get("Disclinas", []):
            nome_disc = disciplina["nome"]
            aulas_semana = disciplina["aulas_por_semana"]
            prof = disciplina["professor"]

            # Gera um ID fake baseado no nome (só pra identificação básica)
            prof_id = f"P_{prof['nome'].replace(' ', '_')}"
            if prof_id not in professores:
                professores[prof_id] = {
                    "nome": prof["nome"],
                    "disciplinas": set(),
                    "disponibilidade": set(prof.get("disponibilidade", [])),
                    "exigencias": prof.get("exigencias", "")
                }
            professores[prof_id]["disciplinas"].add(nome_disc)

            prompt.append(f"- {nome_disc}: {aulas_semana} aulas por semana (Prof: {prof['nome']})")

    # PROFESSORES
    prompt.append("\n👨‍🏫 Professores:")
    for prof_id, prof in professores.items():
        exigencias = prof["exigencias"] if prof["exigencias"] else "nenhuma"
        disciplinas_prof = ', '.join(prof["disciplinas"])
        disponibilidade = ', '.join(sorted(prof["disponibilidade"]))
        prompt.append(f"- {prof['nome']} ({prof_id}): {disciplinas_prof} | Disponível: {disponibilidade} | Exigências: {exigencias}")

    # REGRAS FIXAS
    prompt.append("\n📌 Regras obrigatórias:")
    prompt.append("- Cada turma deve ter exatamente 5 aulas por dia, nos dias definidos.")
    prompt.append("- As aulas devem estar distribuídas ao longo da semana.")
    prompt.append("- O mesmo professor não pode estar em mais de uma turma no mesmo horário.")
    prompt.append("- Respeite a disponibilidade de cada professor.")
    prompt.append("- Atenda às exigências dos professores sempre que possível.")
    prompt.append("- Se não for possível cumprir alguma exigência, indique o erro e explique a causa.")

    # REGRAS OPTATIVAS
    if regras_optativas:
        prompt.append("\n📌 Regras optativas:")
        for regra in regras_optativas:
            prompt.append(f"- {regra}")

    # OBJETIVO
    prompt.append("\n🎯 Objetivo:")
    prompt.append("Gerar uma tabela com os horários de cada disciplina para cada turma, atribuindo o professor certo, em horários permitidos.")
    prompt.append("Se houver inconsistências ou impossibilidades, explique claramente o problema e especifique onde foi o problema (Turma, dia e horário), separando em erros.")
    prompt.append("Se alguma regra optativa ou exigência forem descumpridas, explique claramente o problema e especifique onde foi o problema (Turma, dia e horário), separando em avisos.")

    # FORMATO DE RESPOSTA
    prompt.append("\n⚠️ IMPORTANTE:")
    prompt.append("As próximas interações serão apenas para **ajustes nas tabelas**.")
    prompt.append("Responda **somente com as tabelas alteradas**, evitando conflitos de horário entre professores ou turmas.")
    prompt.append("A resposta deve estar no seguinte formato JSON:")

    prompt.append("""
        {
            "turmas": [
                {
                    nome: "ID_TURMA",
                    dias: [
                        {
                            dia: "segunda",
                            horario: "08", 
                            disciplina: "MAT1", 
                            professor: "P1"
                        }
                        // e assim por diante...
                    ]
                }
            ],
            "erros": [ "" ],
            "avisos": [ "" ]
        }
    """)

    return "\n".join(prompt)
