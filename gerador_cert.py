# gerador_cert.py
import io
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def gerar_certificado_pdf(dados):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    style_titulo = ParagraphStyle(
        'Titulo',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0F172A'),
        alignment=1
    )
    
    style_sub = ParagraphStyle(
        'Subtitulo',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0284C7'),
        alignment=1
    )
    
    style_corpo = ParagraphStyle(
        'Corpo',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=18,
        textColor=colors.HexColor('#334155'),
        alignment=1
    )
    
    style_rodape = ParagraphStyle(
        'Rodape',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#64748B'),
        alignment=1
    )

    story = []

    story.append(Spacer(1, 15))
    story.append(Paragraph("CERTIFICADO DE CAPACITAÇÃO PROFISSIONAL", style_titulo))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"EM CONFORMIDADE COM A NR-01 (ANEXO II) E {dados['nr_nome']}", style_sub))
    story.append(Spacer(1, 25))
    
    texto_certificacao = f"""
    Certificamos que <b>{dados['aluno_nome'].upper()}</b>, portador(a) do CPF nº <b>{dados['aluno_cpf']}</b>, 
    concluiu com êxito o treinamento de <b>{dados['nr_nome']} - {dados['treinamento_titulo']}</b>, 
    realizado na modalidade de Ensino a Distância (EAD), no período de <b>{dados['data_inicio']}</b> a <b>{dados['data_fim']}</b>, 
    com carga horária total de <b>{dados['carga_horaria']}</b> e aproveitamento avaliativo de <b>{dados['aproveitamento']}%</b>.
    """
    story.append(Paragraph(texto_certificacao, style_corpo))
    story.append(Spacer(1, 45))
    
    dados_assinaturas = [
        [
            Paragraph(f"_______________________________________<br/><b>{dados['aluno_nome']}</b><br/>Colaborador / Aluno", style_rodape),
            Paragraph(f"_______________________________________<br/><b>{dados['resp_tecnico']}</b><br/>{dados['registro_profissional']}<br/>Responsável Técnico / Instrutor", style_rodape)
        ]
    ]
    tabela_ass = Table(dados_assinaturas, colWidths=[350, 350])
    tabela_ass.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(tabela_ass)
    
    doc.build(story)
    buffer.seek(0)
    return buffer
