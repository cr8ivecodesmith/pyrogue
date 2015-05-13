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
        self.x += dx
        self.y += dy
        self.sprite.pos = self.pos


class PyRogueGame(Widget):

    keypress_label = ObjectProperty(None)
    move_speed = 10

    def __init__(self, **kwargs):
        super(PyRogueGame, self).__init__(**kwargs)

        # Request for keyboard and bind keypresses to `self.press()`
        self._keyboard = Window.request_keyboard(self.close, self)
        self._keyboard.bind(on_key_down=self.press)

        self.load_initial_widgets()

    def close(self):
        self._keyboard.unbind(on_key_down=self.press)
        self._keyboard = None

    def load_initial_widgets(self):
        widgets = [
            BaseSprite(
                id='player',
                sprite_text='@',
                sprite_color=[255, 255, 255, 1],
                x=self.width / 2,
                y=self.height / 2
            ),
            BaseSprite(
                id='npc',
                sprite_text='@',
                sprite_color=[255, 255, 0, 1],
                x=self.width / 2 - 20,
                y=self.height / 2
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
            self._widget('player').x,
            self._widget('player').y,
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


class PyRogueApp(App):
    def build(self):
        game = PyRogueGame()
        return game


if __name__ == '__main__':
    PyRogueApp().run()
