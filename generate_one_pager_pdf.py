import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, HRFlowable
from reportlab.lib import colors

def create_one_pager_pdf():
    script_dir = Path(__file__).resolve().parent
    pdf_path = script_dir.parents[1] / "one_pager_foliotype.pdf"
    
    if pdf_path.exists():
        try:
            os.remove(pdf_path)
        except PermissionError:
            pdf_path = script_dir.parents[1] / "one_pager_foliotype_clean.pdf"

    # Marges fixes et sécurisées à 36 points pour maximiser l'emprise verticale
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    PRIMARY_COLOR = colors.HexColor("#1A2B4C")
    SECONDARY_COLOR = colors.HexColor("#4A5568")
    TEXT_COLOR = colors.HexColor("#2D3748")
    
    styles = getSampleStyleSheet()
    
    # Calibrage strict anti-débordement
    title_style = ParagraphStyle(
        'PDFTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=22, leading=25, textColor=PRIMARY_COLOR, alignment=1, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'PDFSubtitle', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=10, leading=13, textColor=SECONDARY_COLOR, alignment=1, spaceAfter=10
    )
    h1_style = ParagraphStyle(
        'PDFH1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12.5, leading=15, textColor=PRIMARY_COLOR, spaceBefore=8, spaceAfter=3
    )
    h2_style = ParagraphStyle(
        'PDFH2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=PRIMARY_COLOR, spaceBefore=6, spaceAfter=2
    )
    body_style = ParagraphStyle(
        'PDFBody', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=TEXT_COLOR, spaceAfter=5
    )
    bullet_style = ParagraphStyle(
        'PDFBullet', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=TEXT_COLOR, leftIndent=12, firstLineIndent=-8, spaceAfter=3
    )

    story = []

    # --- EN-TÊTE ---
    story.append(Paragraph("FOLIOTYPE PROTOCOL", title_style))
    story.append(Paragraph("Architectures d'automatisation vocale premium pour les professionnels de l'écrit et de la formation.", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=6))

    # --- LE CONSTAT ---
    story.append(Paragraph("LE CONSTAT", h1_style))
    story.append(Paragraph("La consommation de contenus textuels denses (essais, revues, modules pédagogiques) se heurte aujourd'hui à un obstacle majeur : le manque de temps des lecteurs. La post-production audio traditionnelle (studios, comédiens professionnels) reste quant à elle trop coûteuse et trop lente pour suivre le rythme des publications modernes.", body_style))
    story.append(Paragraph("Foliotype Protocol élimine ces barrières grâce à un pipeline d'ingénierie vocale automatisé, offrant une diction humaine de standard studio sans aucune friction technique.", body_style))

    # --- NOS DEUX PILIERS ---
    story.append(Paragraph("NOS DEUX PILIERS D'EXPERTISE", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=SECONDARY_COLOR, spaceAfter=5))
    
    story.append(Paragraph("1. TEXT-TO-PODCAST (Substack, Revues & Newsletters)", h2_style))
    story.append(Paragraph("Conversion chirurgicale de vos articles écrits et essais de fond en expériences audio haute fidélité.", body_style))
    story.append(Paragraph("&bull; <b>Diction Académique &amp; Journalistique :</b> Restitution fluide, ton posé et maîtrise absolue des structures textuelles complexes (&quot;Zero-Robot-Sound&quot;).", bullet_style))
    story.append(Paragraph("&bull; <b>Rétention &amp; Multitasking :</b> Engagez et fidélisez votre audience d'abonnés en situation de mobilité (transports, sport, veille stratégique).", bullet_style))
    story.append(Paragraph("&bull; <b>Valorisation du Catalogue :</b> Générez instantanément une déclinaison audio premium de vos archives écrites sans matériel ni micro.", bullet_style))
    
    story.append(Paragraph("2. VOCALISATION DIGITAL LEARNING (EdTech &amp; LMS)", h2_style))
    story.append(Paragraph("Industrialisation audio de vos modules e-learning, scripts pédagogiques et catalogues de formation continue.", body_style))
    story.append(Paragraph("&bull; <b>Production à Grande Échelle :</b> Génération instantanée de dizaines d'heures de cours audio avec une régularité acoustique parfaite.", bullet_style))
    story.append(Paragraph("&bull; <b>Standard Acoustique Premium :</b> Élimination algorithmique des micro-respirations artificielles et de la sibilance pour garantir le confort d'apprentissage.", bullet_style))
    story.append(Paragraph("&bull; <b>Rentabilité Critique :</b> Réduction de 80 % des coûts de studio et mise à jour immédiate de vos contenus textuels dès qu'un script évolue.", bullet_style))

    # --- POURQUOI FOLIOTYPE ---
    story.append(Paragraph("POURQUOI FOLIOTYPE PROTOCOL ?", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=SECONDARY_COLOR, spaceAfter=5))
    story.append(Paragraph("<b>[+] PRÉCISION :</b> Alignement temporel et gestion dynamique des silences calibrés pour les formats longs.", bullet_style))
    story.append(Paragraph("<b>[+] SIMPLICITÉ :</b> Des pipelines automatisés conçus pour s'intégrer directement dans les flux des éditeurs et concepteurs.", bullet_style))
    story.append(Paragraph("<b>[+] VALEUR :</b> Un positionnement premium pour transformer l'écrit en un actif audio haut de gamme.", bullet_style))

    # --- CONTACT ---
    story.append(Paragraph("CONTACT &amp; DÉMO", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY_COLOR, spaceAfter=5))
    story.append(Paragraph("Prêt à automatiser votre production audio ? Envoyez-nous un extrait textuel ou un script de 30 secondes. Nous vous renvoyons votre démo Foliotype sous 24 heures.", body_style))
    
    contact_style = ParagraphStyle('PDFContact', parent=body_style, fontName='Helvetica-Bold', textColor=PRIMARY_COLOR, alignment=1, spaceBefore=2)
    
    # Encapsulation de la ligne finale dans une structure fixe pour empêcher le saut de page
    contact_p = Paragraph("Contact : correlation@foliotype-protocol.com   |   LinkedIn : www.linkedin.com/in/pier-ntsama", contact_style)
    contact_table = Table([[contact_p]], colWidths=[doc.width])
    contact_table.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(contact_table)

    doc.build(story)
    print(f"✅ PDF VERROUILLÉ SUR 1 PAGE : {pdf_path.resolve()}")

if __name__ == "__main__":
    create_one_pager_pdf()