from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import re

# Read the markdown file
with open('ML-PROJECT-COMPLETE-GUIDE.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Create PDF
pdf_file = 'ML-PROJECT-COMPLETE-GUIDE.pdf'
pdf = SimpleDocTemplate(
    pdf_file,
    pagesize=letter,
    rightMargin=72,
    leftMargin=72,
    topMargin=72,
    bottomMargin=36
)

# Styles
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=22,
    textColor=colors.HexColor('#1e40af'),
    spaceAfter=20,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

subtitle_style = ParagraphStyle(
    'Subtitle',
    parent=styles['Normal'],
    fontSize=12,
    textColor=colors.HexColor('#64748b'),
    spaceAfter=10,
    alignment=TA_CENTER,
    fontName='Helvetica'
)

heading1_style = ParagraphStyle(
    'CustomHeading1',
    parent=styles['Heading1'],
    fontSize=16,
    textColor=colors.HexColor('#1e40af'),
    spaceAfter=10,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

heading2_style = ParagraphStyle(
    'CustomHeading2',
    parent=styles['Heading2'],
    fontSize=13,
    textColor=colors.HexColor('#2563eb'),
    spaceAfter=8,
    spaceBefore=10,
    fontName='Helvetica-Bold'
)

heading3_style = ParagraphStyle(
    'CustomHeading3',
    parent=styles['Heading3'],
    fontSize=12,
    textColor=colors.HexColor('#3b82f6'),
    spaceAfter=6,
    spaceBefore=8,
    fontName='Helvetica-Bold'
)

code_style = ParagraphStyle(
    'Code',
    parent=styles['Code'],
    fontSize=9,
    leftIndent=20,
    spaceAfter=10,
    spaceBefore=10,
    backColor=colors.HexColor('#f3f4f6'),
    borderColor=colors.HexColor('#d1d5db'),
    borderWidth=1,
    borderPadding=8,
    fontName='Courier'
)

normal_style = ParagraphStyle(
    'CustomNormal',
    parent=styles['Normal'],
    fontSize=10,
    leading=14,
    alignment=TA_JUSTIFY,
    fontName='Helvetica'
)

bullet_style = ParagraphStyle(
    'Bullet',
    parent=styles['Normal'],
    fontSize=10,
    leading=14,
    leftIndent=20,
    fontName='Helvetica'
)

# Build story
story = []
lines = content.split('\n')
i = 0
in_code_block = False
code_block = []

while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # Code blocks
    if stripped.startswith('```'):
        if in_code_block:
            # End of code block
            if code_block:
                code_text = '<br/>'.join(code_block)
                code_text = code_text.replace('<', '&lt;').replace('>', '&gt;')
                story.append(Paragraph(code_text, code_style))
            code_block = []
            in_code_block = False
        else:
            # Start of code block
            in_code_block = True
        i += 1
        continue
    
    if in_code_block:
        code_block.append(line)
        i += 1
        continue
    
    # Headers
    if stripped.startswith('# ') and '📚' not in stripped:
        if i == 0:  # Title
            story.append(Paragraph(stripped[2:], title_style))
            story.append(Spacer(1, 12))
        else:
            story.append(PageBreak())
            story.append(Paragraph(stripped[2:], heading1_style))
            story.append(Spacer(1, 10))
    elif stripped.startswith('## '):
        story.append(Spacer(1, 8))
        story.append(Paragraph(stripped[3:], heading1_style))
        story.append(Spacer(1, 6))
    elif stripped.startswith('### '):
        story.append(Paragraph(stripped[4:], heading2_style))
        story.append(Spacer(1, 4))
    elif stripped.startswith('#### '):
        story.append(Paragraph(stripped[5:], heading3_style))
        story.append(Spacer(1, 3))
    
    # Horizontal rule
    elif stripped.startswith('---'):
        story.append(Spacer(1, 12))
    
    # Bullets
    elif stripped.startswith('- ') or stripped.startswith('* '):
        text = stripped[2:]
        story.append(Paragraph(f'• {text}', bullet_style))
    
    # Special markers
    elif any(stripped.startswith(x) for x in ['✅', '❌', '⚠️', '📊', '🤖', '💻', '📚', '🎯', '💡', '🚀']):
        story.append(Paragraph(stripped, normal_style))
        story.append(Spacer(1, 4))
    
    # Bold text
    elif stripped.startswith('**') and stripped.endswith('**') and len(stripped) > 4:
        text = stripped[2:-2]
        story.append(Paragraph(f'<b>{text}</b>', normal_style))
        story.append(Spacer(1, 6))
    
    # Skip tables and empty lines
    elif stripped.startswith('|') or not stripped:
        pass
    
    # Normal paragraphs
    else:
        if stripped:
            # Handle inline formatting
            text = stripped
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
            text = re.sub(r'`(.*?)`', r'<font face="Courier" size=9>\1</font>', text)
            story.append(Paragraph(text, normal_style))
            story.append(Spacer(1, 6))
    
    i += 1

# Build PDF
print("Creating PDF... This may take a moment.")
pdf.build(story)
print(f"\n✅ PDF created successfully: {pdf_file}")
print(f"📄 Location: D:\\project\\RecipeRecommender\\{pdf_file}")
