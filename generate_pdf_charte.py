import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

def generer_pdf_charte_ultime():
    pdf_filename = "charte_mastering_hermes_v2_en.pdf"
    marge = 30 # Légère réduction pour maximiser l'espace horizontal
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=landscape(A4),
        leftMargin=marge, rightMargin=marge, topMargin=marge, bottomMargin=marge
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=colors.HexColor('#1A2B4C'), spaceAfter=3
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=9, leading=12, textColor=colors.HexColor('#555555'), spaceAfter=10
    )
    th_style = ParagraphStyle(
        'TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=10, textColor=colors.white, alignment=TA_CENTER
    )
    td_style = ParagraphStyle(
        'TableCell', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11, textColor=colors.HexColor('#222222')
    )
    td_center = ParagraphStyle(
        'TableCellCenter', parent=td_style, alignment=TA_CENTER
    )

    elements.append(Paragraph("FOLIOTYPE PROTOCOL — CHARTE MAÎTRESSE HÉRMÈS V2 (EN)", title_style))
    elements.append(Paragraph("Verrouillage des Fréquences, Ratios, Lookahead et Paramètres Experts Multi-Bandes Anti-Artefact", subtitle_style))
    
    # Structure de tableau étendue à 7 colonnes pour isoler le Ratio et le Lookahead
    headers = [
        Paragraph("Pos", th_style),
        Paragraph("Plugin", th_style),
        Paragraph("Bande / Paramètre", th_style),
        Paragraph("Fréquence", th_style),
        Paragraph("Ratio / Lookahead", th_style),
        Paragraph("Réglages Experts &amp; Phase", th_style),
        Paragraph("Rôle Acoustique (Foliotype Context)", th_style)
    ]
    
    raw_data = [
        ("1", "FabFilter Pro-G", "Gate / Expander Global", "Full Range", 
         "<b>Ratio : 1:1.2</b><br/>Lookahead : 0 ms", 
         "• Mode: Expander doux<br/>• Threshold: -52 dB<br/>• Range: 11 dB max<br/>• Attack: 0.1 ms | Release: 280 ms", 
         "Le Gardien du Silence : Atténue le souffle numérique de 11 dB sans coupure entre les phrases. Conserve les micro-expirations humaines et nettoie la pré-ventilation de l'IA."),
        
        ("2.1", "FabFilter Pro-Q 4", "Assise (Low Shelf)", "85 Hz", 
         "N/A<br/>(Égaliseur)", 
         "• Type: Low Shelf (Plateau bas)<br/>• Gain: -2.5 dB<br/>• Q: 0.7 (Courbe ultra-large)<br/>• Mode: Analog", 
         "L'Intériorité Crânienne : Atténuation en pente douce évitant le vrombissement des infra-basses. Conserve le poids physique et le velours des cordes vocales."),
        
        ("2.2", "FabFilter Pro-Q 4", "Anti-Mud / Clarification", "350 Hz", 
         "N/A<br/>(Égaliseur)", 
         "• Type: Bell (Cloche)<br/>• Gain: -1.2 dB<br/>• Q: 1.0 (Large)<br/>• Mode: Dynamic EQ (Seuil réactif)", 
         "Libération de l'Espace Mental : Corrige l'effet 'boîte' lié à l'accumulation des diphtongues anglaises denses. Redonne de l'air à la lecture mentale."),
        
        ("2.3", "FabFilter Pro-Q 4", "Contrôle Dynamique", "3.2 kHz", 
         "N/A<br/>(Égaliseur)", 
         "• Type: Bell (Cloche)<br/>• Gain: -1.5 dB<br/>• Q: 1.8<br/>• Mode: Dynamic EQ", 
         "Atténuation Chirurgicale : Dompte l'agressivité des consonnes dures ou des accents toniques excessifs de l'IA uniquement lorsqu'ils dépassent."),
        
        ("3", "FabFilter Pro-DS", "De-Esser Sibilantes", "4.5 kHz – 9.5 kHz", 
         "N/A<br/>(De-Esser intelligent)", 
         "• Mode: Single Vocal<br/>• Algorithm: Split Band<br/>• Threshold: Ajusté au signal<br/>• Range: -4.5 dB max", 
         "Le Tueur de Sibilantes : Intercepte la friction large de l'anglais (S, Z, SH, TH) avant la compression globale. Supprime tout risque de zézaiement."),
        
        ("4", "FabFilter Pro-MB (1)", "Bande 1 : Le Corps", "90 Hz – 280 Hz", 
         "<b>Ratio : 1:1.4</b><br/>Lookahead : 0 ms", 
         "• Range: -2.5 dB | Gain: 0 dB<br/>• Attack: 35% | Release: 45%<br/>• <b>Mode: Linear Phase (Medium)</b><br/>• <b>Sidechain: Custom (Verrouillé)</b><br/>• Knee: 8 dB (Soft)", 
         "Stabilisateur d'Assise : Compresse le bas-médium pour lisser en temps réel les sautes de proximité de l'IA (liées à l'instabilité du paramètre stability)."),
        
        ("5", "FabFilter Pro-MB (2)", "Bande 1.5 : Anti-Nasal", "600 Hz – 900 Hz", 
         "<b>Ratio : 1:1.4</b><br/>Lookahead : 0 ms", 
         "• Range: -1.0 dB | Gain: 0 dB<br/>• Attack: 40% | Release: 40%<br/>• <b>Mode: Linear Phase (Medium)</b><br/>• <b>Sidechain: Custom (Verrouillé)</b><br/>• Knee: 8 dB (Soft)", 
         "Filtre Anti-Canard : Élimine les résonances nasales artificielles qu'ElevenLabs génère sur les consonnes d'appui anglaises (M, N, R)."),
        
        ("6", "FabFilter Pro-MB (3)", "Bande 2 : Présence", "1.0 kHz – 3.5 kHz", 
         "<b>Ratio : 1:1.4</b><br/>Lookahead : 0 ms", 
         "• Range: -1.5 dB | Gain: 0 dB<br/>• Attack: 40% | Release: 40%<br/>• <b>Mode: Linear Phase (Medium)</b><br/>• <b>Sidechain: Custom (Verrouillé)</b><br/>• Knee: 8 dB (Soft)", 
         "Le Maître de l'Intelligibilité : Gère l'autorité journalistique et le charme d'Hermès. Rabote les pointes excessives sans affadir le médium."),
        
        ("7", "Waves CLA-2A", "Compresseur Global", "Full Range", 
         "<b>Ratio : ~1:3.0</b><br/>(Fixe, Cellule T4)", 
         "• Mode: COMPRESS<br/>• Peak Reduction: Cible -1.5 à -2 dB max<br/>• Hi-Freq: Flat (100% à droite)<br/>• Gain: Sortie (+2 dB)", 
         "Le Ciment de la Prose : Sa cellule optique lente unifie le flux des phrases anglaises pour lier les mots et créer un tapis vocal fluide et hypnotique."),
        
        ("8", "FabFilter Pro-MB (4)", "Bande 3 : Charme &amp; Piqué", "5.0 kHz – 7.0 kHz", 
         "<b>Ratio : 1:1.4</b><br/>Lookahead : 0 ms", 
         "• Range: -1.5 dB | Gain: 0 dB<br/>• Attack: 25% | Release: 35%<br/>• <b>Mode: Linear Phase (Medium)</b><br/>• <b>Sidechain: Custom (Verrouillé)</b><br/>• Knee: 8 dB (Soft)", 
         "Préservation de la Clarté : Protège les micro-détails d'articulation (F, V, Th). Gère la transition en douceur pour garder la définition sans agressivité."),
        
        ("9", "FabFilter Pro-MB (5)", "Bande 4 : Bouclier", "7.5 kHz – 14 kHz", 
         "<b>Ratio : 1:4.0</b> (Dur)<br/><b>Lookahead : 3.0 ms</b>", 
         "• Range: -5.0 dB (Couperet) | Gain: 0 dB<br/>• Attack: 5% (Ultra-rapide) | Release: 25%<br/>• <b>Mode: Linear Phase</b><br/>• <b>Sidechain: Custom (Verrouillé)</b>", 
         "Anti-Aliasing Prévoyant : Placé après le CLA-2A. Grâce aux 3 ms d'anticipation, il intercepte et détruit l'aliasing métallique avant qu'il ne passe au Master."),
        
        ("10", "FabFilter Pro-L 2", "Limiteur Final Master", "Full Range", 
         "<b>Ratio : 1:inf</b> (Limiteur)<br/><b>Lookahead : 1.5 ms</b>", 
         "• Style: TRANSPARENT<br/>• Attack: 0.6 ms | Release: 320 ms<br/>• Output (Ceiling): -1.5 dB TP (Obligatoire)<br/>• <b>Dithering: 24-bit (Optimal)</b>", 
         "Le Shérif du Master : Gère le volume cible (LUFS). L'Output à -1.5 dB True Peak protège le fichier WAV final contre l'écrêtage lors des conversions des clients.")
    ]
    
    data = [headers]
    for row in raw_data:
        data.append([
            Paragraph(row[0], td_center),
            Paragraph(row[1], td_style),
            Paragraph(row[2], td_style),
            Paragraph(row[3], td_center),
            Paragraph(row[4], td_style),
            Paragraph(row[5], td_style),
            Paragraph(row[6], td_style)
        ])
    
    # Ajustement strict des largeurs (Total dispo A4 Paysage avec marges réduites = 781 points)
    col_widths = [18, 82, 95, 52, 90, 184, 260]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    
    ts = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A2B4C')),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DDDDDD')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ])
    
    for i in range(1, len(data)):
        if i % 2 == 0:
            ts.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F8F9FA'))
            
    table.setStyle(ts)
    elements.append(table)
    doc.build(elements)
    print(f"✅ Le document ultime révisé '{pdf_filename}' a été généré avec succès !")

if __name__ == "__main__":
    generer_pdf_charte_ultime()