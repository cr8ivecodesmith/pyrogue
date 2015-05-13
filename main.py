#!/usr/bin/python3
import pdb
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class BaseSprite(Widget):
    """ BaseSprite Object

    Important properties to add value upon initialization:
    - sprite_text
    - sprite_color
    - sprite_center_x
    - sprite_center_y

    """
    sprite = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(BaseSprite, self).__init__(**kwargs)
        self.sprite.text = kwargs.get('sprite_text', self.sprite.text)
        self.sprite.color = kwargs.get('sprite_color', self.sprite.color)
        self.sprite.center_x = kwargs.get('sprite_center_x', self.sprite.center_x)
        self.sprite.center_y = kwargs.get('sprite_center_y', self.sprite.center_y)

    def move(self, dx, dy):
        """ Move by the given amount (dx) (dy)

        """
        self.sprite.center_x += dx
        self.sprite.center_y += dy


class PyRogueGame(Widget):

    keypress_label = ObjectProperty(None)
    move_speed = 10

    def __init__(self, **kwargs):
        super(PyRogueGame, self).__init__(**kwargs)

        # Request for keyboard and bind keypresses to `self.press()`
        self._keyboard = Window.request_keyboard(self.close, self)
        self._keyboard.bind(on_key_down=self.press)

        self.load_initial_widgets()

        self.keypress_label.text = 'parent w: {} h: {}\nx: {}, y: {}\nkey: {}'.format(
            0,
            0,
            self._widget('player').sprite.center_x,
            self._widget('player').sprite.center_y,
            '()'
        )

    def close(self):
        self._keyboard.unbind(on_key_down=self.press)
        self._keyboard = None

    def load_initial_widgets(self):
        widgets = [
            BaseSprite(
                id='player',
                sprite_text='@',
                sprite_color=[255, 255, 255, 1],
                sprite_center_x=self.width / 2,
                sprite_center_y=self.height / 2
            ),
            BaseSprite(
                id='npc',
                sprite_text='@',
                sprite_color=[255, 255, 0, 1],
                sprite_center_x=self.width / 2 - 20,
                sprite_center_y=self.height / 2
            )
        ]

        for widget in widgets:
            self.add_widget(widget)

    def _widget(self, widget_id):
        widget = None
        for obj in self.walk(restrict=True):
            if obj.id == widget_id:
                widget = obj
                break
        return widget

    def press(self, keyboard, keycode, text, modifiers):
        self.keypress_label.text = 'parent w: {} h: {}\nx: {}, y: {}\nkey: {}'.format(
            self.parent.width,
            self.parent.height,
            self._widget('player').sprite.center_x,
            self._widget('player').sprite.center_y,
            keycode
        )

        if keycode[1] == 'left' or keycode[1] == 'h':
            move_p = self.move_speed if self._widget('player').sprite.center_x > 0 else 0
            self._widget('player').sprite.center_x -= move_p

        if keycode[1] == 'right' or keycode[1] == 'l':
            move_p = self.move_speed if self._widget('player').sprite.center_x < self.parent.width else 0
            self._widget('player').sprite.center_x += move_p

        if keycode[1] == 'up' or keycode[1] == 'k':
            move_p = self.move_speed if self._widget('player').sprite.center_y < self.parent.height else 0
            self._widget('player').sprite.center_y += move_p

        if keycode[1] == 'down' or keycode[1] == 'j':
            move_p = self.move_speed if self._widget('player').sprite.center_y > 0 else 0
            self._widget('player').sprite.center_y -= move_p


class PyRogueApp(App):
    def build(self):
        game = PyRogueGame()
        return game


if __name__ == '__main__':
    PyRogueApp().run()
