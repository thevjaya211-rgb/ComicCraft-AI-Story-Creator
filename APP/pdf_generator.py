import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PANELS_DIR = os.path.join(
    BASE_DIR,
    "static",
    "panels"
)

EXPORTS_DIR = os.path.join(
    BASE_DIR,
    "static",
    "exports"
)

STORY_FILE = os.path.join(
    BASE_DIR,
    "story.txt"
)

PDF_FILE = os.path.join(
    EXPORTS_DIR,
    "comic.pdf"
)


def create_comic_pdf():

    os.makedirs(
        EXPORTS_DIR,
        exist_ok=True
    )

    pdf = canvas.Canvas(
        PDF_FILE,
        pagesize=A4
    )

    page_width, page_height = A4

    # ==============================
    # TITLE
    # ==============================

    pdf.setFont(
        "Helvetica-Bold",
        24
    )

    pdf.drawCentredString(
        page_width / 2,
        page_height - 50,
        "ComicCraft AI"
    )

    # ==============================
    # STORY
    # ==============================

    if os.path.exists(STORY_FILE):

        with open(
            STORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            story = file.read()

        pdf.setFont(
            "Helvetica",
            11
        )

        text = pdf.beginText(
            50,
            page_height - 90
        )

        text.setLeading(16)

        for line in story.splitlines():

            text.textLine(line)

        pdf.drawText(text)

    pdf.showPage()

    # ==============================
    # 5 COMIC PANELS
    # ==============================

    for i in range(1, 6):

        image_path = os.path.join(
            PANELS_DIR,
            f"panel_{i}.png"
        )

        if not os.path.exists(image_path):
            continue

        pdf.setFont(
            "Helvetica-Bold",
            18
        )

        pdf.drawString(
            50,
            page_height - 45,
            f"Comic Panel {i}"
        )

        image = ImageReader(
            image_path
        )

        max_width = page_width - 100
        max_height = page_height - 100

        pdf.drawImage(
            image,
            50,
            60,
            width=max_width,
            height=max_height,
            preserveAspectRatio=True,
            anchor="c"
        )

        pdf.showPage()

    pdf.save()

    return PDF_FILE


if __name__ == "__main__":

    pdf_path = create_comic_pdf()

    print(
        f"Comic PDF created successfully: {pdf_path}"
    )