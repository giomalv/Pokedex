import pokebase as pb
from typing import Tuple, Optional

def get_pokemon_list() -> list:
    """Get a big fucking list of all the pokemon."""
    pokemon_list = pb.APIResourceList("pokemon-species")
    names_list = [pokemon["name"].capitalize() for pokemon in pokemon_list]
    return names_list


def get_single_pokemon(lookup:str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Get the weight, height, and image of a pokemon from the pokebase API."""
    pokemon = pb.pokemon(lookup)
    
    weight = getattr(pokemon, "weight", "Unknown!")
    height = getattr(pokemon, "height", "Unknown!")
    sprite = getattr(getattr(pokemon, "sprites", None), "front_default", "Unknown!")

    
    return weight, height, sprite

if __name__ == "__main__":
    # print(get_single_pokemon("charmander"))
    # all = str(get_them_all())
    

    print(get_pokemon_list())