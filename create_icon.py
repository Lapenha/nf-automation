"""
Script para criar ícone do aplicativo Validador NF-e
Gera um ícone .ico com várias resoluções
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Cria ícone do aplicativo."""
    
    # Tamanho base
    size = 256
    
    # Cria imagem com fundo transparente
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Gradiente azul (círculo)
    colors = [
        (0, 123, 255),   # Azul claro
        (0, 86, 179),    # Azul escuro
    ]
    
    # Desenha círculo com gradiente simulado
    for i in range(10, 0, -1):
        alpha = int(255 * (i / 10))
        color = colors[0] + (alpha,)
        margin = (10 - i) * 2
        draw.ellipse(
            [margin, margin, size - margin, size - margin],
            fill=color,
            outline=None
        )
    
    # Círculo principal
    margin = 15
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill='#007bff',
        outline='#0056b3',
        width=6
    )
    
    # Desenha documento estilizado
    doc_color = 'white'
    
    # Retângulo do documento
    doc_left = size // 3
    doc_top = size // 4
    doc_right = size - doc_left
    doc_bottom = size - doc_top
    
    draw.rounded_rectangle(
        [doc_left, doc_top, doc_right, doc_bottom],
        radius=10,
        fill=doc_color,
        outline='#e9ecef',
        width=2
    )
    
    # Linhas no documento (representando texto)
    line_color = '#007bff'
    line_spacing = 16
    line_left = doc_left + 15
    line_right = doc_right - 15
    line_top = doc_top + 20
    
    for i in range(5):
        y = line_top + (i * line_spacing)
        if y < doc_bottom - 20:
            width = 3 if i == 0 else 2  # Primeira linha mais grossa
            draw.line(
                [(line_left, y), (line_right if i % 2 == 0 else line_right - 20, y)],
                fill=line_color,
                width=width
            )
    
    # Checkmark (símbolo de validação)
    check_color = '#28a745'
    check_size = 35
    check_x = size - 65
    check_y = size - 65
    
    # Círculo do checkmark
    draw.ellipse(
        [check_x, check_y, check_x + check_size, check_y + check_size],
        fill=check_color,
        outline='#1e7e34',
        width=2
    )
    
    # Desenha o ✓
    check_points = [
        (check_x + 8, check_y + check_size // 2),
        (check_x + check_size // 2 - 2, check_y + check_size - 10),
        (check_x + check_size - 6, check_y + 8)
    ]
    draw.line(check_points, fill='white', width=4, joint='curve')
    
    # Salva em múltiplas resoluções
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save('icon.ico', format='ICO', sizes=sizes)
    
    print("✅ Ícone criado com sucesso: icon.ico")
    print(f"📏 Resoluções: {', '.join([f'{w}x{h}' for w, h in sizes])}")
    
    # Também salva como PNG para referência
    img.save('icon.png', format='PNG')
    print("✅ Preview salvo: icon.png")


if __name__ == "__main__":
    try:
        create_icon()
    except ImportError:
        print("❌ Erro: Pillow não está instalado")
        print("📦 Instale com: pip install Pillow")
    except Exception as e:
        print(f"❌ Erro ao criar ícone: {e}")
