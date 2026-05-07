from PIL import Image, ImageDraw, ImageFont
import sys

def text_to_image(text, output_path):
    # Use a monospace font
    try:
        font = ImageFont.truetype("consola.ttf", 16) # Windows Consolas
    except:
        try:
            font = ImageFont.truetype("DejaVuSansMono.ttf", 16)
        except:
            font = ImageFont.load_default()

    lines = text.splitlines()
    
    # Calculate image size
    line_height = font.getbbox("A")[3] + 4
    max_width = max([font.getbbox(line)[2] for line in lines]) + 40
    height = line_height * len(lines) + 40
    
    # Create image
    img = Image.new('RGB', (max_width, height), color=(30, 30, 30))
    d = ImageDraw.Draw(img)
    
    y = 20
    for line in lines:
        d.text((20, y), line, font=font, fill=(240, 240, 240))
        y += line_height
        
    img.save(output_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_screenshot.py <output_path> <text>")
        sys.exit(1)
    
    output_path = sys.argv[1]
    text = sys.stdin.read()
    text_to_image(text, output_path)
