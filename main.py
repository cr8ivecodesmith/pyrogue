#!/usr/bin/python3
import pdb
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class MapTile(Widget):
    """ MapTile object

    """
    tile = ObjectProperty(None)
    color_dark_wall = [0, 0, 100, 1]
    color_dark_ground = [50, 50, 150, 1]

    def __init__(self, blocked, block_sight=None, **kwargs):
        super(MapTile, self).__init__(**kwargs)
        self.blocked = blocked
        self.block_sight = block_sight or blocked
        self.tile.pos = self.pos

        if self.block_sight:
            self.tile.color = self.color_dark_wall
        else:
            self.tile.color = self.color_dark_ground

    def set_block_sight(self, value=None):
        self.block_sight = bool(value)

        if value:
            self.tile.color = self.color_dark_wall
            self.tile.text = '#'
        else:
            self.tile.color = self.color_dark_ground
            self.tile.text = '.'

    def set_blocked(self, value):
        self.blocked = value

        if self.block_sight:
            self.tile.color = self.color_dark_wall
            self.tile.text = '#'
        else:
            self.tile.color = self.color_dark_ground
            self.tile.text = '.'


class BaseSprite(Widget):
    """ BaseSprite Object

    Important properties to add value upon initialization:
    - sprite_text
    - sprite_color
    - x
    - y

    """
    sprite = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(BaseSprite, self).__init__(**kwargs)
        self.sprite.text = kwargs.get('sprite_text', self.sprite.text)
        self.sprite.color = kwargs.get('sprite_color', self.sprite.color)
        self.sprite.pos = self.pos

    def move(self, dx, dy):
        """ Move by the given amount (dx) (dy)

        NOTE: When the widget moves, all its children should move too.

        """
        self.center_x += dx
        self.center_y += dy
        self.sprite.pos = self.pos


class PyRogueGame(Widget):

    keypress_label = ObjectProperty(None)
    move_speed = 20

    def __init__(self, **kwargs):
        super(PyRogueGame, self).__init__(**kwargs)

        # Request for keyboard and bind keypresses to `self.press()`
        self._keyboard = Window.request_keyboard(self.close, self)
        self._keyboard.bind(on_key_down=self.press)

    def close(self):
        self._keyboard.unbind(on_key_down=self.press)
        self._keyboard = None

    def load_initial_widgets(self):
        # NOTE: The last item on the list becomes the widget with the highest
        #       z-order.
        widgets = [
            Widget(
                id='game_map',
                width=self.width,
                height=self.height,
                pos=self.pos
            ),
            BaseSprite(
                id='npc',
                sprite_text='@',
                sprite_color=[255, 255, 0, 1],
                x=self.width / 2 - self.move_speed,
                y=self.height / 2
            ),
            BaseSprite(
                id='player',
                sprite_text='@',
                sprite_color=[255, 255, 255, 1],
                x=self.width / 2,
                y=self.height / 2
            ),
        ]

        for widget in widgets:
            self.add_widget(widget)

    def _widget(self, widget_id, restrict=True, loopback=False):
        widget = None
        for obj in self.walk(restrict=restrict, loopback=loopback):
            if obj.id == widget_id:
                widget = obj
                break
        return widget

    def press(self, keyboard, keycode, text, modifiers):
        self.keypress_label.text = 'wxh: {}x{}\nx,y: {}\nkey: {}'.format(
            self.width,
            self.height,
            self._widget('player').pos,
            keycode
        )

        if keycode[1] == 'left' or keycode[1] == 'h':
            self._widget('player').move(-self.move_speed, 0)

        if keycode[1] == 'right' or keycode[1] == 'l':
            self._widget('player').move(self.move_speed, 0)

        if keycode[1] == 'up' or keycode[1] == 'k':
            self._widget('player').move(0, self.move_speed)

        if keycode[1] == 'down' or keycode[1] == 'j':
            self._widget('player').move(0, -self.move_speed)

    def make_map(self):
        game_map = self._widget('game_map')
        for y in range(0, game_map.height, self.move_speed):
            for x in range(0, game_map.width, self.move_speed):
                game_map.add_widget(MapTile(
                    id='tile:{},{}'.format(x, y),
                    blocked=False,
                    x=x,
                    y=y
                ))

        # NOTE: Set some tiles to blocking for testing
        for ctr, widget in enumerate(game_map.walk(restrict=True)):
            if 'tile' not in str(widget.id):
                continue
            widget.set_block_sight(True)
            widget.set_blocked(True)
            if ctr > (game_map.width + game_map.height) / 2:
                break


class PyRogueApp(App):
    def build(self):
        game = PyRogueGame()
        game.load_initial_widgets()
        game.make_map()
        return game


if __name__ == '__main__':
    PyRogueApp().run()
