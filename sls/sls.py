import os.path

from kivy.app import App

from kivy.properties import ObjectProperty

from kivy.uix.boxlayout import BoxLayout

from sls.image_library import ImageLibrary
from sls.image_panel import ImagePanel


class SLSView(BoxLayout):
    """The main window of the program.

    The SLSView contains a MenuBar and a RecycleView that holds the actual
    images.

    Attributes
    ----------
    view
        The RecycleView instance holding the images.

    """

    view: ImagePanel = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.view.library = ImageLibrary("~/src/Python/sls/Pictures")

        # We pass "" as the `directory` argument of `add_folder`, not '.',
        # because the directory is combined with the names of its subdirs using
        # `os.path.join`. With '.', this leads to paths like "./subdir", which
        # subsequently cannot be found in `self.folder.contents` when
        # `add_folder` creates sections for the subdir.

        # An empty `directory` argument also means that no title label is added,
        # which is fine, because we want to add a special one here:

        path = os.path.relpath(self.view.library.root, os.path.expanduser("~"))
        self.view.add_label(path=path, main=True)
        self.view.add_folder("", *self.view.library.contents["."])

        # root.ids.app_title.text = self.folder.root


class SLSApp(App):
    def build(self):
        return SLSView()


if __name__ == "__main__":
    SLSApp().run()
