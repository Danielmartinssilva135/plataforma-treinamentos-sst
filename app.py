# app.py
import streamlit as st
from datetime import date
from conteudo_nrs import CATALOGO_NRS
from gerador_cert import gerar_certificado_pdf

st.set_page_config(
    page_title="Plataforma de Treinamentos SST Corporativa",
    page_icon="🛡️",
    layout="wide"
)

# Barra Lateral - Identificação do Aluno e Responsável Técnico
st.sidebar.image("https://img.icons8.com/color/96/safety-shield.png", width=70)
st.sidebar.title("Portal SST Treinamentos")
st.sidebar.caption("Conforme NR-01 (Anexo II - EAD)")

st.sidebar.markdown("---")
st.sidebar.subheader("Identificação do Aluno")
aluno_nome = st.sidebar.text_input("Nome Completo:", placeholder="Ex: Carlos Eduardo Lima")
aluno_cpf = st.sidebar.text_input("CPF:", placeholder="000.000.000-00")

st.sidebar.markdown("---")
st.sidebar.subheader("Dados do Responsável Técnico")
resp_tecnico = st.sidebar.text_input("Engenheiro / Instrutor:", value="Daniel Martins")
registro_prof = st.sidebar.text_input("Registro Profissional:", value="CREA/SST Especialista")

# Seleção da Norma
nr_selecionada = st.sidebar.selectbox("Selecione o Treinamento Normativo:", list(CATALOGO_NRS.keys()))
treinamento = CATALOGO_NRS[nr_selecionada]

# Cabeçalho Principal
st.title(f"🎓 {nr_selecionada} — {treinamento['titulo']}")
st.write(f"**Carga Horária Regulamentar:** {treinamento['carga_horaria']}")

# Abas de Acesso
aba_conteudo, aba_avaliacao, aba_certificacao = st.tabs([
    "📖 Conteúdo Didático & Videoaula",
    "📝 Avaliação Obrigatória",
    "🎓 Emissão de Certificado"
])

# --- ABA 1: CONTEÚDO ---
with aba_conteudo:
    st.subheader("1. Videoaula Oficial / Didática")
    st.video(treinamento["video_url"])
    
    st.subheader("2. Conteúdo Programático Formal")
    st.info(treinamento["ementa"])
    
    st.subheader("3. Material de Apoio e Leitura")
    st.write("""
    A realização completa deste módulo requer a visualização atenta da instrução em vídeo, 
    a leitura atenta das diretrizes de controle de riscos e a posterior realização do teste de fixação.
    """)

# --- ABA 2: AVALIAÇÃO ---
with aba_avaliacao:
    st.subheader("Avaliação de Aprendizagem (Exigência NR-01)")
    st.caption("Nota mínima exigida para aprovação: 70%")
    
    respostas_usuario = {}
    with st.form("form_avaliacao"):
        for i, q in enumerate(treinamento["questoes"]):
            st.markdown(f"**Questão {i+1}:** {q['pergunta']}")
            respostas_usuario[i] = st.radio(
                "Selecione uma opção:", 
                q["opcoes"], 
                key=f"q_{nr_selecionada}_{i}", 
                index=None
            )
            st.write("")
        
        btn_enviar_prova = st.form_submit_button("Submeter Avaliação")

    if btn_enviar_prova:
        if not aluno_nome or not aluno_cpf:
            st.error("⚠️ Preencha seu Nome e CPF no menu lateral antes de concluir a avaliação.")
        else:
            acertos = 0
            total = len(treinamento["questoes"])
            for i, q in enumerate(treinamento["questoes"]):
                if respostas_usuario[i] == q["resposta"]:
                    acertos += 1
            
            nota_percentual = int((acertos / total) * 100)
            st.session_state["aproveitamento"] = nota_percentual
            st.session_state["prova_feita"] = True
            
            if nota_percentual >= 70:
                st.success(f"🎉 Parabéns! Você foi aprovado com aproveitamento de {nota_percentual}%.")
                st.info("Acesse a aba **Emissão de Certificado** para obter seu documento legal.")
            else:
                st.error(f"Aproveitamento obtido: {nota_percentual}%. A aprovação exige no mínimo 70%. Revise o conteúdo e refaça a avaliação.")

# --- ABA 3: CERTIFICAÇÃO ---
with aba_certificacao:
    st.subheader("Emissão de Certificado")
    
    if "aproveitamento" in st.session_state and st.session_state["aproveitamento"] >= 70:
        st.success("Requisitos pedagógicos e regulamentares atendidos.")
        
        dados_cert = {
            "aluno_nome": aluno_nome,
            "aluno_cpf": aluno_cpf,
            "nr_nome": nr_selecionada,
            "treinamento_titulo": treinamento["titulo"],
            "carga_horaria": treinamento["carga_horaria"],
            "data_inicio": date.today().strftime("%d/%m/%Y"),
            "data_fim": date.today().strftime("%d/%m/%Y"),
            "aproveitamento": st.session_state["aproveitamento"],
            "resp_tecnico": resp_tecnico,
            "registro_profissional": registro_prof
        }
        
        pdf_bytes = gerar_certificado_pdf(dados_cert)
        
        cpf_limpo = aluno_cpf.replace('.', '').replace('-', '') if aluno_cpf else "000"
        st.download_button(
            label="📜 Baixar Certificado Oficial (PDF)",
            data=pdf_bytes,
            file_name=f"Certificado_{nr_selecionada}_{cpf_limpo}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("O certificado será liberado após a conclusão e aprovação na aba 'Avaliação Obrigatória'.")
