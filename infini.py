from kivy.uix.screenmanager import Screen, ScreenManager        # pyright: ignore[reportMissingImports]
from kivy.clock import Clock                                    # pyright: ignore[reportMissingImports]
from set import SetGame

"""TO DO
faire bouton stop et redirection sur menu
"""


class InfiniScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = SetGame()
        self.add_widget(self.game)
        self.game_event = None

    def on_enter(self):
        # Appelée quand on ARRIVE sur cet écran
        self.game.init_game()
        # Lancement du timer d'update
        self.game_event = Clock.schedule_interval(self.game.update, 1.0 / 60.0)

    def on_leave(self):
        # Appelée quand on QUITTE cet écran
        if self.game_event:
            self.game_event.cancel()  # Arrête la boucle du jeu