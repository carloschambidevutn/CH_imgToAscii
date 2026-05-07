import argparse
import shutil  # Para detectar el tamaño de la terminal
from pathlib import Path
from typing import Any, List
from PIL import Image, ImageOps, ImageEnhance

# Paleta profesional con raw string (r"") para evitar errores de escape
ASCII_CHARS = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def optimizar_imagen(img: Image.Image) -> Image.Image:
    img = img.convert("L")
    img = ImageEnhance.Contrast(img).enhance(1.5)
    img = ImageEnhance.Sharpness(img).enhance(2.0)
    img = ImageOps.autocontrast(img)
    return img

def redimensionar(img: Image.Image, nuevo_ancho: int) -> Image.Image:
    w_orig, h_orig = img.size
    ratio = h_orig / w_orig
    nuevo_alto = int(nuevo_ancho * ratio * 0.5)
    return img.resize((nuevo_ancho, nuevo_alto), resample=1)

def encontrar_archivo(nombre: str) -> str:
    ruta = Path(nombre)
    if ruta.is_file():
        return str(ruta)
    
    # Carpetas de búsqueda en Arch/KDE
    carpetas = [Path.home() / "Pictures", Path.home() / "Downloads", Path.home() / "Imágenes", Path.home() / "Descargas"]
    
    for carpeta in carpetas:
        if carpeta.exists():
            busqueda = list(carpeta.rglob(nombre))
            if busqueda:
                return str(busqueda[0])
    return nombre

def imagen_a_ascii(ruta: str, ancho: int) -> str:
    try:
        with Image.open(ruta) as img:
            img = optimizar_imagen(img)
            img = redimensionar(img, ancho)
            
            datos: Any = img.getdata()
            pixeles: List[int] = list(datos)
            
            rango = len(ASCII_CHARS) - 1
            # Mapeo optimizado
            ascii_lista = [ASCII_CHARS[rango - (p * rango // 255)] for p in pixeles]
            
            return "\n".join("".join(ascii_lista[i:i+ancho]) for i in range(0, len(ascii_lista), ancho))
    except Exception as e:
        return f"Error: No se pudo procesar la imagen. {e}"

def main():
    # Detectar ancho de la terminal automáticamente
    ancho_terminal, _ = shutil.get_terminal_size()
    
    parser = argparse.ArgumentParser(description="ASCII Art Studio Pro")
    parser.add_argument("ruta", help="Nombre o ruta de la imagen")
    parser.add_argument("-w", "--width", type=int, default=ancho_terminal, help="Ancho del arte")
    parser.add_argument("-o", "--output", help="Archivo de salida")
    args = parser.parse_args()

    ruta_final = encontrar_archivo(args.ruta)
    print(f"--- Procesando: {ruta_final} ---")
    
    resultado = imagen_a_ascii(ruta_final, args.width)

    if args.output:
        Path(args.output).write_text(resultado, encoding="utf-8")
        print(f"Guardado con éxito en: {args.output}")
    else:
        print(resultado)

if __name__ == "__main__":
    main()
