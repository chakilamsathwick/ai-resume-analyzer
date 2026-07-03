from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(
    ats_score,
    jd_score,
    skills,
    ai_analysis,
    filename="resume_report.pdf"
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Resume Analyzer Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"<b>ATS Score:</b> {ats_score}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>JD Match Score:</b> {jd_score}%",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "<b>Detected Skills:</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            ", ".join(skills),
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "<b>AI Analysis:</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            ai_analysis.replace("\n", "<br/>"),
            styles["Normal"]
        )
    )

    doc.build(content)

    return filename