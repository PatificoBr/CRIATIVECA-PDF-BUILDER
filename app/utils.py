"""
Módulo de utilitários gerais.

Funções auxiliares para:
- Conversão de unidades
- Processamento de caminhos
- Validação de recursos
"""

import os
from pathlib import Path
from typing import Tuple, Optional


def mm_to_points(mm: float) -> float:
    """
    Converte milímetros para pontos (1 ponto = 1/72 polegada).
    
    Args:
        mm: Valor em milímetros
        
    Returns:
        Valor em pontos
    """
    return mm * 2.834645669


def pixels_to_mm(pixels: int, dpi: int = 72) -> float:
    """
    Converte pixels para milímetros.
    
    Args:
        pixels: Número de pixels
        dpi: Pontos por polegada (padrão 72)
        
    Returns:
        Valor em milímetros
    """
    return (pixels / dpi) * 25.4


def get_asset_path(asset_name: str) -> Optional[str]:
    """
    Retorna o caminho completo para um arquivo de asset.
    
    Args:
        asset_name: Nome do arquivo (ex: 'logo.png')
        
    Returns:
        Caminho completo do asset ou None se não encontrado
    """
    # Tenta encontrar o asset na pasta assets
    assets_dir = Path(__file__).parent.parent / "assets"
    asset_path = assets_dir / asset_name
    
    if asset_path.exists():
        return str(asset_path)
    
    return None


def create_directory(directory_path: str) -> bool:
    """
    Cria um diretório se não existir.
    
    Args:
        directory_path: Caminho do diretório
        
    Returns:
        True se criado/existe com sucesso, False caso contrário
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        print(f"Erro ao criar diretório: {e}")
        return False


def get_file_size(filepath: str) -> str:
    """
    Retorna o tamanho do arquivo em formato legível.
    
    Args:
        filepath: Caminho do arquivo
        
    Returns:
        Tamanho formatado (ex: '2.5 MB')
    """
    try:
        size_bytes = os.path.getsize(filepath)
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        
        return f"{size_bytes:.2f} TB"
    except Exception:
        return "0 B"


def safe_filename(filename: str) -> str:
    """
    Remove caracteres inválidos do nome do arquivo.
    
    Args:
        filename: Nome original
        
    Returns:
        Nome seguro para uso como arquivo
    """
    invalid_chars = '<>:"|?*\\\\'
    safe_name = filename
    
    for char in invalid_chars:
        safe_name = safe_name.replace(char, '_')
    
    return safe_name.strip()


def get_relative_path(full_path: str, base_path: str) -> str:
    """
    Retorna o caminho relativo entre dois caminhos.
    
    Args:
        full_path: Caminho completo
        base_path: Caminho base
        
    Returns:
        Caminho relativo
    """
    try:
        return os.path.relpath(full_path, base_path)
    except ValueError:
        return full_path


def format_duration(seconds: float) -> str:
    """
    Formata duração em tempo legível.
    
    Args:
        seconds: Tempo em segundos
        
    Returns:
        Tempo formatado (ex: '1m 30s')
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    
    return f"{minutes}m {secs}s"


def is_asset_available(asset_name: str) -> bool:
    """
    Verifica se um asset está disponível.
    
    Args:
        asset_name: Nome do asset
        
    Returns:
        True se existe, False caso contrário
    """
    return get_asset_path(asset_name) is not None