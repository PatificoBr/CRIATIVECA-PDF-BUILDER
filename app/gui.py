"""
Módulo da interface gráfica.

Responsável por:
- Interface do usuário com CustomTkinter
- Gerenciamento de eventos
- Exibição de progresso e logs
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
from pathlib import Path
from typing import Optional
from datetime import datetime
from natsort import natsorted

from .validator import ImageValidator
from .pdf import PDFBuilder
from .utils import get_asset_path, create_directory, format_duration, get_file_size
import time


class PDFBuilderApp(ctk.CTk):
    """Interface gráfica da aplicação."""
    
    def __init__(self):
        """Inicializa a interface."""
        super().__init__()
        
        # Configurações da janela
        self.title("Criativeca PDF Builder")
        self.geometry("900x800")
        self.resizable(True, True)
        
        # Definir tema e aparencia
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Tentar definir ícone
        icon_path = get_asset_path("icon.ico")
        if icon_path:
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass
        
        # Variáveis da aplicação
        self.input_folder = ""
        self.output_folder = ""
        self.is_processing = False
        self.selected_images = []
        
        # Criar interface
        self._create_ui()
        
        # Centralizar janela
        self._center_window()
    
    def _create_ui(self) -> None:
        """Cria os elementos da interface."""
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="Criativeca PDF Builder",
            font=("Helvetica", 28, "bold"),
            text_color="#00A8FF"
        )
        title_label.pack(pady=(0, 10))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Transforme suas imagens em um PDF profissional",
            font=("Helvetica", 12),
            text_color="#7F8C8D"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Frame de seleção de pastas
        folder_frame = ctk.CTkFrame(main_frame)
        folder_frame.pack(fill="x", pady=10)
        
        # Pasta de entrada
        input_container = ctk.CTkFrame(folder_frame)
        input_container.pack(fill="x", pady=5)
        
        input_label = ctk.CTkLabel(input_container, text="📁 Pasta de Imagens:", font=("Helvetica", 12, "bold"))
        input_label.pack(anchor="w")
        
        input_button_frame = ctk.CTkFrame(input_container)
        input_button_frame.pack(fill="x", pady=5)
        
        self.input_text = ctk.CTkEntry(input_button_frame, placeholder_text="Selecione a pasta com as imagens...")
        self.input_text.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(
            input_button_frame,
            text="Selecionar",
            command=self._select_input_folder,
            width=120
        ).pack(side="left")
        
        # Pasta de saída
        output_container = ctk.CTkFrame(folder_frame)
        output_container.pack(fill="x", pady=5)
        
        output_label = ctk.CTkLabel(output_container, text="💾 Pasta de Saída:", font=("Helvetica", 12, "bold"))
        output_label.pack(anchor="w")
        
        output_button_frame = ctk.CTkFrame(output_container)
        output_button_frame.pack(fill="x", pady=5)
        
        self.output_text = ctk.CTkEntry(output_button_frame, placeholder_text="Selecione onde salvar o PDF...")
        self.output_text.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(
            output_button_frame,
            text="Selecionar",
            command=self._select_output_folder,
            width=120
        ).pack(side="left")
        
        # Frame de texto
        text_frame = ctk.CTkFrame(main_frame)
        text_frame.pack(fill="x", pady=10)
        
        # Título do PDF
        title_container = ctk.CTkFrame(text_frame)
        title_container.pack(fill="x", pady=5)
        
        ctk.CTkLabel(title_container, text="📘 Título:", font=("Helvetica", 12, "bold")).pack(anchor="w")
        self.title_entry = ctk.CTkEntry(title_container, placeholder_text="Digite o título do PDF...")
        self.title_entry.pack(fill="x", pady=5)
        
        # Subtítulo do PDF
        subtitle_container = ctk.CTkFrame(text_frame)
        subtitle_container.pack(fill="x", pady=5)
        
        ctk.CTkLabel(subtitle_container, text="📄 Subtítulo:", font=("Helvetica", 12, "bold")).pack(anchor="w")
        self.subtitle_entry = ctk.CTkEntry(subtitle_container, placeholder_text="Digite o subtítulo do PDF...")
        self.subtitle_entry.pack(fill="x", pady=5)
        
        # Nome do arquivo
        filename_container = ctk.CTkFrame(text_frame)
        filename_container.pack(fill="x", pady=5)
        
        ctk.CTkLabel(filename_container, text="📄 Nome do Arquivo:", font=("Helvetica", 12, "bold")).pack(anchor="w")
        self.filename_entry = ctk.CTkEntry(filename_container, placeholder_text="Nome do arquivo (sem .pdf)...")
        self.filename_entry.pack(fill="x", pady=5)
        
        # Barra de progresso
        progress_label = ctk.CTkLabel(main_frame, text="Progresso:", font=("Helvetica", 11, "bold"))
        progress_label.pack(anchor="w", pady=(15, 5))
        
        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.pack(fill="x", pady=5)
        self.progress_bar.set(0)
        
        self.progress_text = ctk.CTkLabel(main_frame, text="0%", font=("Helvetica", 10))
        self.progress_text.pack(anchor="w")
        
        # Frame de botões (ANTES do log para aparecer na tela)
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=(15, 10))
        
        # Botão gerar PDF (DESTAQUE PRINCIPAL)
        self.generate_button = ctk.CTkButton(
            button_frame,
            text="▶️  COMEÇAR A CONVERTER",
            command=self._generate_pdf,
            width=250,
            height=60,
            font=("Helvetica", 16, "bold"),
            fg_color="#FF6B35",
            hover_color="#D84315",
            text_color="white"
        )
        self.generate_button.pack(side="left", padx=5)
        
        # Botão limpar log
        ctk.CTkButton(
            button_frame,
            text="🗑️  Limpar Log",
            command=self._clear_log,
            width=120,
            font=("Helvetica", 12),
            fg_color="#E74C3C",
            hover_color="#C0392B"
        ).pack(side="right", padx=5)
        
        # Log
        log_label = ctk.CTkLabel(main_frame, text="📋 Log:", font=("Helvetica", 11, "bold"))
        log_label.pack(anchor="w", pady=(10, 5))
        
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(fill="both", expand=True, pady=5)
        
        # Text widget com scrollbar
        self.log_text = ctk.CTkTextbox(log_frame, height=100, state="disabled")
        self.log_text.pack(fill="both", expand=True)
        
        # Log inicial
        self._log("Bem-vindo ao Criativeca PDF Builder!")
        self._log("Selecione as pastas e preencha os campos para começar.")
    
    def _select_input_folder(self) -> None:
        """Seleciona a pasta de entrada."""
        folder = filedialog.askdirectory(title="Selecione a pasta com as imagens")
        
        if folder:
            self.input_folder = folder
            self.input_text.delete(0, "end")
            self.input_text.insert(0, folder)
            
            # Validar e listar imagens
            valid_images, errors = ImageValidator.get_valid_images(folder)
            
            if valid_images:
                # Ordenar naturalmente
                self.selected_images = natsorted(valid_images)
                self._log(f"✓ {len(self.selected_images)} imagem(ns) encontrada(s)")
                
                if errors:
                    for error in errors:
                        self._log(f"  {error}")
            else:
                self._log("✗ Nenhuma imagem válida encontrada")
                
                if errors:
                    for error in errors:
                        self._log(f"  {error}")
    
    def _select_output_folder(self) -> None:
        """Seleciona a pasta de saída."""
        folder = filedialog.askdirectory(title="Selecione a pasta de saída")
        
        if folder:
            self.output_folder = folder
            self.output_text.delete(0, "end")
            self.output_text.insert(0, folder)
            self._log(f"✓ Pasta de saída: {folder}")
    
    def _validate_inputs(self) -> tuple[bool, str]:
        """
        Valida todas as entradas.
        
        Returns:
            Tupla (válido: bool, mensagem_erro: str)
        """
        # Validar pasta de entrada
        valid, msg = ImageValidator.validate_folder(self.input_folder)
        if not valid:
            return False, f"Pasta de entrada: {msg}"
        
        # Validar imagens
        if not self.selected_images:
            return False, "Nenhuma imagem válida para processar"
        
        # Validar pasta de saída
        valid, msg = ImageValidator.validate_output_folder(self.output_folder)
        if not valid:
            return False, f"Pasta de saída: {msg}"
        
        # Validar título
        valid, msg = ImageValidator.validate_text_field(
            self.title_entry.get(),
            "Título",
            100
        )
        if not valid:
            return False, msg
        
        # Validar subtítulo
        valid, msg = ImageValidator.validate_text_field(
            self.subtitle_entry.get(),
            "Subtítulo",
            200
        )
        if not valid:
            return False, msg
        
        # Validar nome do arquivo
        valid, msg = ImageValidator.validate_pdf_name(self.filename_entry.get())
        if not valid:
            return False, msg
        
        return True, "Validação OK"
    
    def _generate_pdf(self) -> None:
        """Gera o PDF em uma thread separada."""
        if self.is_processing:
            messagebox.showwarning("Aviso", "Já existe uma geração em andamento")
            return
        
        # Validar entradas
        valid, msg = self._validate_inputs()
        if not valid:
            messagebox.showerror("Erro de validação", msg)
            self._log(f"✗ Erro: {msg}")
            return
        
        # Desabilitar botão
        self.is_processing = True
        self.generate_button.configure(state="disabled", text="⏳ Gerando...")
        
        # Executar em thread
        thread = threading.Thread(target=self._generate_pdf_thread)
        thread.daemon = True
        thread.start()
    
    def _generate_pdf_thread(self) -> None:
        """Thread para gerar PDF."""
        try:
            start_time = time.time()
            
            self._log("\n" + "="*50)
            self._log(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando geração...")
            self._log("="*50)
            
            # Preparar caminho do PDF
            pdf_name = self.filename_entry.get().strip()
            if not pdf_name.lower().endswith('.pdf'):
                pdf_name += '.pdf'
            
            output_path = os.path.join(self.output_folder, pdf_name)
            
            # Verificar se arquivo já existe
            if os.path.exists(output_path):
                self._log(f"⚠ Arquivo já existe. Sobrescrevendo: {pdf_name}")
            
            # Criar builder
            builder = PDFBuilder(progress_callback=self._update_progress)
            
            # Obter logo
            logo_path = get_asset_path("logo.png")
            
            # Gerar PDF
            success, message = builder.build(
                self.selected_images,
                output_path,
                self.title_entry.get(),
                self.subtitle_entry.get(),
                logo_path
            )
            
            # Calcular tempo
            elapsed_time = time.time() - start_time
            
            if success:
                file_size = get_file_size(output_path)
                self._log(f"✓ {message}")
                self._log(f"✓ Tamanho: {file_size}")
                self._log(f"✓ Tempo: {format_duration(elapsed_time)}")
                self._log(f"✓ Arquivo: {output_path}")
                self._log("="*50)
                self._log("PDF gerado com sucesso!")
                
                # Mensagem de sucesso
                messagebox.showinfo(
                    "Sucesso",
                    f"PDF gerado com sucesso!\n\n{output_path}\n\nTamanho: {file_size}"
                )
            else:
                self._log(f"✗ Erro: {message}")
                self._log("="*50)
                messagebox.showerror("Erro", message)
        
        except Exception as e:
            self._log(f"✗ Erro inesperado: {str(e)}")
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
        
        finally:
            # Reabilitar botão
            self.is_processing = False
            self.generate_button.configure(state="normal", text="🚀 GERAR PDF")
    
    def _update_progress(self, progress: int) -> None:
        """
        Atualiza a barra de progresso.
        
        Args:
            progress: Percentual de progresso (0-100)
        """
        self.progress_bar.set(progress / 100)
        self.progress_text.configure(text=f"{progress}%")
        self.update()
    
    def _log(self, message: str) -> None:
        """
        Adiciona mensagem ao log.
        
        Args:
            message: Mensagem a adicionar
        """
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
        self.update()
    
    def _clear_log(self) -> None:
        """Limpa o log."""
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
    
    def _center_window(self) -> None:
        """Centraliza a janela na tela."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


def main():
    """Função principal para executar a aplicação."""
    app = PDFBuilderApp()
    app.mainloop()


if __name__ == "__main__":
    main()