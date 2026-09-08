from kivy.app import App                                    # pyright: ignore[reportMissingImports]
from kivy.lang import Builder                               # pyright: ignore[reportMissingImports]
from kivy.uix.screenmanager import ScreenManager            # pyright: ignore[reportMissingImports]

from menu import MenuScreen
from classic import ClassicScreen
from infini import InfiniScreen


class MonApplication(App):

  def build(self):
    sm = ScreenManager()

    sm.add_widget(MenuScreen(name='menu_screen'))
    sm.add_widget(ClassicScreen(name='classic_screen'))
    sm.add_widget(InfiniScreen(name='infini_screen'))

    return sm


if __name__ == '__main__':
  MonApplication().run()