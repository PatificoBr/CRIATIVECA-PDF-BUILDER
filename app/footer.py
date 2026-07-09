"""
Módulo de rodapé do PDF.

Responsável por:
- Desenhar rodapé em cada página
- Adicionar numeração
- Incluir logo e marca
"""

from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from typing import Optional
from PIL import Image
import os


class PDFFooter:
    """Gerenciador de rodapé para PDFs."""
    
    # Constantes de design
    LINE_WIDTH = 0.5  # pt
    LINE_COLOR = (0.7, 0.7, 0.7)  # Cinza claro
    TEXT_COLOR = (0.4, 0.4, 0.4)  # Cinza mais escuro
    FONT_NAME = "Helvetica"
    FONT_SIZE = 9
    MARGIN_BOTTOM = 10  # mm
    
    def __init__(self, logo_path: Optional[str] = None):
        """
        Inicializa o gerenciador de rodapé.
        
        Args:
            logo_path: Caminho da logo (opcional)
        """
        self.logo_path = logo_path
        self.logo_size = 15  # mm (tamanho da logo no rodapé)
        self.page_width, self.page_height = A4
    
    def draw_footer(self, c: canvas.Canvas, page_number: int, total_pages: int) -> None:
        """
        Desenha o rodapé na página.
        
        Args:
            c: Canvas do ReportLab
            page_number: Número da página atual
            total_pages: Total de páginas
        """
        # Posição y do rodapé
        footer_y = self.MARGIN_BOTTOM * mm
        
        # Desenhar linha horizontal
        self._draw_separator_line(c, footer_y)
        
        # Desenhar logo (opcional)
        if self.logo_path:
            self._draw_footer_logo(c, footer_y)
        
        # Desenhar texto "@criativeca"
        self._draw_brand_text(c, footer_y)
        
        # Desenhar numeração de página
        self._draw_page_number(c, page_number, total_pages, footer_y)
    
    def _draw_separator_line(self, c: canvas.Canvas, footer_y: float) -> None:
        """
        Desenha a linha separadora do rodapé.
        
        Args:
            c: Canvas do ReportLab
            footer_y: Posição Y da linha
        """
        margin_side = 10 * mm
        line_y = footer_y + 5 * mm
        
        c.setLineWidth(self.LINE_WIDTH)
        c.setStrokeColorRGB(*self.LINE_COLOR)
        c.line(margin_side, line_y, self.page_width - margin_side, line_y)
    
    def _draw_footer_logo(self, c: canvas.Canvas, footer_y: float) -> None:
        """
        Desenha a logo no rodapé.
        
        Args:
            c: Canvas do ReportLab
            footer_y: Posição Y de referência
        """
        try:
            # Verificar se a logo existe
            if not os.path.exists(self.logo_path):
                return
            
            # Abrir e obter dimensões da imagem
            img = Image.open(self.logo_path)
            img_width, img_height = img.size
            
            # Calcular proporção
            aspect_ratio = img_height / img_width
            logo_height = self.logo_size * aspect_ratio
            
            # Posição (centralizada horizontalmente)
            logo_x = (self.page_width - self.logo_size * mm) / 2
            logo_y = footer_y + 6 * mm
            
            # Desenhar imagem
            c.drawImage(
                self.logo_path,
                logo_x,
                logo_y,
                width=self.logo_size * mm,
                height=logo_height * mm,
                preserveAspectRatio=True
            )
        except Exception:
            # Se houver erro, apenas não desenha a logo
            pass
    
    def _draw_brand_text(self, c: canvas.Canvas, footer_y: float) -> None:
        """
        Desenha o texto da marca no rodapé.
        
        Args:
            c: Canvas do ReportLab
            footer_y: Posição Y de referência
        """
        text = "@criativeca"
        text_y = footer_y + 8 * mm
        
        # Posicionar à esquerda
        margin_left = 10 * mm
        
        c.setFont(self.FONT_NAME, self.FONT_SIZE)
        c.setFillColorRGB(*self.TEXT_COLOR)
        c.drawString(margin_left, text_y, text)
    
    def _draw_page_number(
        self, 
        c: canvas.Canvas, 
        page_number: int, 
        total_pages: int, 
        footer_y: float
    ) -> None:
        """
        Desenha a numeração de página no rodapé.
        
        Args:
            c: Canvas do ReportLab
            page_number: Número da página atual
            total_pages: Total de páginas
            footer_y: Posição Y de referência
        """
        page_text = f"Página {page_number}"
        text_y = footer_y + 8 * mm
        
        # Posicionar à direita
        margin_right = 10 * mm
        text_width = c.stringWidth(page_text, self.FONT_NAME, self.FONT_SIZE)
        text_x = self.page_width - margin_right - text_width
        
        c.setFont(self.FONT_NAME, self.FONT_SIZE)
        c.setFillColorRGB(*self.TEXT_COLOR)
        c.drawString(text_x, text_y, page_text)