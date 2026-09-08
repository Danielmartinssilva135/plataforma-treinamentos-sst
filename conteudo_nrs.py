# conteudo_nrs.py

DADOS_BASE_NRS = {
    "NR-01": ("Disposições Gerais e Gerenciamento de Riscos Ocupacionais (GRO/PGR)", "4 horas"),
    "NR-02": ("Inspeção Prévia (Revogada)", "2 horas"),
    "NR-03": ("Embargo e Interdição", "4 horas"),
    "NR-04": ("Serviços Especializados em Segurança e Medicina do Trabalho (SESMT)", "8 horas"),
    "NR-05": ("Comissão Interna de Prevenção de Acidentes e Assédio (CIPA)", "20 horas"),
    "NR-06": ("Equipamentos de Proteção Individual (EPI)", "4 horas"),
    "NR-07": ("Programa de Controle Médico de Saúde Ocupacional (PCMSO)", "4 horas"),
    "NR-08": ("Edificações", "4 horas"),
    "NR-09": ("Avaliação e Controle das Exposições Ocupacionais a Agentes Físicos, Químicos e Biológicos", "8 horas"),
    "NR-10": ("Segurança em Instalações e Serviços em Eletricidade", "40 horas"),
    "NR-11": ("Transporte, Movimentação, Armazenagem e Manuseio de Materiais", "16 horas"),
    "NR-12": ("Segurança no Trabalho em Máquinas e Equipamentos", "16 horas"),
    "NR-13": ("Caldeiras, Vasos de Pressão, Tubulações e Tanques Metálicos de Armazenamento", "40 horas"),
    "NR-14": ("Fornos", "4 horas"),
    "NR-15": ("Atividades e Operações Insalubres", "8 horas"),
    "NR-16": ("Atividades e Operações Perigosas", "8 horas"),
    "NR-17": ("Ergonomia e Análise Ergonômica do Trabalho (AET)", "8 horas"),
    "NR-18": ("Segurança e Saúde no Trabalho na Indústria da Construção", "16 horas"),
    "NR-19": ("Explosivos", "20 horas"),
    "NR-20": ("Segurança e Saúde no Trabalho com Inflamáveis e Combustíveis", "16 horas"),
    "NR-21": ("Trabalhos a Céu Aberto", "4 horas"),
    "NR-22": ("Segurança e Saúde Ocupacional na Mineração", "24 horas"),
    "NR-23": ("Proteção Contra Incêndios", "8 horas"),
    "NR-24": ("Condições Sanitárias e de Conforto nos Locais de Trabalho", "4 horas"),
    "NR-25": ("Resíduos Industriais", "4 horas"),
    "NR-26": ("Sinalização de Segurança e Classificação GHS", "4 horas"),
    "NR-27": ("Registro Profissional do Técnico de Segurança (Revogada)", "2 horas"),
    "NR-28": ("Fiscalização e Penalidades", "4 horas"),
    "NR-29": ("Segurança e Saúde no Trabalho Portuário", "24 horas"),
    "NR-30": ("Segurança e Saúde no Trabalho Aquaviário", "24 horas"),
    "NR-31": ("Segurança e Saúde no Trabalho na Agricultura, Pecuária, Silvicultura e Exploração Florestal", "20 horas"),
    "NR-32": ("Segurança e Saúde no Trabalho em Serviços de Saúde", "16 horas"),
    "NR-33": ("Segurança e Saúde nos Trabalhos em Espaços Confinados", "16 horas"),
    "NR-34": ("Condições e Meio Ambiente de Trabalho na Indústria da Construção e Reparação Naval", "20 horas"),
    "NR-35": ("Trabalho em Altura", "8 horas"),
    "NR-36": ("Segurança e Saúde no Trabalho em Empresas de Abate e Processamento de Carnes e Derivados", "16 horas"),
    "NR-37": ("Segurança e Saúde em Plataformas de Petróleo", "30 horas"),
    "NR-38": ("Segurança e Saúde no Trabalho nas Atividades de Limpeza Urbana e Manejo de Resíduos Sólidos", "8 horas")
}

CATALOGO_NRS = {}

for cod, (titulo, ch) in DADOS_BASE_NRS.items():
    query_busca = f"{cod.replace('-', ' ')} {titulo} treinamento sesmt"
    url_youtube = f"https://www.youtube.com/results?search_query={query_busca.replace(' ', '+')}"
    
    CATALOGO_NRS[cod] = {
        "titulo": titulo,
        "carga_horaria": ch,
        "video_url": url_youtube,
        "ementa": f"Capacitação técnica em conformidade com os requisitos vigentes da {cod} ({titulo}). Aborda identificação e gestão de perigos, medidas preventivas de controle coletivo e individual, responsabilidades legais e operacionais, procedimentos de emergência e diretrizes de conformidade aplicáveis.",
        "questoes": [
            {
                "pergunta": f"Qual é o objetivo principal das diretrizes estabelecidas na {cod}?",
                "opcoes": [
                    f"Estabelecer padrões de proteção e prevenção para {titulo.lower()}",
                    "Aumentar o valor das multas aplicadas pelas consultorias",
                    "Dispensar a empresa da emissão de laudos de SST",
                    "Reduzir a carga horária de trabalho para todos os funcionários"
                ],
                "resposta": f"Estabelecer padrões de proteção e prevenção para {titulo.lower()}"
            },
            {
                "pergunta": f"Conforme os preceitos regulamentares da {cod}, as medidas de controle devem priorizar:",
                "opcoes": [
                    "A eliminação do perigo e a proteção coletiva (EPC) antes do fornecimento de EPI",
                    "O uso exclusivo de advertências verbais",
                    "A indenização financeira em detrimento de melhorias ambientais",
                    "A dispensa imediata de treinamentos periódicos"
                ],
                "resposta": "A eliminação do perigo e a proteção coletiva (EPC) antes do fornecimento de EPI"
            }
        ]
    }
