from kivy.uix.boxlayout import BoxLayout                # pyright: ignore[reportMissingImports]
from kivy.uix.button import Button                      # pyright: ignore[reportMissingImports]
from kivy.uix.screenmanager import Screen               # pyright: ignore[reportMissingImports]
from kivy.uix.label import Label                        # pyright: ignore[reportMissingImports]

class MenuScreen(Screen):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

    text = Label(text='Liste des jeux',
                 font_size=32,
                bold=True,  # Texte en gras
                size_hint=(1, 0.2),)
    layout.add_widget(text)

    btn_classic = Button(
        text='Classic', size_hint=(1, 0.3), font_size=24
    )
    btn_classic.bind(on_release=self.classic)
    layout.add_widget(btn_classic)

    btn_infini = Button(
        text='Infini', size_hint=(1, 0.3), font_size=24
    )
    btn_infini.bind(on_release=self.infini)

    layout.add_widget(btn_infini)

    self.add_widget(layout)


  def classic(self, instance):
    self.manager.current = 'classic_screen'

  def infini(self, instance):
    self.manager.current = 'infini_screen'