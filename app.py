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

# Estilização visual customizada
st.markdown("""
<style>
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Barra Lateral - Identificação Legal e Configurações
st.sidebar.markdown("## 🛡️ SST Capacita")
st.sidebar.caption("Conforme NR-01 (Anexo II - EAD)")

st.sidebar.markdown("---")
st.sidebar.subheader("Identificação do Aluno")
aluno_nome = st.sidebar.text_input("Nome Completo:", placeholder="Ex: Carlos Eduardo Lima")
aluno_cpf = st.sidebar.text_input("CPF:", placeholder="000.000.000-00")

st.sidebar.markdown("---")
st.sidebar.subheader("Dados do Responsável Técnico")
resp_tecnico = st.sidebar.text_input("Engenheiro / Instrutor:", value="Daniel Martins")
registro_prof = st.sidebar.text_input("Registro Profissional:", value="CREA/SST Especialista")

# Seleção da Norma Regulamentadora
nr_selecionada = st.sidebar.selectbox("Selecione o Treinamento Normativo:", list(CATALOGO_NRS.keys()))
treinamento = CATALOGO_NRS[nr_selecionada]

# Cabeçalho Principal
st.title(f"🎓 {nr_selecionada} — {treinamento['titulo']}")
st.write(f"**Carga Horária Regulamentar:** {treinamento['carga_horaria']}")

# Abas de Navegação
aba_conteudo, aba_avaliacao, aba_certificacao = st.tabs([
    "📖 Conteúdo Didático & Videoaula",
    "📝 Avaliação Obrigatória",
    "🎓 Emissão de Certificado"
])

# --- ABA 1: CONTEÚDO DIDÁTICO ---
with aba_conteudo:
    st.subheader("1. Videoaula Oficial / Didática")
    st.video(treinamento["video_url"])
    
    st.subheader("2. Conteúdo Programático Formal")
    st.info(treinamento["ementa"])
    
    st.subheader("3. Diretrizes de Conclusão")
    st.write("""
    Para obter a certificação em conformidade com a NR-01, assista atentamente à instrução audiovisual, 
    revise o conteúdo programático descrito e complete a avaliação de aprendizagem com aproveitamento mínimo de 70%.
    """)

# --- ABA 2: AVALIAÇÃO OBRIGATÓRIA ---
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
            st.error("⚠️ Preencha seu Nome Completo e CPF na barra lateral antes de submeter a avaliação.")
        elif any(respostas_usuario[i] is None for i in range(len(treinamento["questoes"]))):
            st.warning("⚠️ Por favor, responda a todas as questões antes de finalizar a prova.")
        else:
            acertos = 0
            total = len(treinamento["questoes"])
            for i, q in enumerate(treinamento["questoes"]):
                if respostas_usuario[i] == q["resposta"]:
                    acertos += 1
            
            nota_percentual = int((acertos / total) * 100)
            st.session_state["aproveitamento"] = nota_percentual
            st.session_state["curso_aprovado"] = nr_selecionada
            
            if nota_percentual >= 70:
                st.success(f"🎉 Parabéns! Você foi aprovado com aproveitamento de {nota_percentual}%.")
                st.info("Acesse a aba **Emissão de Certificado** para fazer o download do documento oficial.")
            else:
                st.error(f"Aproveitamento obtido: {nota_percentual}%. A aprovação regulamentar exige no mínimo 70%. Revise o conteúdo didático e tente novamente.")

# --- ABA 3: CERTIFICAÇÃO ---
with aba_certificacao:
    st.subheader("Emissão de Certificado de Conclusão")
    
    aprovado_neste_curso = (
        st.session_state.get("curso_aprovado") == nr_selecionada and 
        st.session_state.get("aproveitamento", 0) >= 70
    )
    
    if aprovado_neste_curso:
        st.success(f"Conformidade confirmada para {nr_selecionada}! Requisitos pedagógicos e avaliativos atendidos.")
        
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
        
        cpf_limpo = aluno_cpf.replace('.', '').replace('-', '').strip() if aluno_cpf else "000"
        st.download_button(
            label="📜 Baixar Certificado Oficial (PDF)",
            data=pdf_bytes,
            file_name=f"Certificado_{nr_selecionada}_{cpf_limpo}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning(f"O certificado para {nr_selecionada} estará disponível assim que a avaliação de aprendizagem for concluída com nota igual ou superior a 70%.")
