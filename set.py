from random import randint
from itertools import combinations
from kivy.graphics import Color, Ellipse, Line, Mesh, Rectangle     # pyright: ignore[reportMissingImports]
from kivy.uix.gridlayout import GridLayout                      # pyright: ignore[reportMissingImports]
from kivy.app import App                                        # pyright: ignore[reportMissingImports]
from kivy.clock import Clock                                    # pyright: ignore[reportMissingImports]
from kivy.properties import ListProperty, NumericProperty, ObjectProperty     # pyright: ignore[reportMissingImports]
from kivy.uix.button import Button                              # pyright: ignore[reportMissingImports]
from kivy.uix.widget import Widget                                  # pyright: ignore[reportMissingImports]
from kivy.uix.boxlayout import BoxLayout                             # pyright: ignore[reportMissingImports]
"""
Symbol :
    carre = 0 
    triangle = 1
    rond = 2

Fond :
    plein = 0
    vide = 1
    rayé = 2

Couleur :
    vert = 0
    rouge = 1
    bleu = 2
    """


# --- WIDGET QUI DESSINE UNE SEULE FORME ---
class ShapeWidget(Widget):

  def __init__(self, symbole, fond, couleur_rgba, **kwargs):
    super().__init__(**kwargs)
    self.symbole = symbole  # 0: carré, 1: triangle, 2: rond
    self.fond = fond  # 0: plein, 1: vide, 2: hachuré
    self.couleur_rgba = couleur_rgba

    # Se redessine automatiquement si la taille ou position change
    self.bind(pos=self.draw, size=self.draw)

  def draw(self, *args):
    self.canvas.clear()
    if self.width <= 0 or self.height <= 0:
      return

    with self.canvas:
      Color(*self.couleur_rgba)

      # Centre et dimensions de la forme
      cx, cy = self.center_x, self.center_y
      w, h = min(self.width, 30), min(self.height, 30)

      # --- 1. GESTION DES FORMES & REMPLISSAGE ---

      # A. DESSIN DU ROND (symbole == 2)
      if self.symbole == 2:
        pos = (cx - w / 2, cy - h / 2)
        if self.fond == 0:  # Plein
          Ellipse(pos=pos, size=(w, h))
        elif self.fond == 1:  # Vide (contour)
          Line(ellipse=(pos[0], pos[1], w, h), width=2)
        elif self.fond == 2:  # Hachuré
          Line(ellipse=(pos[0], pos[1], w, h), width=1.5)
          # Lignes de hachures internes
          for offset in range(-int(w / 3), int(w / 3), 6):
            Line(
                points=[cx + offset, cy - h / 3, cx + offset, cy + h / 3],
                width=1.1,
            )

      # B. DESSIN DU CARRÉ (symbole == 0)
      elif self.symbole == 0:
        pos = (cx - w / 2, cy - h / 2)
        if self.fond == 0:  # Plein
          Rectangle(pos=pos, size=(w, h))
        elif self.fond == 1:  # Vide
          Line(rectangle=(pos[0], pos[1], w, h), width=2)
        elif self.fond == 2:  # Hachuré
          Line(rectangle=(pos[0], pos[1], w, h), width=1.5)
          for offset in range(-int(w / 2) + 4, int(w / 2), 6):
            Line(
                points=[
                    cx + offset,
                    cy - h / 2 + 2,
                    cx + offset,
                    cy + h / 2 - 2,
                ],
                width=1.1,
            )

      # C. DESSIN DU TRIANGLE (symbole == 1)
      elif self.symbole == 1:
        p1 = (cx, cy + h / 2)
        p2 = (cx - w / 2, cy - h / 2)
        p3 = (cx + w / 2, cy - h / 2)

        if self.fond == 0:  # Plein
          Mesh(
              vertices=[p1[0], p1[1], 0, 0, p2[0], p2[1], 0, 0, p3[0], p3[1], 0, 0],
              indices=[0, 1, 2],
              mode='triangle_fan',
          )
        elif self.fond == 1:  # Vide
          Line(
              points=[p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], p1[0], p1[1]],
              width=2,
          )
        elif self.fond == 2:  # Hachuré
          Line(
              points=[p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], p1[0], p1[1]],
              width=1.5,
          )
          for y_off in range(-int(h / 3), int(h / 3), 6):
            Line(points=[cx - w / 4, cy + y_off, cx + w / 4, cy + y_off], width=1.1)


class SetCard(Button):
    # 1. DÉCLARATION DES PROPRIÉTÉS 
    nombre = NumericProperty(0)
    symbole = NumericProperty(0)
    fond = NumericProperty(0)
    couleur_rgba = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 2. AFFECTATION DES VALEURS 
        self.nombre = randint(0, 2)  # 0, 1 ou 2
        self.symbole = randint(0, 2)  # 0: carré, 1: triangle, 2: rond
        self.fond = randint(0, 2)  # 0: plein, 1: vide, 2: hachuré

        couleur = randint(0, 2)
        if couleur == 0:
            self.couleur_rgba = [0.1, 0.9, 0.3, 1]  # Vert (entre 0 et 1)
        elif couleur == 1:
            self.couleur_rgba = [1.0, 0.25, 0.25, 1]  # Rouge (entre 0 et 1)
        else:
            self.couleur_rgba = [0.1, 0.7, 1.0, 1]  # Bleu (entre 0 et 1)

        self.attribut = (self.nombre, couleur, self.fond, self.symbole)
        
        # --- CREATION DE LA DISPOSITION DES SYMBOLES ---
        # Un layout vertical interne pour empiler 1, 2 ou 3 formes
        layout_interne = BoxLayout(
            orientation='horizontal',
            spacing=5,
            padding=10,
            pos=self.pos,
            size=self.size,
        )

        # Synchroniser la position du layout avec le bouton
        self.bind(
            pos=lambda instance, value: setattr(layout_interne, 'pos', value),
            size=lambda instance, value: setattr(layout_interne, 'size', value),
        )

        # Ajouter 1, 2 ou 3 formes (nombre + 1)
        quantite = self.nombre + 1
        for _ in range(quantite):
            shape = ShapeWidget(
                symbole=self.symbole,
                fond=self.fond,
                couleur_rgba=self.couleur_rgba,
            )
            layout_interne.add_widget(shape)

        self.add_widget(layout_interne)


class SetGame(GridLayout):
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4  # 4 colonnes pour afficher les 12 cartes (3 lignes de 4)
        self.spacing = 10
        self.padding = 10
        self.selection = []
        self.cartes = []
        

    def reset_game(self):
        """reinitialise le jeu"""
        # pour chaque carte selectionnée en creer une nouvelle a la place 
        for in_set in self.selection :
            new_card = SetCard()  # Création d'une nouvelle carte
            emplacement = self.cartes.index(in_set)
            
            while any(c.attribut == new_card.attribut for c in self.cartes):
                new_card = SetCard()  # Création d'une nouvelle carte
            self.cartes.remove(in_set)
            # carte non présente dans le plateau
            self.cartes.insert(emplacement,new_card)
            new_card.bind(on_release=self.on_card_click)
            

        self.selection.clear()
        self.clear_widgets()
        for card in self.cartes :
            self.add_widget(card)
        if not self.combinaison():
           #aucun set dans les cartes
           self.init_game()
                
            

    def init_game(self):
        """initialise le jeu"""
        has_set = False
        
        while not has_set:
            self.selection.clear()
            self.clear_widgets()
            self.cartes = []
            while len(self.cartes) < 12:
                new_card = SetCard()  # Création d'une nouvelle carte

                if not any(c.attribut == new_card.attribut for c in self.cartes):
                    self.cartes.append(new_card)
                    new_card.bind(on_release=self.on_card_click)
                    self.add_widget(new_card)
            has_set = self.combinaison()
        


    def is_set(self,card1, card2, card3):
        """Vérifie si 3 cartes forment un Set valide."""
        # astuce somme des 3 valeurs modulo 3 ==0 alors valide 
        # il faut tester sur toutes les caracteristiques
        # On parcourt chaque attribut (index 0 à 3)
        for attr_idx in range(4):
            total = (
                card1.attribut[attr_idx]
                + card2.attribut[attr_idx]
                + card3.attribut[attr_idx]
            )
            if total % 3 != 0:
                return False  # Un des attribut ne valide pas la condition

        return True  # Tous les attributs sont vlides

    def combinaison(self):
        """verifie qu'il existe un set avec les cartes du plateu 
        renvoie vrai si existence"""
        
        for [card1, card2, card3] in list(combinations(self.cartes, 3)):
            if self.is_set(card1, card2, card3):
                return True
        return False
        
            
    def on_card_click(self, instance):
        """Méthode appelée quand le joueur clique sur une carte."""
        if instance not in self.selection :
            self.selection.append(instance)
        else :
            self.selection.remove(instance)
                        
    def update(self,dt):
       if len(self.selection) == 3 :
            c1, c2, c3 = self.selection[0], self.selection[1], self.selection[2]
            if self.is_set(c1,c2,c3) :
                self.reset_game()
            else :
                self.selection.clear()

