from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, ListStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
import re

def generate_pdf_from_report(report_text: str, output_path: str) -> None:
    """
    Parse a markdown-like report_text into a formatted PDF.
    
    - Section headings: lines starting with "## N: TITLE"
    - Sub-headings: lines starting with "### TITLE"
    - Ordered lists: lines starting with "1. ", "2. ", etc.
    - Paragraphs: other text blocks separated by blank lines.
    
    Args:
      report_text: the full report string
      output_path: file path to write the PDF (e.g. "./report.pdf")
    """
    # 1. Set up document and styles
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='SectionHeading', parent=styles['Heading1'], fontSize=16, spaceAfter=12))
    styles.add(ParagraphStyle(name='SubHeading', parent=styles['Heading2'], fontSize=14, spaceAfter=8))
    body_style = styles['BodyText']
    list_style = ListStyle('OrderedList', leftIndent=20, bulletType='1', bulletFontName=body_style.fontName)
    
    flowables = []
    
    # 2. Tokenize into lines and process
    lines = report_text.splitlines()
    buffer = []           # accumulate paragraph lines
    in_list = False
    list_items = []
    
    def flush_paragraph():
        nonlocal buffer
        text = ' '.join(l.strip() for l in buffer).strip()
        if text:
            flowables.append(Paragraph(text, body_style))
            flowables.append(Spacer(1, 6))
        buffer = []
    
    def flush_list():
        nonlocal list_items
        if list_items:
            lf = ListFlowable(
                [ListItem(Paragraph(item, body_style)) for item in list_items],
                style=list_style
            )
            flowables.append(lf)
            flowables.append(Spacer(1, 6))
        list_items = []
    
    for line in lines:
        # Section heading
        m_sec = re.match(r'##\s*\d+:\s*(.+)', line)
        if m_sec:
            # flush any pending text
            if in_list:
                flush_list()
                in_list = False
            flush_paragraph()
            flowables.append(Paragraph(m_sec.group(1).upper(), styles['SectionHeading']))
            continue
        
        # Sub-heading
        m_sub = re.match(r'###\s*(.+)', line)
        if m_sub:
            if in_list:
                flush_list()
                in_list = False
            flush_paragraph()
            flowables.append(Paragraph(m_sub.group(1), styles['SubHeading']))
            continue
        
        # Ordered-list item
        m_li = re.match(r'\d+\.\s+(.+)', line)
        if m_li:
            if not in_list:
                flush_paragraph()
            in_list = True
            list_items.append(m_li.group(1).strip())
            continue
        
        # Blank line
        if not line.strip():
            if in_list:
                flush_list()
                in_list = False
            else:
                flush_paragraph()
            continue
        
        # Regular paragraph line
        buffer.append(line)
    
    # Flush any trailing content
    if in_list:
        flush_list()
    else:
        flush_paragraph()
    
    # 3. Build PDF
    doc.build(flowables)



if __name__ == '__main__':
    report_markdown = """

"""

    generate_pdf_from_report(report_markdown, 'melina_brand_alchemy.pdf')
    print("PDF written to melina_brand_alchemy.pdf")