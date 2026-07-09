#!/usr/bin/env python3
"""
Criativeca PDF Builder
Transformando imagens em PDFs profissionais para impressão.

Ponto de entrada da aplicação.
"""

import sys
from pathlib import Path

# Adicionar o diretório do projeto ao path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.gui import PDFBuilderApp


def main():
    """Função principal."""
    app = PDFBuilderApp()
    app.mainloop()


if __name__ == "__main__":
    main()