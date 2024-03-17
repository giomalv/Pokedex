
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Header, Footer, OptionList, Label, Static
from textual.reactive import Reactive
from textual import events,on
import image_loader
from pokedata import get_single_pokemon, get_pokemon_list

##DEBUG Constants, for use before we implement grabbing data via PokeAPI
DEBUG_POKEMON_LIST = ["Urshifu", "Pikachu","Charmander","Bulbasaur","Squirtle","Jigglypuff","Meowth","Psyduck","Mewtwo","Mew","Gengar","Gyarados","Lapras","Eevee","Vaporeon","Jolteon","Flareon","Espeon","Umbreon","Leafeon","Glaceon","Sylveon","Grimmsnarl","Toxtricity","Corviknight","Cinderace","Inteleon","Rillaboom","Zacian","Zamazenta","Eternatus","Urshifu","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Kubfu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex"]
POKEMON_LIST = get_pokemon_list()

class PokePortraitWidget(Static):
    image_url: Reactive[str] = Reactive("")

    # Displays image of pokemon we grab from the API
    def compose(self) -> ComposeResult:
        yield Label("Pokemon Portrait", id="pokemon-portrait-text")
        yield Label("",id="pokemon-portrait")
        
    def watch_image_url(self,url:str):
            pixels = image_loader.load_from_url(self.image_url,(42,42))
            self.query_one("#pokemon-portrait",Label).update(pixels)

class PokemonList(OptionList):
    pass

class MainContainer(Static):
    selected_pokemon: Reactive[str] = Reactive("")

    def __init__(self) -> None:
        self.pokeportrait_widget = PokePortraitWidget()
        super().__init__()
    
    def compose(self) -> ComposeResult:
        yield Label("Welcome to Pykedex!", id="test-label")
        yield Label("Select a Pokemon from the list to view its details.", id="instruction-label")
        yield Label(f"Selected Pokemon:{self.selected_pokemon}", id="selected-pokemon-label")
        yield self.pokeportrait_widget
    
    def watch_selected_pokemon(self, selected:str):
        self.query_one("#selected-pokemon-label", Label).update(selected)
        weight,height,image = get_single_pokemon(selected.lower())
        self.pokeportrait_widget.query_one("#pokemon-portrait-text", Label).update(image)
        self.pokeportrait_widget.image_url = image
              
class PykedexApp(App):
    BINDINGS = [("v","toggle_dark","Dark Mode Toggle"),
                ("q","quit","Quit")]

    CSS_PATH = "styles/poke.tcss"

    def __init__(self) -> None:
        self.main_container = MainContainer()
        super().__init__()
    
    def compose(self) -> ComposeResult:
        yield Footer()
        yield Header()
        yield PokemonList(*POKEMON_LIST, id="pokemon-list")
        yield self.main_container
    
    @on(OptionList.OptionSelected, "#pokemon-list")
    def handle_selection_change(self, event:OptionList.OptionSelected) -> None:
        print(POKEMON_LIST[event.option_index])
        #Update the selected pokemon in the main container. IT uses a reactive variable so it should update automatically
        self.main_container.selected_pokemon = POKEMON_LIST[event.option_index]
        # self.main_container.query_one("#selected-pokemon-label", Label).update(POKEMON_LIST[event.option_index])


appyWappy = PykedexApp()
appyWappy.run()