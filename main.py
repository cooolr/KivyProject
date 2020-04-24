# -*- coding: utf-8 -*-

import os
import sys
from ast import literal_eval

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.utils import get_hex_from_color
from kivy.properties import ObjectProperty, StringProperty

from libs.uix.baseclass.startscreen import StartScreen
from libs.uix.lists import Lists

from kivymd.app import MDApp
from kivymd.toast import toast


__projectname__ = "KivyProject Demo"
__version__ = "1.0"
__copyright__ = "MIT"
__author__ = "Developer"
__site__ = "https://github.com"
__repo__ = "github.com"
__mail__ = ""


class MainApp(MDApp):
    title = __projectname__
    version = __version__
    icon = 'icon.png'
    nav_drawer = ObjectProperty()

    def __init__(self, **kvargs):
        super(MainApp, self).__init__(**kvargs)
        Window.bind(on_keyboard=self.events_program)
        Window.softinput_mode = 'below_target'
        LabelBase.register(name="Roboto", fn_regular="./data/droid.ttf")

        self.list_previous_screens = ['base']
        self.window = Window
        self.config = ConfigParser()
        self.manager = None
        self.exit_interval = False

    def set_value_from_config(self):
        self.config.read(os.path.join(self.directory, 'main.ini'))
        self.style = self.config.get('General', 'theme_style')
        self.theme_cls.theme_style = self.style

    def build(self):
        self.set_value_from_config()
        self.load_all_kv_files(os.path.join(self.directory, 'libs', 'uix', 'kv'))
        self.screen = StartScreen()
        self.manager = self.screen.ids.manager
        self.nav_drawer = self.screen.ids.nav_drawer

        return self.screen

    def load_all_kv_files(self, directory_kv_files):
        for kv_file in os.listdir(directory_kv_files):
            kv_file = os.path.join(directory_kv_files, kv_file)
            if os.path.isfile(kv_file):
                with open(kv_file, encoding='utf-8') as kv:
                    Builder.load_string(kv.read())

    def events_program(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.nav_drawer.state == 'open':
                self.nav_drawer.toggle_nav_drawer()
            self.back_screen(event=keyboard)
        elif keyboard in (282, 319):
            pass

        return True

    def back_screen(self, event=None):
        if event in (1001, 27):
            if self.manager.current == 'base':
                self.dialog_exit()
                return
            try:
                self.manager.current = self.list_previous_screens.pop()
            except:
                self.manager.current = 'base'
            self.screen.ids.action_bar.title = self.title
            self.screen.ids.action_bar.left_action_items = \
                [['menu', lambda x: self.nav_drawer.toggle_nav_drawer()]]

    def show_about(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.screen.ids.about.ids.label.text = \
            (
                u'[size=20][b]{name}[/b][/size]\n\n'
                u'[b]Version:[/b] {version}\n'
                u'[b]License:[/b] {license}\n\n'
                u'[size=20][b]Developer[/b][/size]\n\n'
                u'[ref={site}]'
                u'[color={link_color}]{author}[/color][/ref]\n'
                u'{mail}\n\n'
                u'[b]Source code:[/b] '
                u'[ref={repo}]'
                u'[color={link_color}]GitHub[/color][/ref]').format(
                name=__projectname__,
                version=__version__,
                license=__copyright__,
                author=__author__,
                site=__site__,
                mail=__mail__,
                repo=__repo__,
                link_color=get_hex_from_color(self.theme_cls.primary_color)
            )
        self.manager.current = 'about'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen(27)]]

    def show_license(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.screen.ids.license.ids.text_license.text = \
            open(os.path.join(self.directory, 'LICENSE'), 'r', encoding='utf-8').read()

        self.manager.current = 'license'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen(27)]]
        self.screen.ids.action_bar.title = 'MIT LICENSE'

    def select_style(self, *args):
        if self.style == 'Light':
            self.theme_cls.theme_style = 'Dark'
            self.style = 'Dark'
            self.config.set('General', 'theme_style', self.style)
            self.config.write()
        else:
            self.theme_cls.theme_style = 'Light'
            self.style = 'Light'
            self.config.set('General', 'theme_style', self.style)
            self.config.write()

    def dialog_exit(self):
        def check_interval_press(interval):
            self.exit_interval += interval
            if self.exit_interval > 5:
                self.exit_interval = False
                Clock.unschedule(check_interval_press)

        if self.exit_interval:
            sys.exit(0)
            
        Clock.schedule_interval(check_interval_press, 1)
        toast(('Press Back to Exit'))


if __name__ in ('__main__', '__android__'):
    MainApp().run()
