# Importy pro azure
import logging
import azure.functions as func
 
# Importy pro práci s obrázkem
from PIL import Image
from io import BytesIO
import base64
 
 
# Nastavení konstant
new_width = 180
chars = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]
 
def main(req: func.HttpRequest) -> func.HttpResponse:
    # Logni start funkce
    logging.info('Python HTTP endpoint triggered.')
 
    # Získej parametr obrazek. 
    # Pokus se vzít z těla requestu.
    obrazek = {}
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        obrazek = req_body.get('obrazek')
     
    # Pokud ani po kontrolach neni obrazek nadefinovan, pošli zpět 422
    if not obrazek:
        return func.HttpResponse(
            "Prosím, zadejte base64 'obrazek' argument",
            status_code=422
        )
 
    # Získej obrázek z base64 formátu
    img = Image.open(BytesIO(base64.b64decode(obrazek)))
 
    # Změň šířku a výšku obrázku
    width, height = img.size
    aspect_ratio = height/width
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))
 
    # Přehoď obrázek na černobílý
    img = img.convert('L')
     
    # Získej pixely z obrázku
    pixels = img.getdata()
 
    # Nahraď každý pixel s chrakterem z pole
    new_pixels = [chars[pixel//25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)
 
    # Vytvoř ASCII art
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)
 
    # Logni finální obrázek
    logging.info(ascii_image)
 
    # Pošli zpět ASCII art
    return func.HttpResponse(
        ascii_image,
        status_code=200
    )