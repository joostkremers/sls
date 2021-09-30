from kivy.core.window import Window

from kivy.properties import ObjectProperty

from kivy.uix.image import AsyncImage

from kivy.uix.modalview import ModalView
from kivy.uix.carousel import Carousel


class ImageCarousel(ModalView):
    gallery: Carousel = ObjectProperty()

    def __init__(self, images, **kwargs):
        super().__init__(**kwargs)
        for image in images:
            widget = AsyncImage(source=image)
            self.gallery.add_widget(widget)
        Window.bind(on_key_down=self.key_action)

    def key_action(self, win, keycode, codepoint, text, modifiers):
        if keycode == 275:
            self.gallery.load_next()
        elif keycode == 276:
            self.gallery.load_previous()

    def on_dismiss(self):
        Window.unbind(on_key_down=self.key_action)
