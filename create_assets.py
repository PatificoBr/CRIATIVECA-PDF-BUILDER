#!/usr/bin/env python3
"""
Script para gerar assets do projeto.
Cria logo.png e icon.ico na pasta assets/
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Criar pasta assets se não existir
assets_dir = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(assets_dir, exist_ok=True)

# ============================================================
# Criar logo.png
# ============================================================
print("Gerando logo.png...")

logo_size = (400, 400)
logo = Image.new('RGBA', logo_size, (0, 0, 0, 0))
draw = ImageDraw.Draw(logo)

# Cores
accent_color = "#2C3E50"
accent_rgb = (44, 62, 80)
light_color = "#00A8FF"
light_rgb = (0, 168, 255)

# Desenhar círculo de fundo
circle_size = 350
circle_pos = (25, 25)
draw.ellipse(
    [(circle_pos[0], circle_pos[1]), 
     (circle_pos[0] + circle_size, circle_pos[1] + circle_size)],
    fill=light_rgb,
    outline=accent_rgb,
    width=3
)

# Desenhar gradiente simples (rectângulo no topo do círculo para efeito)
for y in range(100):
    alpha = int(100 * (1 - y / 100))
    overlay = Image.new('RGBA', logo_size, (255, 255, 255, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.line(
        [(0, circle_pos[1] + y), (logo_size[0], circle_pos[1] + y)],
        fill=(255, 255, 255, alpha // 3),
        width=1
    )
    logo.paste(Image.alpha_composite(logo, overlay))

# Adicionar texto "C"
try:
    # Tentar usar fonte padrão do sistema
    font_size = 200
    font = ImageFont.truetype("arial.ttf", font_size)
except Exception:
    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 200)
    except Exception:
        # Usar fonte padrão se não encontrar
        font = ImageFont.load_default()

draw = ImageDraw.Draw(logo)
text = "C"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
text_x = (logo_size[0] - text_width) // 2
text_y = (logo_size[1] - text_height) // 2 - 20

draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)

# Salvar logo
logo_path = os.path.join(assets_dir, "logo.png")
logo.save(logo_path, "PNG")
print(f"✓ Logo criado: {logo_path}")

# ============================================================
# Criar icon.ico
# ============================================================
print("Gerando icon.ico...")

# Criar imagem de ícone
icon_size = (256, 256)
icon = Image.new('RGB', icon_size, (44, 62, 80))
draw = ImageDraw.Draw(icon)

# Desenhar quadrado com "C"
draw.rectangle(
    [(20, 20), (236, 236)],
    outline=(0, 168, 255),
    width=5
)

# Adicionar "C"
try:
    font = ImageFont.truetype("arial.ttf", 150)
except Exception:
    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 150)
    except Exception:
        font = ImageFont.load_default()

draw = ImageDraw.Draw(icon)
bbox = draw.textbbox((0, 0), "C", font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
text_x = (icon_size[0] - text_width) // 2
text_y = (icon_size[1] - text_height) // 2 - 20

draw.text((text_x, text_y), "C", fill=(0, 168, 255), font=font)

# Salvar ícone
icon_path = os.path.join(assets_dir, "icon.ico")
icon.save(icon_path, "ICO")
print(f"✓ Ícone criado: {icon_path}")

print("\n✓ Assets gerados com sucesso!")
