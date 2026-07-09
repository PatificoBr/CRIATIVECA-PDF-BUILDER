"""
Módulo de geração de PDF.

Responsável por:

- Processar imagens
- Gerar PDF profissional
- Inserir capa
- Inserir rodapé
- Otimizar o arquivo final
"""

import os
from pathlib import Path
from typing import Callable, Optional

import fitz
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from .cover import PDFCover
from .footer import PDFFooter


class PDFBuilder:
    """Classe responsável pela geração do PDF."""

    PAGE_WIDTH, PAGE_HEIGHT = A4

    TOP_MARGIN = 8 * mm
    SIDE_MARGIN = 8 * mm
    BOTTOM_MARGIN = 8 * mm

    FOOTER_HEIGHT = 18 * mm

    DPI = 300

    def __init__(
        self,
        progress_callback: Optional[Callable[[int], None]] = None,
    ):

        self.progress_callback = progress_callback

        self.total_steps = 0
        self.current_step = 0

        self.logo_path = None

    def build(
        self,
        image_paths: list[str],
        output_path: str,
        title: str,
        subtitle: str,
        logo_path: Optional[str] = None,
    ) -> tuple[bool, str]:

        try:

            if not image_paths:
                return False, "Nenhuma imagem encontrada."

            self.logo_path = logo_path

            self.total_steps = len(image_paths) + 2
            self.current_step = 0

            temp_pdf = output_path + ".tmp"

            ok, msg = self._generate_pdf(
                image_paths=image_paths,
                output_path=temp_pdf,
                title=title,
                subtitle=subtitle,
            )

            if not ok:
                return False, msg

            self.current_step += 1
            self._update_progress()

            self._optimize_pdf(
                temp_pdf,
                output_path,
            )

            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)

            size = os.path.getsize(output_path) / (1024 * 1024)

            self.current_step = self.total_steps
            self._update_progress()

            return True, f"PDF gerado com sucesso ({size:.2f} MB)"

        except Exception as e:

            return False, str(e)

    def _generate_pdf(
        self,
        image_paths: list[str],
        output_path: str,
        title: str,
        subtitle: str,
    ) -> tuple[bool, str]:

        try:

            c = canvas.Canvas(
                output_path,
                pagesize=A4,
            )

            c.setAuthor("PatificoBr")
            c.setCreator("Criativeca PDF Builder")
            c.setTitle(title)
            c.setSubject("Livro para Colorir")

            cover = PDFCover(self.logo_path)

            footer = PDFFooter(self.logo_path)

            cover.generate_cover(
                c,
                title,
                subtitle,
            )

            c.showPage()

            self.current_step += 1
            self._update_progress()

            total_pages = len(image_paths)

            for page, image_path in enumerate(image_paths, start=1):

                self._add_image_page(
                    canvas_obj=c,
                    footer=footer,
                    image_path=image_path,
                    page_number=page,
                    total_pages=total_pages,
                )

                self.current_step += 1
                self._update_progress()

            c.save()

            return True, "OK"

        except Exception as e:

            return False, str(e)

    def _add_image_page(
        self,
        canvas_obj: canvas.Canvas,
        footer: PDFFooter,
        image_path: str,
        page_number: int,
        total_pages: int,
    ) -> None:

        if not os.path.exists(image_path):
            return

        temp_image = None

        try:

            with Image.open(image_path) as img:

                if img.mode in ("RGBA", "LA", "P"):

                    background = Image.new(
                        "RGB",
                        img.size,
                        (255, 255, 255),
                    )

                    if img.mode == "RGBA":
                        background.paste(
                            img,
                            mask=img.split()[-1],
                        )
                    else:
                        background.paste(img)

                    img = background

                if image_path.lower().endswith(".png") and img.mode == "RGB":

                    image_to_draw = image_path

                else:

                    temp_image = image_path + "_temp.png"

                    img.save(
                        temp_image,
                        "PNG",
                        optimize=True,
                    )

                    image_to_draw = temp_image

                img_width, img_height = img.size

                aspect = img_height / img_width

                usable_width = (
                    self.PAGE_WIDTH
                    - (self.SIDE_MARGIN * 2)
                )

                usable_height = (
                    self.PAGE_HEIGHT
                    - self.TOP_MARGIN
                    - self.BOTTOM_MARGIN
                    - self.FOOTER_HEIGHT
                )

                if usable_width / usable_height < aspect:

                    draw_width = usable_width

                    draw_height = draw_width * aspect

                else:

                    draw_height = usable_height

                    draw_width = draw_height / aspect

                scale = 0.985

                draw_width *= scale
                draw_height *= scale

                area_left = self.SIDE_MARGIN

                area_bottom = (
                    self.BOTTOM_MARGIN
                    + self.FOOTER_HEIGHT
                )

                area_width = usable_width

                area_height = usable_height

                x = area_left + (
                    area_width - draw_width
                ) / 2

                y = area_bottom + (
                    area_height - draw_height
                ) / 2

                canvas_obj.drawImage(
                    image_to_draw,
                    x,
                    y,
                    width=draw_width,
                    height=draw_height,
                    preserveAspectRatio=True,
                )

            footer.draw_footer(
                canvas_obj,
                page_number,
                total_pages,
            )

            canvas_obj.showPage()

        finally:

            if (
                temp_image
                and os.path.exists(temp_image)
            ):
                try:
                    os.remove(temp_image)
                except Exception:
                    pass

    def _optimize_pdf(
        self,
        input_path: str,
        output_path: str,
    ) -> None:

        try:

            doc = fitz.open(input_path)

            doc.save(
                output_path,
                garbage=4,
                deflate=True,
                clean=True,
            )

            doc.close()

        except Exception:

            import shutil

            shutil.copy2(
                input_path,
                output_path,
            )

    def _update_progress(self) -> None:
        """
        Atualiza a barra de progresso.
        """

        if (
            self.progress_callback is None
            or self.total_steps == 0
        ):
            return

        progress = int(
            (self.current_step / self.total_steps) * 100
        )

        self.progress_callback(
            min(progress, 100)
        )
