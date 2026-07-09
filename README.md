# Criativeca PDF Builder

Uma ferramenta para transformar pastas de imagens em PDFs para impressão.

## 🎯 Características

- **Interface moderna** com CustomTkinter (tema escuro)
- **Suporte a múltiplos formatos**: PNG, JPG, JPEG, WEBP
- **Geração automática de capa** com logo e título
- **Rodapé** em todas as páginas
- **Validação completa** de imagens
- **Ordenação natural** dos arquivos (001, 002, 003...)
- **Otimização automática** do PDF
- **Barra de progresso** em tempo real
- **Log detalhado** das operações

## 📋 Requisitos

- Python 3.13+
- pip (gerenciador de pacotes)

## 🚀 Instalação

1. Clone ou baixe o projeto
2. Navegue até a pasta do projeto
3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## 💻 Uso

1. Execute o programa:

```bash
python main.py
```

2. Na interface:
   - Selecione a pasta contendo as imagens
   - Escolha a pasta de saída
   - Preenchch título e subtítulo
   - Digite o nome do PDF
   - Clique em "GERAR PDF"

## 📁 Estrutura do Projeto

```
Criativeca PDF Builder/
├── main.py              # Ponto de entrada
├── requirements.txt     # Dependências
├── README.md           # Documentação
├── assets/
│   ├── logo.png        # Logo da capa
│   └── icon.ico        # Ícone da aplicação
├── input/              # Pasta de imagens (padrão)
├── output/             # Pasta de saída (padrão)
└── app/
    ├── __init__.py
    ├── gui.py          # Interface gráfica
    ├── pdf.py          # Geração do PDF
    ├── cover.py        # Capa do PDF
    ├── footer.py       # Rodapé do PDF
    ├── validator.py    # Validação de imagens
    └── utils.py        # Funções auxiliares
```

## 🎨 Configuração da Capa

A capa é gerada automaticamente com:
- Logo (assets/logo.png)
- Título (customizável)
- Subtítulo (customizável)

## 📄 Especificações do PDF

- **Formato**: A4 (210 x 297 mm)
- **Resolução**: 300 DPI
- **Compressão**: Otimizada automaticamente
- **Margens**: 10 mm (impressão doméstica)
- **Uma imagem por página**

## ⚙️ Detalhes Técnicos

### Validação
- Verifica imagens corrompidas
- Valida formatos suportados
- Detecta pastas vazias
- Reporta erros na interface

### Ordenação
- Utiliza natsort para ordenação natural
- Suporta nomes com números: 001, 002, 010, etc.

### Performance
- Processa imagens em lotes
- Otimiza PDF após geração
- Mostra progresso em tempo real

## 🔧 Dependências

| Biblioteca | Versão | Função |
|-----------|--------|--------|
| customtkinter | 5.2.2 | Interface gráfica moderna |
| pillow | 10.2.0 | Manipulação de imagens |
| reportlab | 4.0.9 | Geração de PDF |
| pymupdf | 1.24.2 | Otimização de PDF |
| natsort | 8.4.0 | Ordenação natural |

## 📝 Licença

Desenvolvido por PatificoBr
GitHub: https://github.com/PatificoBr

## 🤝 Suporte

Para reportar problemas ou sugestões, abra uma issue no repositório.