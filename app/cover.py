"""
Módulo de capa do PDF.

Responsável por:
- Gerar capa visual profissional
- Incorporar logo
- Exibir título e subtítulo
"""

from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

from PIL import Image
import os
from typing import Optional


class PDFCover:
    """Gerenciador de capa para PDF."""

    # Cores do design
    BG_COLOR = HexColor("#F8F9FA")
    ACCENT_COLOR = HexColor("#2C3E50")
    TEXT_COLOR = HexColor("#2C3E50")
    SUBTITLE_COLOR = HexColor("#7F8C8D")

    # Dimensões da página A4
    PAGE_WIDTH, PAGE_HEIGHT = A4

    def __init__(self, logo_path: Optional[str] = None):
        """
        Inicializa o gerenciador de capa.

        Args:
            logo_path: Caminho da logo (opcional)
        """
        self.logo_path = logo_path
        self.logo_size = 75  # mm

    def generate_cover(
        self,
        c: canvas.Canvas,
        title: str,
        subtitle: str
    ) -> None:
        """
        Gera a capa do PDF.

        Args:
            c: Canvas do ReportLab
            title: Título da capa
            subtitle: Subtítulo da capa
        """
        # Fundo
        self._draw_background(c)

        # Desenhar elementos
        self._draw_logo(c)
        self._draw_title(c, title)
        self._draw_subtitle(c, subtitle)
        self._draw_decorative_elements(c)

    def _draw_background(self, c: canvas.Canvas) -> None:
        """
        Desenha o fundo da capa.

        Args:
            c: Canvas do ReportLab
        """
        c.setFillColor(self.BG_COLOR)
        c.rect(0, 0, self.PAGE_WIDTH, self.PAGE_HEIGHT, fill=1, stroke=0)

        # Linha decorativa no topo
        line_height = 15 * mm
        c.setFillColor(self.ACCENT_COLOR)
        c.rect(0, self.PAGE_HEIGHT - line_height,
               self.PAGE_WIDTH, line_height, fill=1, stroke=0)

    def _draw_logo(self, c: canvas.Canvas) -> None:
        """
        Desenha a logo na capa.

        Args:
            c: Canvas do ReportLab
        """
        if not self.logo_path or not os.path.exists(self.logo_path):
            return

        try:
            # Obter dimensões da imagem
            img = Image.open(self.logo_path).convert("RGBA")

            image = ImageReader(img)

            img_width, img_height = img.size

            # Calcular proporção
            aspect_ratio = img_height / img_width
            logo_height = self.logo_size * aspect_ratio

            # Posição (centralizada horizontalmente, na parte superior)
            logo_x = (self.PAGE_WIDTH - self.logo_size * mm) / 2
            logo_y = self.PAGE_HEIGHT - 85 * mm

            # Desenhar imagem
            c.drawImage(
                image,
                logo_x,
                logo_y,
                width=self.logo_size * mm,
                height=logo_height * mm,
                preserveAspectRatio=True,
                mask="auto"
            )
        except Exception:
            # Se houver erro, apenas não desenha a logo
            pass

    def _draw_title(self, c: canvas.Canvas, title: str) -> None:
        """
        Desenha o título na capa.

        Args:
            c: Canvas do ReportLab
            title: Texto do título
        """
        # Posição vertical (centro da página)
        title_y = self.PAGE_HEIGHT / 2 + 20 * mm

        # Font
        font_name = "Helvetica-Bold"
        font_size = 48

        c.setFont(font_name, font_size)
        c.setFillColor(self.TEXT_COLOR)

        # Quebrar título em múltiplas linhas se necessário
        max_width = self.PAGE_WIDTH - 40 * mm
        lines = self._wrap_text(title, font_name, font_size, max_width)

        # Desenhar linhas
        current_y = title_y
        for line in lines:
            text_width = c.stringWidth(line, font_name, font_size)
            x = (self.PAGE_WIDTH - text_width) / 2
            c.drawString(x, current_y, line)
            current_y -= font_size * 1.3

    def _draw_subtitle(self, c: canvas.Canvas, subtitle: str) -> None:
        """
        Desenha o subtítulo na capa.

        Args:
            c: Canvas do ReportLab
            subtitle: Texto do subtítulo
        """
        # Posição vertical (abaixo do título)
        subtitle_y = self.PAGE_HEIGHT / 2 - 40 * mm

        # Font
        font_name = "Helvetica"
        font_size = 24

        c.setFont(font_name, font_size)
        c.setFillColor(self.SUBTITLE_COLOR)

        # Quebrar subtítulo em múltiplas linhas se necessário
        max_width = self.PAGE_WIDTH - 40 * mm
        lines = self._wrap_text(subtitle, font_name, font_size, max_width)

        # Desenhar linhas
        current_y = subtitle_y
        for line in lines:
            text_width = c.stringWidth(line, font_name, font_size)
            x = (self.PAGE_WIDTH - text_width) / 2
            c.drawString(x, current_y, line)
            current_y -= font_size * 1.3

    def _draw_decorative_elements(self, c: canvas.Canvas) -> None:
        """
        Desenha elementos decorativos na capa.

        Args:
            c: Canvas do ReportLab
        """
        # Linha decorativa no rodapé
        c.setLineWidth(2)
        c.setStrokeColor(self.ACCENT_COLOR)

        line_y = 40 * mm
        margin_sides = 50 * mm

        c.line(margin_sides, line_y, self.PAGE_WIDTH - margin_sides, line_y)

        # Pequeno texto no rodapé
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColor(self.SUBTITLE_COLOR)
        footer_text = "Criativeca PDF Builder"
        text_width = c.stringWidth(footer_text, "Helvetica-Oblique", 10)
        x = (self.PAGE_WIDTH - text_width) / 2
        c.drawString(x, 25 * mm, footer_text)

    @staticmethod
    def _wrap_text(text: str, font_name: str, font_size: int, max_width: float) -> list[str]:
        """
        Quebra texto em múltiplas linhas para caber em uma largura.

        Args:
            text: Texto a quebrar
            font_name: Nome da fonte
            font_size: Tamanho da fonte
            max_width: Largura máxima em pontos

        Returns:
            Lista de linhas
        """
        from reportlab.pdfgen import canvas as canvas_module

        # Usar canvas temporário para medir texto
        temp_canvas = canvas_module.Canvas("")

        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + " " + word if current_line else word
            text_width = temp_canvas.stringWidth(
                test_line, font_name, font_size)

            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines if lines else [text]
