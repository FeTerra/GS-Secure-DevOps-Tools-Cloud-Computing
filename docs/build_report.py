"""Gera o relatório PDF a partir de relatorio-devops.md usando ReportLab."""
from pathlib import Path
import shutil
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, Flowable
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / "docs" / "relatorio-devops.md"
OUTPUT = BASE.parent / "output" / "DevOps_Ponto_Falante.pdf"
REPO_COPY = BASE / "docs" / "DevOps_Ponto_Falante.pdf"
NAVY, TEAL, PALE = colors.HexColor("#12243A"), colors.HexColor("#087F8C"), colors.HexColor("#EAF3F5")

class Architecture(Flowable):
    def __init__(self):
        super().__init__(); self.width = 170*mm; self.height = 70*mm
    def draw(self):
        d = Drawing(self.width, self.height)
        nodes = [(3,47,44,16,"Navegador"),(59,47,50,16,"Lightsail · FastAPI"),(121,47,48,16,"Métricas CPU/memória"),(3,8,44,16,"GitHub Actions"),(55,8,61,16,"Gitleaks · Semgrep · Trivy"),(125,8,44,16,"GHCR · imagem")]
        for x,y,w,h,label in nodes:
            d.add(Rect(x*mm,y*mm,w*mm,h*mm,rx=3,ry=3,fillColor=PALE,strokeColor=TEAL,strokeWidth=1.2))
            d.add(String((x+w/2)*mm,(y+h/2)*mm-3,label,textAnchor="middle",fontName="Helvetica",fontSize=7.3,fillColor=NAVY))
        def arrow(x1,y1,x2,y2):
            d.add(Line(x1*mm,y1*mm,x2*mm,y2*mm,strokeColor=TEAL,strokeWidth=1.1))
            d.add(Polygon([x2*mm,y2*mm,x2*mm-3,y2*mm+2,x2*mm-3,y2*mm-2],fillColor=TEAL,strokeColor=TEAL))
        arrow(47,55,59,55); arrow(109,55,121,55); arrow(47,16,55,16); arrow(116,16,125,16); arrow(99,16,99,47); arrow(147,24,99,47)
        d.drawOn(self.canv,0,0)

def clean(s):
    s=s.strip().replace("&","&amp;")
    s=re.sub(r"\*\*(.+?)\*\*",r"<b>\1</b>",s)
    s=re.sub(r"`([^`]+)`",r"<font name='Courier' size='8'>\1</font>",s)
    s=re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",r"<link href='\2' color='#087F8C'><u>\1</u></link>",s)
    return s

def footer(canvas,doc):
    canvas.saveState(); w,h=A4
    canvas.setStrokeColor(colors.HexColor("#D7E1E8")); canvas.line(20*mm,15*mm,w-20*mm,15*mm)
    canvas.setFont("Helvetica",8); canvas.setFillColor(colors.HexColor("#536578"))
    canvas.drawString(20*mm,10*mm,"Ponto Falante · Secure DevOps · Relatório-base"); canvas.drawRightString(w-20*mm,10*mm,str(doc.page))
    if doc.page>1:
        canvas.setFont("Helvetica-Bold",8); canvas.setFillColor(TEAL); canvas.drawString(20*mm,h-12*mm,"GLOBAL SOLUTION 2026.2  |  DISCIPLINA 6 DE 7")
    canvas.restoreState()

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitlePF",parent=styles["Title"],fontName="Helvetica-Bold",fontSize=24,leading=29,textColor=NAVY,alignment=1,spaceAfter=9*mm))
styles.add(ParagraphStyle(name="SubPF",parent=styles["Normal"],fontSize=12,leading=17,textColor=TEAL,alignment=1,spaceAfter=5*mm))
styles.add(ParagraphStyle(name="H1PF",parent=styles["Heading1"],fontName="Helvetica-Bold",fontSize=16,leading=20,textColor=NAVY,spaceBefore=6*mm,spaceAfter=3*mm,keepWithNext=True))
styles.add(ParagraphStyle(name="H2PF",parent=styles["Heading2"],fontName="Helvetica-Bold",fontSize=11,leading=14,textColor=TEAL,spaceBefore=4*mm,spaceAfter=2*mm,keepWithNext=True))
styles.add(ParagraphStyle(name="BodyPF",parent=styles["BodyText"],fontName="Helvetica",fontSize=9,leading=13,textColor=colors.HexColor("#223344"),spaceAfter=2.5*mm))
styles.add(ParagraphStyle(name="SmallPF",parent=styles["BodyText"],fontSize=8,leading=10,textColor=colors.HexColor("#4C5B6A")))
styles.add(ParagraphStyle(name="TableHeadPF",parent=styles["BodyText"],fontSize=8,leading=10,textColor=colors.white,fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="BulletPF",parent=styles["BodyText"],fontSize=9,leading=12,leftIndent=12,firstLineIndent=-8,spaceAfter=1.2*mm))

lines=SOURCE.read_text(encoding="utf-8").splitlines()
story=[Spacer(1,22*mm),Paragraph("PONTO FALANTE",styles["SubPF"]),Paragraph("Deploy Blindado",styles["TitlePF"]),Paragraph("Secure DevOps Tools &amp; Cloud Computing · Disciplina 6 de 7",styles["SubPF"]),Spacer(1,10*mm)]
started=False; in_code=False; code=[]; i=0
while i<len(lines):
    line=lines[i].strip()
    if line.startswith("# "):
        if not started: started=True; i+=1; continue
        story.append(Paragraph(clean(line[2:]),styles["H1PF"]))
    elif line.startswith("## "): story.append(Paragraph(clean(line[3:]),styles["H1PF"]))
    elif line.startswith("### "): story.append(Paragraph(clean(line[4:]),styles["H2PF"]))
    elif line.startswith("```"):
        if not in_code: in_code=True; code=[]
        else:
            in_code=False
            if any("flowchart" in x for x in code): story.append(Architecture()); story.append(Spacer(1,3*mm))
            elif code: story.append(Preformatted("\n".join(code),ParagraphStyle("code",fontName="Courier",fontSize=7,leading=9,backColor=PALE,borderPadding=5)))
    elif in_code: code.append(line)
    elif line.startswith("| "):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith("|"):
            cells=[x.strip() for x in lines[i].strip().strip("|").split("|")]
            if not all(re.fullmatch(r":?-{2,}:?",c) for c in cells):
                cell_style=styles["TableHeadPF"] if not rows else styles["SmallPF"]
                rows.append([Paragraph(clean(c),cell_style) for c in cells])
            i+=1
        if rows:
            widths=[(A4[0]-40*mm)/len(rows[0])]*len(rows[0]); tab=Table(rows,colWidths=widths,repeatRows=1,hAlign="LEFT")
            tab.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,PALE]),("GRID",(0,0),(-1,-1),.35,colors.HexColor("#C8D5DF")),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
            story.extend([tab,Spacer(1,2*mm)])
        continue
    elif line.startswith("- "): story.append(Paragraph("•  "+clean(line[2:]),styles["BulletPF"]))
    elif re.match(r"^\d+\. ",line): story.append(Paragraph(clean(line),styles["BulletPF"]))
    elif line: story.append(Paragraph(clean(line),styles["BodyPF"]))
    i+=1

doc=SimpleDocTemplate(str(OUTPUT),pagesize=A4,rightMargin=20*mm,leftMargin=20*mm,topMargin=22*mm,bottomMargin=22*mm,title="Ponto Falante — Secure DevOps",author="Equipe CitizenTech — FIAP Global Solution")
doc.build(story,onFirstPage=footer,onLaterPages=footer)
shutil.copy2(OUTPUT, REPO_COPY)
print(OUTPUT)
