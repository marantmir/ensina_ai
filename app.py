import streamlit as st
from textwrap import dedent

st.set_page_config(
    page_title="Ensina.AI — Gerador de Aulas",
    page_icon="🎓",
    layout="wide",
)


# -----------------------------
# Helpers
# --------------------([docs.streamlit.io](https://docs.streamlit.io/deploy/streamlit-community-cloud?utm_source=chatgpt.com))ence: str,
    include_code: bool,
    include_exercises: bool,
    include_project: bool,
    include_plan: bool,
    area_focus: str,
) -> str:
    code_section = (
        "Inclua códigos comentados e explicados passo a passo quando fizer sentido para o tema."
        if include_code
        else "Use exemplos sem código quando código não for necessário."
    )

    exercises_section = (
        dedent(
            """
            Crie exercícios em 3 níveis:
            - Básico: 3 questões
            - Intermediário: 2 questões
            - Desafio: 1 questão
            Traga as respostas comentadas.
            """
        ).strip()
        if include_exercises
        else ""
    )

    project_section = (
        dedent(
            """
            Crie um projeto prático para portfólio com:
            - nome do projeto
            - objetivo
            - problema real que resolve
            - etapas detalhadas
            - ferramentas sugeridas
            - resultado esperado
            - melhorias futuras
            """
        ).strip()
        if include_project
        else ""
    )

    plan_section = (
        "Monte também um plano de estudo de 7 dias para consolidar o aprendizado."
        if include_plan
        else ""
    )

    return dedent(
        f"""
        Você é um professor especialista, didático e orientado a resultados.

        Sua missão é criar uma aula completa sobre o tema informado, de forma que uma pessoa {audience.lower()} consiga aprender, aplicar e ensinar o conteúdo.

        Tema: {theme}
        Nível desejado: {level}
        Foco da área: {area_focus}

        Estruture a resposta exatamente nesta ordem:

        1. Abertura da aula
        - Explique por que esse tema importa.
        - Dê contexto de uso real.

        2. Explicação intuitiva
        - Explique de forma simples e acessível.
        - Use analogias do cotidiano.

        3. Fundamentos essenciais
        - Conceitos principais
        - Definições técnicas sem exagero
        - Relação entre os conceitos

        4. Base teórica essencial
        - Explique o suficiente para entendimento sólido.
        - Evite excesso de academicismo.

        5. Aplicação prática guiada
        - Mostre passo a passo como aplicar.

        6. Exemplos reais
        - Um exemplo do dia a dia
        - Um exemplo profissional

        7. Erros comuns
        - Liste os erros de iniciantes e como evitar.

        8. Como ensinar esse conteúdo para outra pessoa
        - Explique em linguagem muito simples.
        - Traga uma versão para iniciantes.
        - Traga uma versão para contexto profissional.

        9. Revisão inteligente
        - Resumo em tópicos
        - Palavras-chave
        - Checklist do que foi aprendido
        - 5 perguntas com respostas

        {code_section}

        {exercises_section}

        {project_section}

        {plan_section}

        Regras obrigatórias:
        - Não assuma conhecimento prévio.
        - Use linguagem clara, amigável e organizada.
        - Vá do simples ao mais técnico.
        - Priorize clareza e utilidade prática.
        - Sempre conecte teoria com prática.
        - Formate a resposta com títulos e subtítulos bem organizados.
        """
    ).strip()


def app_header() -> None:
    st.markdown(
        """
        <div style='padding: 1.2rem 0 0.6rem 0;'>
            <h1 style='margin-bottom: 0.2rem;'>🎓 Ensina.AI</h1>
            <p style='font-size: 1.05rem;'>Gere aulas completas, exercícios e projetos práticos a partir de um tema.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar():
    with st.sidebar:
        st.header("Configurações")
        theme = st.text_input("Tema da aula", placeholder="Ex.: SQL para análise de dados")
        level = st.selectbox(
            "Nível",
            ["Iniciante", "Básico ao Intermediário", "Intermediário", "Básico ao Avançado"],
        )
        audience = st.selectbox(
            "Público",
            ["Leigo", "Estudante", "Profissional em transição", "Equipe de trabalho"],
        )
        area_focus = st.selectbox(
            "Foco principal",
            ["Tecnologia", "Dados", "Negócios", "Educação", "Processos", "Outro"],
        )

        st.subheader("Recursos da aula")
        include_code = st.checkbox("Incluir código quando aplicável", value=True)
        include_exercises = st.checkbox("Incluir exercícios", value=True)
        include_project = st.checkbox("Incluir projeto prático", value=True)
        include_plan = st.checkbox("Incluir plano de estudo de 7 dias", value=True)

        generate = st.button("Gerar prompt da aula", type="primary", use_container_width=True)

    return (
        theme,
        level,
        audience,
        include_code,
        include_exercises,
        include_project,
        include_plan,
        area_focus,
        generate,
    )


def main() -> None:
    app_header()
    (
        theme,
        level,
        audience,
        include_code,
        include_exercises,
        include_project,
        include_plan,
        area_focus,
        generate,
    ) = sidebar()

    col1, col2 = st.columns([1.15, 0.85], gap="large")

    with col1:
        st.subheader("Como funciona")
        st.markdown(
            """
            1. Você informa o tema da aula.
            2. Ajusta o nível e o público.
            3. Escolhe se quer exercícios, projeto e código.
            4. O app monta um prompt completo para usar com um modelo de IA.
            """
        )

        st.subheader("Exemplos de temas")
        st.markdown(
            """
            - CRISP-DM na prática
            - Power BI para iniciantes
            - Python para análise de dados
            - Lean Six Sigma aplicado a processos
            - Machine Learning explicado de forma simples
            """
        )

    with col2:
        st.subheader("Saída esperada")
        st.info(
            "O app gera um prompt mestre que você pode usar para criar uma aula completa com teoria leve, exemplos, exercícios e projeto prático."
        )

    st.divider()

    if generate:
        if not theme.strip():
            st.warning("Informe um tema para gerar a aula.")
            return

        prompt = build_prompt(
            theme=theme,
            level=level,
            audience=audience,
            include_code=include_code,
            include_exercises=include_exercises,
            include_project=include_project,
            include_plan=include_plan,
            area_focus=area_focus,
        )

        st.subheader("Prompt gerado")
        st.code(prompt, language="markdown")
        st.download_button(
            label="Baixar prompt em TXT",
            data=prompt,
            file_name="prompt_aula_completa.txt",
            mime="text/plain",
        )

        st.subheader("Sugestão de evolução")
        st.markdown(
            f"""
            Você gerou um prompt para o tema **{theme}**.

            Próximos passos para transformar isso em um SaaS educacional:
            - salvar histórico de aulas geradas
            - adicionar login
            - exportar em PDF/DOCX
            - integrar com API de IA
            - criar área de cursos e trilhas
            """
        )
    else:
        st.subheader("Prompt de exemplo")
        example = build_prompt(
            theme="SQL para análise de dados",
            level="Iniciante",
            audience="Leigo",
            include_code=True,
            include_exercises=True,
            include_project=True,
            include_plan=True,
            area_focus="Dados",
        )
        st.code(example, language="markdown")


if __name__ == "__main__":
    main()
