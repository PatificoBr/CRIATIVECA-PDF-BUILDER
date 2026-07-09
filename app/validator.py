"""
Módulo de validação de imagens e pastas.

Responsável por verificar:
- Integridade de imagens
- Formatos suportados
- Pastas vazias
- Imagens corrompidas
"""

import os
from pathlib import Path
from typing import List, Tuple
from PIL import Image


SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.webp'}


class ImageValidator:
    """Validador de imagens e pastas."""
    
    @staticmethod
    def validate_folder(folder_path: str) -> Tuple[bool, str]:
        """
        Valida se a pasta existe e contém imagens válidas.
        
        Args:
            folder_path: Caminho da pasta
            
        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        if not folder_path or not folder_path.strip():
            return False, "Pasta não selecionada"
        
        if not os.path.exists(folder_path):
            return False, "Pasta não existe"
        
        if not os.path.isdir(folder_path):
            return False, "Caminho não é uma pasta"
        
        if not os.access(folder_path, os.R_OK):
            return False, "Sem permissão de leitura na pasta"
        
        return True, "Pasta válida"
    
    @staticmethod
    def get_valid_images(folder_path: str) -> Tuple[List[str], List[str]]:
        """
        Retorna lista de imagens válidas e erros encontrados.
        
        Args:
            folder_path: Caminho da pasta com imagens
            
        Returns:
            Tupla (imagens_validas, mensagens_erro)
        """
        valid_images = []
        errors = []
        
        try:
            files = sorted([
                f for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f))
            ])
            
            if not files:
                return [], ["Nenhum arquivo encontrado na pasta"]
            
            image_files = [
                f for f in files
                if Path(f).suffix.lower() in SUPPORTED_FORMATS
            ]
            
            if not image_files:
                return [], ["Nenhuma imagem suportada encontrada (PNG, JPG, JPEG, WEBP)"]
            
            # Validar cada imagem
            for filename in image_files:
                filepath = os.path.join(folder_path, filename)
                
                try:
                    with Image.open(filepath) as img:
                        # Tenta carregar a imagem para verificar integridade
                        img.load()
                        
                        # Verifica se tem dimensões válidas
                        if img.size[0] > 0 and img.size[1] > 0:
                            valid_images.append(filepath)
                        else:
                            errors.append(f"⚠ {filename}: Dimensões inválidas")
                
                except Exception as e:
                    errors.append(f"⚠ {filename}: Imagem corrompida ou inválida")
            
            if not valid_images:
                return [], ["Nenhuma imagem válida encontrada"]
            
            return valid_images, errors
        
        except Exception as e:
            return [], [f"Erro ao verificar pasta: {str(e)}"]
    
    @staticmethod
    def validate_output_folder(folder_path: str) -> Tuple[bool, str]:
        """
        Valida se a pasta de saída é válida.
        
        Args:
            folder_path: Caminho da pasta de saída
            
        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        if not folder_path or not folder_path.strip():
            return False, "Pasta de saída não selecionada"
        
        # Criar pasta se não existir
        try:
            os.makedirs(folder_path, exist_ok=True)
            
            if not os.access(folder_path, os.W_OK):
                return False, "Sem permissão de escrita na pasta de saída"
            
            return True, "Pasta de saída válida"
        
        except Exception as e:
            return False, f"Erro ao acessar pasta de saída: {str(e)}"
    
    @staticmethod
    def validate_pdf_name(pdf_name: str) -> Tuple[bool, str]:
        """
        Valida o nome do arquivo PDF.
        
        Args:
            pdf_name: Nome do PDF (sem extensão)
            
        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        if not pdf_name or not pdf_name.strip():
            return False, "Nome do PDF não preenchido"
        
        # Caracteres inválidos para nomes de arquivo
        invalid_chars = '<>:"|?*\\'
        
        if any(char in pdf_name for char in invalid_chars):
            return False, f"Nome contém caracteres inválidos: {invalid_chars}"
        
        if len(pdf_name) > 100:
            return False, "Nome do PDF muito longo (máximo 100 caracteres)"
        
        return True, "Nome do PDF válido"
    
    @staticmethod
    def validate_text_field(text: str, field_name: str, max_length: int = 200) -> Tuple[bool, str]:
        """
        Valida campos de texto como título e subtítulo.
        
        Args:
            text: Texto a validar
            field_name: Nome do campo (para mensagem)
            max_length: Comprimento máximo permitido
            
        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        if not text or not text.strip():
            return False, f"{field_name} vazio"
        
        if len(text) > max_length:
            return False, f"{field_name} muito longo (máximo {max_length} caracteres)"
        
        return True, f"{field_name} válido"