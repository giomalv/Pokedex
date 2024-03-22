import pokebase as pb
from rich_pixels import Pixels

from typing import Tuple, Optional
import os
import json
import image_loader
import pickle as gherkin

def serialise_image_data(data:Pixels,pokemon:str):
    filename = f"pokecache/{pokemon}.pokeimg"
    with open(filename, "wb") as file:
        gherkin.dump(data,file)

def get_pokemon_list() -> list:
    """Get a big fucking list of all the pokemon."""
    pokemon_list = pb.APIResourceList("pokemon-species")
    names_list = [pokemon["name"].capitalize() for pokemon in pokemon_list]
    return names_list


def get_single_pokemon(lookup:str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Get the weight, height, and image of a pokemon from the pokebase API."""

    lookup = lookup.lower()
    cache_file = f"pokecache/{lookup}.json"

    if os.path.exists(cache_file):
        with open(cache_file, "r") as file:
            data = json.load(file)
            height = data.get("height","Unknown!")
            weight = data.get("weight","Unknown!")
            sprite_url = data.get("sprite_url", "Unknown!")
            sprite_path = data.get("sprite_path", "Unknown!")

    else:
        pokemon = pb.pokemon(lookup)
        height = getattr(pokemon, "height", "Unknown!")
        weight = getattr(pokemon, "weight", "Unknown!")
        sprite_url = getattr(getattr(pokemon, "sprites", None), "front_default", "Unknown!")
        sprite_data = image_loader.load_from_url(sprite_url)
        serialise_image_data(sprite_data,lookup)
        sprite_path = f"pokecache/{lookup}.pokeimg"
        
        data = {"weight":weight,"height":height,"sprite_url":sprite_url, "sprite_path":sprite_path}

        with open(cache_file,"w") as file:
            json.dump(data,file)

    return height, weight, sprite_url, sprite_path

def cache_them_all():
    list = get_pokemon_list()
    for pokemon in list:
        get_single_pokemon(pokemon)

if __name__ == "__main__":
    print(get_single_pokemon("Pidgey"))
    # all = str(get_them_all())
    # print(get_pokemon_list())