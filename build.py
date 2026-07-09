#!/usr/bin/env python3
"""
Script de build para criar executável com PyInstaller.

Este script gera um executável standalone que não precisa de Python.
"""

import os
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """Constrói o executável com PyInstaller."""
    
    project_root = Path(__file__).parent
    
    print("=" * 70)
    print("  CRIATIVECA PDF BUILDER - GERADOR DE EXECUTÁVEL")
    print("=" * 70)
    print()
    
    # Limpar build anterior
    print("1️⃣  Limpando builds anteriores...")
    for folder in ["build", "dist", "__pycache__", "app/__pycache__"]:
        folder_path = project_root / folder
        if folder_path.exists():
            shutil.rmtree(folder_path)
            print(f"   ✓ Removido: {folder}/")
    
    # Remover arquivo .spec anterior
    spec_file = project_root / "Criativeca_PDF_Builder.spec"
    if spec_file.exists():
        spec_file.unlink()
        print(f"   ✓ Removido: {spec_file.name}")
    
    print()
    print("2️⃣  Gerando executável com PyInstaller...")
    print("   (isto pode levar alguns minutos...)")
    print()
    
    # Comando PyInstaller
    command = [
        "python",
        "-m",
        "PyInstaller",
        "--name=Criativeca_PDF_Builder",
        "--onefile",
        "--windowed",
        "--icon=assets/icon.ico",
        f"--add-data=assets{os.pathsep}assets",
        f"--add-data=input{os.pathsep}input",
        f"--add-data=output{os.pathsep}output",
        "--hidden-import=PIL",
        "--hidden-import=reportlab",
        "--hidden-import=fitz",
        "--hidden-import=natsort",
        "--hidden-import=customtkinter",
        "--clean",
        "--noconfirm",
        "main.py"
    ]
    
    try:
        result = subprocess.run(
            command,
            cwd=str(project_root),
            text=True
        )
        
        if result.returncode != 0:
            print("❌ Erro ao gerar executável:")
            print(result.stderr)
            return False
        
        print(result.stdout)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    print()
    print("3️⃣  Verificando executável gerado...")
    
    exe_path = project_root / "dist" / "Criativeca_PDF_Builder.exe"
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"   ✓ Executável criado com sucesso!")
        print(f"   📦 Tamanho: {size_mb:.2f} MB")
        print(f"   📍 Localização: {exe_path}")
        print()
        
        return True
    else:
        print(f"❌ Executável não foi criado")
        return False

def create_readme():
    """Cria README para o executável."""
    
    readme_content = """# 🎉 CRIATIVECA PDF BUILDER - EXECUTÁVEL

## ✅ Como Usar

### Opção 1: Uso Simples
Basta **duplo clique** no arquivo:
```
Criativeca_PDF_Builder.exe
```

### Opção 2: Criar Atalho (Recomendado)
1. Clique direito no .exe
2. Selecione "Enviar para" → "Área de Trabalho (criar atalho)"
3. Duplo clique no atalho para usar

## 📋 Requisitos
- Windows 7 ou superior
- Não precisa de Python instalado
- ~150 MB de espaço em disco

## 🚀 Como Usar a Aplicação
1. Execute o programa
2. Selecione a pasta com suas imagens
3. Preencha o título e subtítulo
4. Escolha onde salvar o PDF
5. Clique em "GERAR PDF"

## 📊 Formatos Suportados
- PNG
- JPG
- JPEG
- WEBP

## ⚙️ Especificações do PDF
- Formato: A4 (210 x 297 mm)
- Resolução: 300 DPI (pronto para impressão)
- Capa profissional automática
- Rodapé em todas as páginas
- Otimizado automaticamente

## 🆘 Problemas?
Se o antivírus reclama, é normal para executáveis empacotados.
O programa é 100% seguro e open-source.

## 📧 Distribuir
Pode mandar o arquivo `Criativeca_PDF_Builder.exe` para amigos/clientes.
Eles podem usar direto sem instalar nada!
"""
    
    readme_path = Path(__file__).parent / "dist" / "LEIA-ME.txt"
    readme_path.write_text(readme_content, encoding="utf-8")
    print(f"   ✓ README criado: LEIA-ME.txt")

def main():
    """Função principal."""
    
    success = build_executable()
    
    if success:
        print()
        print("=" * 70)
        print("  ✅ EXECUTÁVEL CRIADO COM SUCESSO!")
        print("=" * 70)
        print()
        
        create_readme()
        
        print()
        print("📦 ARQUIVOS GERADOS:")
        print("   dist/")
        print("   ├─ Criativeca_PDF_Builder.exe  (seu programa!)")
        print("   └─ LEIA-ME.txt                 (instruções)")
        print()
        
        print("🚀 PRÓXIMOS PASSOS:")
        print("   1. Execute: dist/Criativeca_PDF_Builder.exe")
        print("   2. Teste a aplicação")
        print("   3. Distribua o .exe para seus amigos")
        print()
        
        print("💡 DICA:")
        print("   Você pode comprimir o .exe com WinRAR ou 7-Zip")
        print("   para reduzir tamanho de distribuição (~50 MB)")
        print()
        
    else:
        print()
        print("=" * 70)
        print("  ❌ ERRO AO GERAR EXECUTÁVEL")
        print("=" * 70)
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
