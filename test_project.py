#!/usr/bin/env python3
"""
Script de teste para validar o Criativeca PDF Builder.

Este script verifica se todos os módulos estão OK e se o projeto
está pronto para uso.
"""

import os
import sys
from pathlib import Path

# Cores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'

def print_status(status: str, message: str) -> None:
    """Imprime status com cor."""
    if status == "ok":
        print(f"{GREEN}✓{END} {message}")
    elif status == "error":
        print(f"{RED}✗{END} {message}")
    elif status == "warning":
        print(f"{YELLOW}⚠{END} {message}")
    elif status == "info":
        print(f"{BLUE}ℹ{END} {message}")

def check_files():
    """Verifica se todos os arquivos necessários existem."""
    print(f"\n{BLUE}=== VERIFICANDO ARQUIVOS ==={END}\n")
    
    project_root = Path(__file__).parent
    
    files_to_check = [
        "main.py",
        "requirements.txt",
        "README.md",
        "create_assets.py",
        "app/__init__.py",
        "app/gui.py",
        "app/pdf.py",
        "app/cover.py",
        "app/footer.py",
        "app/validator.py",
        "app/utils.py",
        "assets/logo.png",
        "assets/icon.ico",
    ]
    
    all_ok = True
    for file_path in files_to_check:
        full_path = project_root / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print_status("ok", f"{file_path} ({size:,} bytes)")
        else:
            print_status("error", f"{file_path} NÃO ENCONTRADO")
            all_ok = False
    
    return all_ok

def check_imports():
    """Verifica se os módulos podem ser importados."""
    print(f"\n{BLUE}=== VERIFICANDO IMPORTAÇÕES ==={END}\n")
    
    all_ok = True
    
    # Adicionar projeto ao path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # Tentar importar módulos
    modules = [
        ("PIL", "Pillow"),
        ("reportlab", "ReportLab"),
        ("fitz", "PyMuPDF"),
        ("natsort", "natsort"),
        ("customtkinter", "CustomTkinter"),
    ]
    
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print_status("ok", f"{display_name} instalado")
        except ImportError:
            print_status("error", f"{display_name} NÃO INSTALADO")
            all_ok = False
    
    # Tentar importar módulos do projeto
    print()
    project_modules = [
        ("app", "app"),
        ("app.gui", "app.gui"),
        ("app.pdf", "app.pdf"),
        ("app.validator", "app.validator"),
        ("app.utils", "app.utils"),
    ]
    
    for module_name, display_name in project_modules:
        try:
            __import__(module_name)
            print_status("ok", f"{display_name} pode ser importado")
        except ImportError as e:
            print_status("error", f"{display_name} erro ao importar: {e}")
            all_ok = False
    
    return all_ok

def check_folders():
    """Verifica se as pastas necessárias existem."""
    print(f"\n{BLUE}=== VERIFICANDO PASTAS ==={END}\n")
    
    project_root = Path(__file__).parent
    
    folders = [
        "app",
        "assets",
        "input",
        "output",
    ]
    
    all_ok = True
    for folder in folders:
        folder_path = project_root / folder
        if folder_path.exists() and folder_path.is_dir():
            files_count = len(list(folder_path.glob("*")))
            print_status("ok", f"{folder}/ ({files_count} itens)")
        else:
            print_status("error", f"{folder}/ NÃO ENCONTRADA")
            all_ok = False
    
    return all_ok

def check_requirements():
    """Verifica o arquivo requirements.txt."""
    print(f"\n{BLUE}=== VERIFICANDO DEPENDÊNCIAS ==={END}\n")
    
    project_root = Path(__file__).parent
    req_file = project_root / "requirements.txt"
    
    if not req_file.exists():
        print_status("error", "requirements.txt não encontrado")
        return False
    
    try:
        with open(req_file, 'r') as f:
            requirements = f.read().strip().split('\n')
        
        print_status("info", f"Dependências definidas:")
        for req in requirements:
            if req.strip():
                print(f"  • {req}")
        
        return True
    except Exception as e:
        print_status("error", f"Erro ao ler requirements.txt: {e}")
        return False

def check_code_quality():
    """Verifica qualidade básica do código."""
    print(f"\n{BLUE}=== VERIFICANDO QUALIDADE DO CÓDIGO ==={END}\n")
    
    project_root = Path(__file__).parent
    app_dir = project_root / "app"
    
    all_ok = True
    
    # Verificar type hints em cada módulo
    modules_to_check = [
        "gui.py",
        "pdf.py",
        "validator.py",
        "utils.py",
        "cover.py",
        "footer.py",
    ]
    
    for module_file in modules_to_check:
        file_path = app_dir / module_file
        
        if not file_path.exists():
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            has_docstring = '"""' in content or "'''" in content
            has_type_hints = "->" in content
            has_classes = "class " in content
            
            status = "ok" if has_type_hints and has_docstring else "warning"
            has_type = "sim" if has_type_hints else "não"
            
            if status == "ok":
                print_status("ok", f"{module_file} (type hints: {has_type}, docstrings: sim)")
            else:
                print_status("warning", f"{module_file} (considere adicionar mais documentação)")
        
        except Exception as e:
            print_status("error", f"{module_file}: {e}")
            all_ok = False
    
    return all_ok

def main():
    """Função principal."""
    print(f"\n{BLUE}{'='*60}{END}")
    print(f"{BLUE}  CRIATIVECA PDF BUILDER - TESTE DE VALIDAÇÃO{END}")
    print(f"{BLUE}{'='*60}{END}")
    
    results = {
        "Arquivos": check_files(),
        "Pastas": check_folders(),
        "Dependências": check_requirements(),
        "Importações": check_imports(),
        "Qualidade": check_code_quality(),
    }
    
    # Resumo
    print(f"\n{BLUE}=== RESUMO ==={END}\n")
    
    all_ok = all(results.values())
    
    for category, status in results.items():
        if status:
            print_status("ok", f"{category}: OK")
        else:
            print_status("error", f"{category}: PROBLEMAS DETECTADOS")
    
    print()
    
    if all_ok:
        print_status("ok", "Projeto está pronto para uso!")
        print(f"\n{GREEN}Para iniciar a aplicação, execute:{END}")
        print(f"  python main.py\n")
    else:
        print_status("error", "Alguns problemas foram detectados.")
        print(f"\n{YELLOW}Execute:{END}")
        print(f"  pip install -r requirements.txt\n")
    
    print(f"{BLUE}{'='*60}{END}\n")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
