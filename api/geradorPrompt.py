def gerar_prompt(data):
    professores_list = data.get("professores", [])
    turmas_list = data.get("turmas", [])
    disciplinas_list = data.get("disciplinas", [])
    horarios = sorted(data.get("horariosDisponiveis", []))
    regras_optativas = list(data.get("regras", []))

    # Transformar listas em dicionários
    professores = {p["id"]: p for p in professores_list}
    turmas = {t["id"]: t for t in turmas_list}
    disciplinas = {d["id"]: d for d in disciplinas_list}

    prompt = []
    prompt.append("Você é um assistente especializado em montar horários escolares.")
    prompt.append("Use os dados abaixo para gerar quadros de aulas semanais para cada turma.")
    prompt.append("Cada turma tem aulas de segunda a sexta, com número fixo de aulas por dia (turnos).")

    # TURMAS
    for turma_id, turma in turmas.items():
        prompt.append(f"\n📚 Turma {turma_id} ({turma['periodo']}):")
        prompt.append("Disciplinas e Aulas Semanais:")
        for disciplina in turma["disciplinas"]:
            disc_id = disciplina["id"]
            aulas = disciplina["aulas_por_semana"]
            nome = disciplinas[disc_id]["nome"]
            prompt.append(f"- {disc_id} ({nome}): {aulas} aulas por semana")

    # PROFESSORES
    prompt.append("\n👨‍🏫 Professores:")
    for prof_id, prof in professores.items():
        exigencias = ', '.join(prof.get("exigencias", [])) if prof.get("exigencias") else "nenhuma"
        disciplinas_prof = ', '.join(prof["disciplinas"])
        disponibilidade = ', '.join(sorted(prof["disponibilidade"]))
        prompt.append(f"- {prof['nome']} ({prof_id}): {disciplinas_prof} | Disponível: {disponibilidade} | Exigências: {exigencias}")
    
    # REGRAS FIXAS
    prompt.append("\n📌 Regras obrigatórias:")
    prompt.append("- Cada turma deve ter exatamente 5 aulas por dia, de segunda a sexta.")
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
    prompt.append("Se houver inconsistências ou impossibilidades, explique claramente o problema e proponha soluções viáveis e expecifique onde foi o problema(Turma dia e horario), separando em erros.")
    prompt.append("Se alguma regra optativa ou exigência forem descumpridas, explique claramente o problema e expecifique onde foi o problema(Turma dia e horario), separando em avisos.")

    # FORMATO DE RESPOSTA
    prompt.append("\n⚠️ IMPORTANTE:")
    prompt.append("As próximas interações serão apenas para **ajustes nas tabelas**.")
    prompt.append("Responda **somente com as tabelas alteradas**, evitando conflitos de horário entre professores ou turmas.")
    prompt.append("A resposta deve estar no seguinte formato JSON:")

    prompt.append("""
        {
            "turmas": [
                {
                    nome: "ID_TURMA"
                    dias: [
                        {
                            dia: "segunda"
                            "horario": "08", 
                            "disciplina": "MAT1", 
                            "professor": "P1"
                        },
                        {
                            dia: "segunda"
                            "horario": "09", 
                            "disciplina": "POR1", 
                            "professor": "P2"
                        }
                        // e assim por diante...
                    ]
                }
            ],
            "erros": [ "" ],
            "avisos": [ "" ]
        }
    """)

    # HORÁRIOS DISPONÍVEIS
    prompt.append("\n📅 Horários disponíveis:")
    prompt.append(', '.join(horarios))

    return "\n".join(prompt)



