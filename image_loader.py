from rich_pixels import Pixels
from rich.console import Console
from typing import Optional, Tuple
from PIL import Image

import requests
from io import BytesIO

DEFAULT_DIMENSIONS = (30,30)

def load_from_url(url:str, dimensions: Optional[Tuple[int,int]] = DEFAULT_DIMENSIONS) -> Pixels:
    response = requests.get(url)
    image_data = BytesIO(response.content)

    image = Image.open(image_data)

    if dimensions:
        image  = image.resize(dimensions)
    
    pixels = Pixels.from_image(image)

    image.save("testing.png")
    
    return pixels

if __name__ == "__main__":
    load_from_url("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png")
    #Dimensions test
    # load_from_url("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",(75,75))