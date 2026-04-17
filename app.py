import json
from datetime import datetime
from textwrap import dedent

import requests
import streamlit as st

st.set_page_config(
    page_title="Ensina.AI — Aula Inteligente",
    page_icon="🎓",
    layout="wide",
)


# ============================================================
# Estado da aplicação
# ============================================================
def init_session_state() -> None:
    if "history" not in st.session_state:
        st.session_state.history = []
    if "last_result" not in st.session_state:
        st.session_state.last_result = ""
    if "last_payload" not in st.session_state:
        st.session_state.last_payload = {}


# ============================================================
# Configuração visual
# ============================================================
def render_header() -> None:
    st.markdown(
        """
        <div style='padding: 0.5rem 0 1rem 0;'>
            <h1 style='margin-bottom: 0.25rem;'>🎓 Ensina.AI</h1>
            <p style='font-size: 1.05rem; margin-top: 0;'>
                Gere aulas completas, exercícios, projeto prático e conteúdo explicativo em um só lugar.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Prompt base
# ============================================================
def build_prompt(
    theme: str,
    level: str,
    audience: str,
    area_focus: str,
    include_code: bool,
    include_exercises: bool,
    include_project: bool,
    include_plan: bool,
    lesson_goal: str,
) -> str:
    code_section = (
        "Inclua códigos comentados e explicados passo a passo quando fizer sentido para o tema."
        if include_code
        else "Use exemplos sem código quando o tema não exigir programação."
    )

    exercises_section = (
        dedent(
            """
            Crie exercícios em 3 níveis:
            - Básico: 3 exercícios de fixação
            - Intermediário: 2 exercícios aplicados
            - Desafio: 1 exercício com cenário real
            Traga as respostas comentadas de todos.
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
        Objetivo específico da aula: {lesson_goal}

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


# ============================================================
# Geração local de fallback
# ============================================================
def generate_local_lesson(payload: dict) -> str:
    theme = payload["theme"]
    level = payload["level"]
    audience = payload["audience"]
    area_focus = payload["area_focus"]
    goal = payload["lesson_goal"]

    code_block = ""
    if payload["include_code"]:
        code_block = dedent(
            f"""
            ## Exemplo de código ilustrativo
            ```python
            tema = "{theme}"
            nivel = "{level}"
            publico = "{audience}"

            print(f"Aula sobre: {{tema}}")
            print(f"Nível: {{nivel}}")
            print(f"Público: {{publico}}")
            ```

            **Explicação:**
            - A variável `tema` guarda o assunto principal.
            - A variável `nivel` define a profundidade.
            - A variável `publico` ajuda a adaptar a linguagem.
            - O `print()` mostra as informações de forma simples.
            """
        ).strip()

    exercises_block = ""
    if payload["include_exercises"]:
        exercises_block = dedent(
            f"""
            ## Exercícios
            ### Básico
            1. Explique com suas palavras o que é **{theme}**.
            2. Cite uma utilidade prática de **{theme}**.
            3. Qual é a diferença entre conhecer o conceito e aplicá-lo?

            **Respostas comentadas:**
            - O aluno deve mostrar entendimento claro e simples.
            - A utilidade prática pode ser ligada ao dia a dia ou trabalho.
            - Aplicar significa transformar teoria em ação.

            ### Intermediário
            1. Monte um exemplo profissional em que **{theme}** seria útil.
            2. Liste erros comuns de iniciantes e como evitá-los.

            **Respostas comentadas:**
            - O aluno precisa conectar teoria e realidade.
            - Os erros devem ser acompanhados por ação corretiva.

            ### Desafio
            1. Crie uma mini aula de 5 minutos sobre **{theme}** para alguém sem experiência.

            **Resposta esperada:**
            - Explicação simples
            - Exemplo real
            - Fechamento com aplicação prática
            """
        ).strip()

    project_block = ""
    if payload["include_project"]:
        project_block = dedent(
            f"""
            ## Projeto prático para portfólio
            **Nome do projeto:** {theme} na prática

            **Objetivo:**
            Construir um material aplicável sobre **{theme}** com foco em aprendizado e apresentação.

            **Problema real que resolve:**
            Muitas pessoas têm dificuldade para entender {theme} com clareza e transformar isso em ação.

            **Etapas:**
            1. Definir o problema que será explicado.
            2. Organizar conceitos essenciais.
            3. Criar exemplo prático.
            4. Montar exercício de validação.
            5. Transformar em material de portfólio.

            **Ferramentas sugeridas:**
            - Streamlit
            - Python
            - Markdown
            - GitHub

            **Resultado esperado:**
            Um mini produto educacional claro, útil e apresentável.

            **Melhorias futuras:**
            - adicionar exportação em PDF
            - incluir trilha de estudo
            - salvar progresso do aluno
            """
        ).strip()

    plan_block = ""
    if payload["include_plan"]:
        plan_block = dedent(
            f"""
            ## Plano de estudo de 7 dias
            - **Dia 1:** visão geral de {theme}
            - **Dia 2:** conceitos fundamentais
            - **Dia 3:** base teórica essencial
            - **Dia 4:** aplicações práticas
            - **Dia 5:** exercícios
            - **Dia 6:** projeto prático
            - **Dia 7:** revisão e explicação para outra pessoa
            """
        ).strip()

    return dedent(
        f"""
        # Aula completa: {theme}

        **Nível:** {level}  
        **Público:** {audience}  
        **Área:** {area_focus}  
        **Objetivo:** {goal}

        ## 1. Abertura da aula
        {theme} é importante porque ajuda a transformar conhecimento em resultado. Quando o aluno entende o conceito, ele consegue aplicar, explicar e tomar decisões melhores.

        ## 2. Explicação intuitiva
        Pense em {theme} como uma ferramenta que organiza a forma como você entende e resolve um problema. Em vez de decorar, você passa a enxergar lógica, utilidade e aplicação.

        ## 3. Fundamentos essenciais
        - Conceito central do tema
        - Elementos principais
        - Relação entre teoria e prática
        - Como o tema aparece em situações reais

        ## 4. Base teórica essencial
        A teoria existe para evitar aplicação superficial. O objetivo aqui não é cansar, mas dar sustentação para que a prática faça sentido.

        ## 5. Aplicação prática guiada
        1. Identifique onde o tema aparece.
        2. Separe os conceitos mais importantes.
        3. Teste com um exemplo simples.
        4. Explique o que aconteceu.
        5. Replique em um caso mais próximo da realidade.

        ## 6. Exemplos reais
        - **Dia a dia:** usar lógica, análise ou organização para resolver uma tarefa comum.
        - **Profissional:** usar {theme} para melhorar decisões, processos, análises ou entregas.

        ## 7. Erros comuns
        - querer avançar sem dominar a base
        - decorar sem entender
        - ignorar a prática
        - não revisar o conteúdo

        ## 8. Como ensinar esse conteúdo
        Explique primeiro com um exemplo simples. Depois conecte com o conceito técnico. Por fim, mostre aplicação real e valide com perguntas.

        ## 9. Revisão inteligente
        - **Resumo:** {theme} combina entendimento, aplicação e comunicação.
        - **Palavras-chave:** conceito, prática, explicação, aplicação, revisão
        - **Checklist:** entendi? consigo explicar? consigo aplicar? consigo mostrar um exemplo?
        - **Perguntas:** o que é? para que serve? onde aplicar? quais erros evitar? como ensinar?

        {code_block}

        {exercises_block}

        {project_block}

        {plan_block}
        """
    ).strip()


# ============================================================
# Integração com API de IA
# ============================================================
def get_ai_config() -> dict:
    return {
        "api_key": st.secrets.get("OPENAI_API_KEY", "") if hasattr(st, "secrets") else "",
        "model": st.secrets.get("OPENAI_MODEL", "gpt-4.1-mini") if hasattr(st, "secrets") else "gpt-4.1-mini",
        "base_url": st.secrets.get("OPENAI_BASE_URL", "https://api.openai.com/v1") if hasattr(st, "secrets") else "https://api.openai.com/v1",
        "enabled": bool(st.secrets.get("OPENAI_API_KEY", "")) if hasattr(st, "secrets") else False,
    }


def extract_text_from_response(data: dict) -> str:
    if isinstance(data, dict):
        if isinstance(data.get("output_text"), str) and data["output_text"].strip():
            return data["output_text"].strip()

        output = data.get("output", [])
        collected = []
        for item in output:
            content_items = item.get("content", []) if isinstance(item, dict) else []
            for content in content_items:
                if isinstance(content, dict):
                    text_value = content.get("text")
                    if isinstance(text_value, str) and text_value.strip():
                        collected.append(text_value.strip())
        if collected:
            return "\n\n".join(collected)

    return ""


def generate_with_ai(prompt: str, temperature: float = 0.4) -> str:
    config = get_ai_config()
    if not config["enabled"]:
        raise RuntimeError("Integração com IA não configurada.")

    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": config["model"],
        "input": prompt,
        "temperature": temperature,
    }

    response = requests.post(
        f"{config['base_url'].rstrip('/')}/responses",
        headers=headers,
        data=json.dumps(payload),
        timeout=120,
    )

    if response.status_code >= 400:
        raise RuntimeError(f"Erro da API: {response.status_code} - {response.text[:500]}")

    data = response.json()
    text = extract_text_from_response(data)
    if not text:
        raise RuntimeError("A API respondeu, mas não foi possível extrair o texto gerado.")
    return text


# ============================================================
# Persistência em sessão
# ============================================================
def save_history(theme: str, result: str, payload: dict, source: str) -> None:
    st.session_state.history.insert(
        0,
        {
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "theme": theme,
            "source": source,
            "result": result,
            "payload": payload,
        },
    )
    st.session_state.last_result = result
    st.session_state.last_payload = payload


# ============================================================
# Interface
# ============================================================
def render_sidebar() -> dict:
    with st.sidebar:
        st.header("Configurações da aula")
        theme = st.text_input("Tema da aula", placeholder="Ex.: SQL para análise de dados")
        lesson_goal = st.text_area(
            "Objetivo específico",
            placeholder="Ex.: Quero entender o tema do zero e ser capaz de ensinar para outra pessoa.",
            height=100,
        )
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

        st.subheader("Recursos")
        include_code = st.checkbox("Incluir código", value=True)
        include_exercises = st.checkbox("Incluir exercícios", value=True)
        include_project = st.checkbox("Incluir projeto prático", value=True)
        include_plan = st.checkbox("Incluir plano de estudo", value=True)

        st.subheader("Modo de geração")
        ai_enabled = get_ai_config()["enabled"]
        generation_mode = st.radio(
            "Escolha o modo",
            ["IA real" if ai_enabled else "Modo local", "Modo local"],
            index=0,
        )
        temperature = st.slider("Criatividade", min_value=0.0, max_value=1.0, value=0.4, step=0.1)

        generate = st.button("Gerar aula completa", type="primary", use_container_width=True)
        clear_history = st.button("Limpar histórico", use_container_width=True)

        if clear_history:
            st.session_state.history = []
            st.session_state.last_result = ""
            st.session_state.last_payload = {}
            st.success("Histórico limpo.")

        st.divider()
        st.caption("O app funciona sem API, mas aceita integração com IA por secrets.")

    return {
        "theme": theme,
        "lesson_goal": lesson_goal.strip() or "Entender, aplicar e ensinar esse tema com clareza.",
        "level": level,
        "audience": audience,
        "area_focus": area_focus,
        "include_code": include_code,
        "include_exercises": include_exercises,
        "include_project": include_project,
        "include_plan": include_plan,
        "generation_mode": generation_mode,
        "temperature": temperature,
        "generate": generate,
    }


def render_overview() -> None:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Histórico da sessão", len(st.session_state.history))
    with col2:
        st.metric("Modo atual", "IA real" if get_ai_config()["enabled"] else "Local")
    with col3:
        st.metric("App", "Pronto para MVP")

    st.info(
        "Este app já está preparado para duas fases: teste local sem custo e geração inteligente com API de IA quando você adicionar a chave nas secrets."
    )


def render_setup_tab() -> None:
    st.subheader("Como ligar a IA real")
    st.markdown(
        """
        Crie o arquivo `.streamlit/secrets.toml` no projeto local ou configure as secrets no ambiente de deploy.

        Exemplo:
        ```toml
        OPENAI_API_KEY = "sua_chave_aqui"
        OPENAI_MODEL = "gpt-4.1-mini"
        OPENAI_BASE_URL = "https://api.openai.com/v1"
        ```

        Depois disso, o app passa a usar a API automaticamente.
        """
    )

    st.subheader("Dependências sugeridas")
    st.code("streamlit>=1.44.0\nrequests>=2.31.0", language="txt")

    st.subheader("Próximas evoluções")
    st.markdown(
        """
        - autenticação de usuário
        - banco de dados para histórico persistente
        - exportação em PDF e DOCX
        - trilhas de estudo
        - painel administrativo
        - cobrança por plano
        """
    )


def render_history_tab() -> None:
    st.subheader("Histórico da sessão")
    if not st.session_state.history:
        st.caption("Nenhuma aula foi gerada ainda.")
        return

    for i, item in enumerate(st.session_state.history, start=1):
        with st.expander(f"{i}. {item['theme']} — {item['timestamp']} — {item['source']}"):
            st.markdown(item["result"])
            st.download_button(
                label="Baixar em Markdown",
                data=item["result"],
                file_name=f"aula_{item['theme'].lower().replace(' ', '_')}.md",
                mime="text/markdown",
                key=f"download_{i}",
            )


def render_generator_tab(payload: dict) -> None:
    st.subheader("Gerador inteligente")
    st.markdown(
        """
        Preencha os campos na barra lateral e clique em **Gerar aula completa**.
        O conteúdo pode ser criado por IA real ou pelo modo local estruturado.
        """
    )

    if payload["generate"]:
        if not payload["theme"].strip():
            st.warning("Informe um tema para gerar a aula.")
            return

        prompt = build_prompt(
            theme=payload["theme"],
            level=payload["level"],
            audience=payload["audience"],
            area_focus=payload["area_focus"],
            include_code=payload["include_code"],
            include_exercises=payload["include_exercises"],
            include_project=payload["include_project"],
            include_plan=payload["include_plan"],
            lesson_goal=payload["lesson_goal"],
        )

        with st.expander("Ver prompt base usado na geração"):
            st.code(prompt, language="markdown")

        with st.spinner("Gerando aula..."):
            try:
                if payload["generation_mode"] == "IA real" and get_ai_config()["enabled"]:
                    result = generate_with_ai(prompt, temperature=payload["temperature"])
                    source = "IA real"
                else:
                    result = generate_local_lesson(payload)
                    source = "Modo local"

                save_history(payload["theme"], result, payload, source)
                st.success(f"Aula gerada com sucesso via {source}.")
            except Exception as exc:
                st.error(f"Não foi possível gerar a aula: {exc}")
                return

    if st.session_state.last_result:
        st.subheader("Resultado")
        st.markdown(st.session_state.last_result)
        st.download_button(
            label="Baixar aula em Markdown",
            data=st.session_state.last_result,
            file_name="aula_completa.md",
            mime="text/markdown",
        )


def main() -> None:
    init_session_state()
    render_header()
    payload = render_sidebar()
    render_overview()

    tab1, tab2, tab3 = st.tabs(["Gerar aula", "Histórico", "Configuração"])

    with tab1:
        render_generator_tab(payload)
    with tab2:
        render_history_tab()
    with tab3:
        render_setup_tab()


if __name__ == "__main__":
    main()
