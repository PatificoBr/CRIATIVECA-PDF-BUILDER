"""
Módulo de rodapé do PDF.

Responsável por:
- Desenhar rodapé em cada página
- Adicionar numeração
- Incluir logo e marca
"""

import os
from typing import Optional

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


class PDFFooter:
    """Gerenciador de rodapé para PDFs."""

    LINE_WIDTH = 0.5
    LINE_COLOR = (0.75, 0.75, 0.75)

    TEXT_COLOR = (0.35, 0.35, 0.35)

    FONT_NAME = "Helvetica"
    FONT_SIZE = 9

    MARGIN_BOTTOM = 8  # mm

    def __init__(self, logo_path: Optional[str] = None):
        self.logo_path = logo_path

        self.logo_width = 12  # mm

        self.page_width, self.page_height = A4

    def draw_footer(
        self,
        c: canvas.Canvas,
        page_number: int,
        total_pages: int
    ) -> None:

        footer_y = self.MARGIN_BOTTOM * mm

        self._draw_separator_line(c, footer_y)

        logo_end_x = 10 * mm

        if self.logo_path:
            logo_end_x = self._draw_footer_logo(c, footer_y)

        self._draw_brand_text(
            c,
            footer_y,
            logo_end_x
        )

        self._draw_page_number(
            c,
            page_number,
            total_pages,
            footer_y
        )

    def _draw_separator_line(
        self,
        c: canvas.Canvas,
        footer_y: float
    ) -> None:

        margin = 10 * mm

        line_y = footer_y + 6 * mm

        c.setStrokeColorRGB(*self.LINE_COLOR)

        c.setLineWidth(self.LINE_WIDTH)

        c.line(
            margin,
            line_y,
            self.page_width - margin,
            line_y
        )

    def _draw_footer_logo(
        self,
        c: canvas.Canvas,
        footer_y: float
    ) -> float:

        try:

            if not self.logo_path:
                return 10 * mm

            if not os.path.exists(self.logo_path):
                return 10 * mm

            img = Image.open(self.logo_path).convert("RGBA")

            img_width, img_height = img.size

            aspect = img_height / img_width

            logo_width = self.logo_width * mm
            logo_height = logo_width * aspect

            image = ImageReader(img)

            logo_x = 10 * mm

            logo_y = footer_y + 2 * mm

            c.drawImage(
                image,
                logo_x,
                logo_y,
                width=logo_width,
                height=logo_height,
                preserveAspectRatio=True,
                mask="auto",
            )

            return logo_x + logo_width + 5 * mm

        except Exception as e:

            print(f"Erro ao desenhar logo do rodapé: {e}")

            return 10 * mm

    def _draw_brand_text(
        self,
        c: canvas.Canvas,
        footer_y: float,
        start_x: float
    ) -> None:

        c.setFont(
            self.FONT_NAME,
            self.FONT_SIZE
        )

        c.setFillColorRGB(*self.TEXT_COLOR)

        text_y = footer_y + 6 * mm

        c.drawString(
            start_x,
            text_y,
            "@criativeca"
        )

    def _draw_page_number(
        self,
        c: canvas.Canvas,
        page_number: int,
        total_pages: int,
        footer_y: float
    ) -> None:

        page_text = f"{page_number} / {total_pages}"

        c.setFont(
            self.FONT_NAME,
            self.FONT_SIZE
        )

        c.setFillColorRGB(*self.TEXT_COLOR)

        text_width = c.stringWidth(
            page_text,
            self.FONT_NAME,
            self.FONT_SIZE
        )

        x = self.page_width - (10 * mm) - text_width

        y = footer_y + 6 * mm

        c.drawString(
            x,
            y,
            page_text
        )
