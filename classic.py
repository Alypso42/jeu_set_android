from kivy.uix.screenmanager import Screen                       # pyright: ignore[reportMissingImports]
from kivy.clock import Clock                                    # pyright: ignore[reportMissingImports]
from kivy.properties import NumericProperty                     # pyright: ignore[reportMissingImports]
from kivy.uix.boxlayout import BoxLayout                # pyright: ignore[reportMissingImports]
from kivy.uix.button import Button                      # pyright: ignore[reportMissingImports]
from kivy.uix.label import Label                        # pyright: ignore[reportMissingImports]
from set import SetGame

# reste a coder l'arret au bout de 1min 
class ClassicSet(SetGame):
    timer = NumericProperty(0.0)
    score = NumericProperty(0)
    def update(self,dt):
        self.timer += dt
        if len(self.selection) == 3 :
            c1, c2, c3 = self.selection[0], self.selection[1], self.selection[2]
            if self.is_set(c1,c2,c3) :
                self.score += 1
                self.reset_game()
            else :
                self.selection.clear()
        #fin jeu 
        if self.timer >= 60.0:
            # bouton continue ou redirection vers la page acceuil
            print ("fin")
            self.timer = 0
            self.clear_widgets()
            layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

            text = Label(text=f'Fin du jeu\nScore : {self.score}',
                        font_size=32,
                        bold=True,  # Texte en gras
                        size_hint=(1, 0.2),)
            layout.add_widget(text)

            btn_continuer = Button(
                text='continuer', size_hint=(1, 0.3), font_size=24
            )
            btn_continuer.bind(on_release=self.parent.to_continue)
            layout.add_widget(btn_continuer)

            btn_menu = Button(
                text='Retour au menu', size_hint=(1, 0.3), font_size=24
            )
            btn_menu.bind(on_release=self.parent.to_menu)

            layout.add_widget(btn_menu)

            self.add_widget(layout)



class ClassicScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = ClassicSet()
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

    def to_continue(self,instance = None):
        self.game.score = 0
        self.game.timer = 0
        self.game.init_game()
        self.game_event = Clock.schedule_interval(self.game.update, 1.0 / 60.0)

    def to_menu(self,instance = None):
        self.manager.current = 'menu_screen'
        