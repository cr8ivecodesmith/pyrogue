#!/usr/bin/python3
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class RogueSprite(Widget):
    pass


class PyRogueGame(Widget):
    player = ObjectProperty(None)
    keypress_label = ObjectProperty(None)
    move_speed = 10

    def __init__(self, **kwargs):
        super(PyRogueGame, self).__init__(**kwargs)

        # Request for keyboard and bind keypresses to `self.press()`
        self._keyboard = Window.request_keyboard(self.close, self)
        self._keyboard.bind(on_key_down=self.press)

        self.keypress_label.text = 'x: {}, y: {}\nkey: {}'.format(
            self.player.center_x,
            self.player.center_y,
            '()'
        )

    def close(self):
        self._keyboard.unbind(on_key_down=self.press)
        self._keyboard = None

    def press(self, keyboard, keycode, text, modifiers):
        self.keypress_label.text = 'x: {}, y: {}\nkey: {}'.format(
            self.player.center_x,
            self.player.center_y,
            keycode
        )

        if keycode[1] == 'left' or keycode[1] == 'h':
            move = self.move_speed if self.player.center_x > 0 else 0
            self.player.center_x -= move

        if keycode[1] == 'right' or keycode[1] == 'l':
            move = self.move_speed if self.player.center_x < self.parent.width else 0
            self.player.center_x += move

        if keycode[1] == 'up' or keycode[1] == 'k':
            move = self.move_speed if self.player.center_y < self.parent.height else 0
            self.player.center_y += move

        if keycode[1] == 'down' or keycode[1] == 'j':
            move = self.move_speed if self.player.center_y > 0 else 0
            self.player.center_y -= move


class PyRogueApp(App):
    def build(self):
        game = PyRogueGame()
        return game


if __name__ == '__main__':
    PyRogueApp().run()
