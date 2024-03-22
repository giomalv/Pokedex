
from textual.app import App, ComposeResult
from textual.widgets import Footer, OptionList, Label, Static, Button, Input, DataTable
from textual.containers import Grid, ScrollableContainer
from textual.reactive import Reactive
from textual.screen import ModalScreen
from textual import on
from pokedata import get_single_pokemon, get_pokemon_list, cache_them_all

import pickle as gherkin
import random

##DEBUG List, for use before we implement grabbing data via PokeAPI
DEBUG_POKEMON_LIST = ["Urshifu", "Pikachu","Charmander","Bulbasaur","Squirtle","Jigglypuff","Meowth","Psyduck","Mewtwo","Mew","Gengar","Gyarados","Lapras","Eevee","Vaporeon","Jolteon","Flareon","Espeon","Umbreon","Leafeon","Glaceon","Sylveon","Grimmsnarl","Toxtricity","Corviknight","Cinderace","Inteleon","Rillaboom","Zacian","Zamazenta","Eternatus","Urshifu","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex"]

INITIAL_POKEMON_LIST = get_pokemon_list()



class PokePortraitWidget(Static):
    image_path: Reactive[str] = Reactive("")

    # Displays image of pokemon we grab from the API
    def compose(self) -> ComposeResult:
        yield Label(id="pokemon-portrait-url")
        yield Label("",id="pokemon-portrait")

        
    def load_pixels(self,path):
        with open(self.image_path,"rb") as file:
            pixels = gherkin.load(file)
            return pixels
    
    def watch_image_path(self) -> None:
        pixels = self.load_pixels(self.image_path)
        self.query_one("#pokemon-portrait",Label).update(pixels)

class PokemonList(Static):
    search_query: Reactive[str] = Reactive("")

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search", id="search")
        yield OptionList(*INITIAL_POKEMON_LIST, id="pokemon-option-select")

    def update_pokemon_list(self,query:str):
         appyWappy.pokemon_list = list(filter(lambda pokemon: self.search_query.lower() in pokemon.lower(), INITIAL_POKEMON_LIST))
    
    def watch_search_query(self, query:str) -> None:
        self.query_one("#pokemon-option-select", OptionList).clear_options()
        self.update_pokemon_list(query)
        self.query_one("#pokemon-option-select", OptionList).add_options(appyWappy.pokemon_list)
        print(self.search_query)

class CachePrompt(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Creating a full Pokémon cache will take a long time.\n\nAre you sure?", id="question"),
            Button("Yes", variant="warning", id="yes"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog"
        )

    def on_button_pressed(self, event:Button.Pressed):
        if event.button.id == "yes":
            cache_them_all()
        else:
            self.app.pop_screen()

class MainContainer(ScrollableContainer):
    selected_pokemon: Reactive[str] = Reactive("")

    def __init__(self) -> None:
        self.pokeportrait_widget = PokePortraitWidget()
        super().__init__()
    
    def compose(self) -> ComposeResult:
        yield Label("Welcome to Pykedex!", id="test-label")
        yield Label("Select a Pokemon from the list to view its details.\n", id="instruction-label")

        yield Label(f"Selected Pokemon:{self.selected_pokemon}", id="selected-pokemon-label")
        yield self.pokeportrait_widget
    
    def watch_selected_pokemon(self, selected:str):
        self.query_one("#selected-pokemon-label", Label).update(f"Selected Pokemon: {selected}")
        height,weight,image_url,pokeimg_path = get_single_pokemon(selected.lower())
        self.pokeportrait_widget.query_one("#pokemon-portrait-url", Label).update(f"Image URL: {image_url}")
        self.pokeportrait_widget.image_path = pokeimg_path
              
class PykedexApp(App):
    BINDINGS = [("q","quit","Quit"),
                ("r","random_selection", "Random Pokémon"),
                ("m","make_cache", "Cache All Pokémon")]

    CSS_PATH = "styles/poke.tcss"

    pokemon_list = INITIAL_POKEMON_LIST

    def __init__(self) -> None:
        self.main_container = MainContainer()
        super().__init__()
    
    def compose(self) -> ComposeResult:
        yield Footer()
        yield PokemonList(id="pokemon-list")

        yield self.main_container
    
    @on(OptionList.OptionSelected, "#pokemon-option-select")
    def handle_selection_change(self, event:OptionList.OptionSelected) -> None:
        # print(POKEMON_LIST[event.option_index])
        #Update the selected pokemon in the main container. IT uses a reactive variable so it should update automatically
        self.main_container.selected_pokemon = appyWappy.pokemon_list[event.option_index]
        # self.main_container.query_one("#selected-pokemon-label", Label).update(POKEMON_LIST[event.option_index])

    @on(Input.Changed, "#search")
    def handle_search_change(self,event:Input.Changed)-> None:
        self.query_one("#pokemon-list",PokemonList).search_query = event.value


    def action_random_selection(self) -> None:
        random_pokemon = random.choice(appyWappy.pokemon_list)
        while random_pokemon == self.main_container.selected_pokemon:
            random_pokemon = random.choice(appyWappy.pokemon_list)
            
        self.main_container.selected_pokemon = random_pokemon
        
    def action_make_cache(self) -> None:
        self.push_screen(CachePrompt())



appyWappy = PykedexApp()
appyWappy.run()