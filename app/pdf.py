"""
Módulo de geração de PDF.

Responsável por:
- Processar imagens
- Gerar PDF otimizado
- Incluir capa e rodapé
- Compressão de arquivo
"""

import os
from pathlib import Path
from typing import Callable, Optional, List
from PIL import Image
import fitz  # PyMuPDF
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .cover import PDFCover
from .footer import PDFFooter


class PDFBuilder:
    """Gerenciador de construção de PDFs."""
    
    # Configurações padrão
    PAGE_WIDTH, PAGE_HEIGHT = A4  # 210 x 297 mm
    MARGIN = 10 * mm  # 10 mm de margem
    DPI = 300
    COMPRESSION = True
    
    def __init__(self, progress_callback: Optional[Callable[[int], None]] = None):
        """
        Inicializa o construtor de PDF.
        
        Args:
            progress_callback: Função para reportar progresso (0-100)
        """
        self.progress_callback = progress_callback
        self.total_steps = 0
        self.current_step = 0
    
    def build(
        self,
        image_paths: List[str],
        output_path: str,
        title: str,
        subtitle: str,
        logo_path: Optional[str] = None
    ) -> tuple[bool, str]:
        """
        Constrói o PDF com as imagens fornecidas.
        
        Args:
            image_paths: Lista de caminhos das imagens
            output_path: Caminho do arquivo PDF de saída
            title: Título da capa
            subtitle: Subtítulo da capa
            logo_path: Caminho da logo
            
        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        try:
            if not image_paths:
                return False, "Nenhuma imagem para processar"
            
            # Calcular total de passos
            self.total_steps = len(image_paths) + 2  # +2 para capa e otimização
            self.current_step = 0
            
            # Criar PDF temporário
            temp_pdf_path = output_path + ".tmp"
            
            # Gerar PDF com ReportLab
            success, message = self._generate_pdf(
                image_paths,
                temp_pdf_path,
                title,
                subtitle,
                logo_path
            )
            
            if not success:
                return False, message
            
            # Otimizar PDF com PyMuPDF
            self.current_step = len(image_paths) + 1
            self._update_progress()
            
            self._optimize_pdf(temp_pdf_path, output_path)
            
            # Remover temporário
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
            
            # Obter tamanho do arquivo
            file_size = os.path.getsize(output_path)
            file_size_mb = file_size / (1024 * 1024)
            
            self.current_step = self.total_steps
            self._update_progress()
            
            message = f"PDF gerado com sucesso! ({file_size_mb:.2f} MB)"
            return True, message
        
        except Exception as e:
            return False, f"Erro ao gerar PDF: {str(e)}"
    
    def _generate_pdf(
        self,
        image_paths: List[str],
        output_path: str,
        title: str,
        subtitle: str,
        logo_path: Optional[str] = None
    ) -> tuple[bool, str]:
        """
        Gera o PDF usando ReportLab.
        
        Args:
            image_paths: Lista de caminhos das imagens
            output_path: Caminho de saída
            title: Título
            subtitle: Subtítulo
            logo_path: Caminho da logo
            
        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        try:
            c = canvas.Canvas(output_path, pagesize=A4)
            
            # Inicializar gerenciadores
            cover = PDFCover(logo_path)
            footer = PDFFooter(logo_path)
            
            # Página 1: Capa
            cover.generate_cover(c, title, subtitle)
            c.showPage()
            
            self.current_step += 1
            self._update_progress()
            
            # Páginas com imagens
            total_images = len(image_paths)
            
            for idx, image_path in enumerate(image_paths, 1):
                try:
                    self._add_image_page(c, image_path, idx, total_images + 1)
                except Exception as e:
                    return False, f"Erro ao processar {Path(image_path).name}: {str(e)}"
                
                self.current_step += 1
                self._update_progress()
            
            # Salvar PDF
            c.save()
            return True, "PDF base gerado"
        
        except Exception as e:
            return False, f"Erro ao gerar PDF base: {str(e)}"
    
    def _add_image_page(
        self,
        c: canvas.Canvas,
        image_path: str,
        page_number: int,
        total_pages: int
    ) -> None:
        """
        Adiciona uma página com imagem ao PDF.
        
        Args:
            c: Canvas do ReportLab
            image_path: Caminho da imagem
            page_number: Número da página (incluindo capa)
            total_pages: Total de páginas
        """
        # Verificar se a imagem existe
        if not os.path.exists(image_path):
            return
        
        temp_img_path = None
        
        try:
            # Abrir imagem
            with Image.open(image_path) as img:
                # Converter para RGB se necessário
                if img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        rgb_img.paste(img, mask=img.split()[-1])
                    else:
                        rgb_img.paste(img)
                    img = rgb_img
                
                # Se não é PNG, converter para PNG temporário
                if image_path.lower().endswith('.png') and img.mode == 'RGB':
                    img_to_draw = image_path
                else:
                    # Salvar em arquivo temporário
                    temp_img_path = image_path + "_temp.png"
                    img.save(temp_img_path, format='PNG')
                    img_to_draw = temp_img_path
                
                # Obter dimensões da imagem original
                img_width, img_height = img.size
                aspect_ratio = img_height / img_width
                
                # Calcular tamanho da imagem na página (respeitando margens)
                available_width = self.PAGE_WIDTH - 2 * self.MARGIN
                available_height = self.PAGE_HEIGHT - 2 * self.MARGIN - 20 * mm
                
                # Ajustar para manter proporção
                if available_width / available_height < aspect_ratio:
                    # Limitar por largura
                    display_width = available_width
                    display_height = available_width * aspect_ratio
                else:
                    # Limitar por altura
                    display_height = available_height
                    display_width = available_height / aspect_ratio
                
                # Centralizar imagem
                img_x = (self.PAGE_WIDTH - display_width) / 2
                img_y = self.PAGE_HEIGHT - self.MARGIN - display_height - 20 * mm
                
                # Desenhar imagem
                c.drawImage(
                    img_to_draw,
                    img_x,
                    img_y,
                    width=display_width,
                    height=display_height,
                    preserveAspectRatio=True
                )
            
            # Desenhar rodapé
            footer = PDFFooter()
            footer.draw_footer(c, page_number, total_pages)
            
            # Próxima página
            c.showPage()
        
        finally:
            # Limpar arquivo temporário
            if temp_img_path and os.path.exists(temp_img_path):
                try:
                    os.remove(temp_img_path)
                except Exception:
                    pass
    
    def _optimize_pdf(self, input_path: str, output_path: str) -> None:
        """
        Otimiza o PDF usando PyMuPDF.
        
        Args:
            input_path: Caminho do PDF de entrada
            output_path: Caminho do PDF de saída
        """
        try:
            # Abrir documento
            doc = fitz.open(input_path)
            
            # Otimizar
            doc.save(
                output_path,
                garbage=4,
                deflate=True,
                clean=True
            )
            
            doc.close()
        except Exception as e:
            # Se otimização falhar, copiar original
            import shutil
            shutil.copy(input_path, output_path)
    
    def _update_progress(self) -> None:
        """Atualiza o progresso da operação."""
        if self.progress_callback and self.total_steps > 0:
            progress = int((self.current_step / self.total_steps) * 100)
            self.progress_callback(min(progress, 100))
