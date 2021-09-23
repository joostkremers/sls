import os.path

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

from kivy.properties import ObjectProperty, ListProperty, StringProperty

from kivy.uix.recycleview import RecycleView

from sls.image_folder import ImageFolder
from sls.sparsegridlayout import SparseGridLayout, SparseGridEntry
from sls.image_panel import ImagePanel


class SLSImage(ButtonBehavior, SparseGridEntry, Image):
    def on_release(self):
        print(f"Image clicked: {self.source}")


class SLSImageRow(SparseGridLayout):
    image_paths = ListProperty()

    def on_image_paths(self, instance, value):
        self.clear_widgets()
        for index, path in enumerate(self.image_paths):
            image = SLSImage(row=0, column=index, source=path)
            self.add_widget(image)


class SLSFolder(ButtonBehavior, SparseGridEntry, Image):
    def on_release(self):
        print(f"Folder clicked: {self.source}")


class SLSFolderRow(SparseGridLayout):
    image_path = StringProperty()

    def on_image_path(self, instance, value):
        self.clear_widgets()
        image = SLSFolder(row=0, column=0, source=self.image_path)
        self.add_widget(image)


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

        self.view.folder = ImageFolder("~/src/Python/sls/Pictures")

        # We pass "" as the `directory` argument of `add_folder`, not '.',
        # because the directory is combined with the names of its subdirs using
        # `os.path.join`. With '.', this leads to paths like "./subdir", which
        # subsequently cannot be found in `self.folder.contents` when
        # `add_folder` creates sections for the subdir.

        # An empty `directory` argument also means that no title label is added,
        # which is fine, because we want to add a special one here:

        path = os.path.relpath(self.view.folder.root, os.path.expanduser("~"))
        self.view.add_label(path=path, main=True)
        self.view.add_folder("", *self.view.folder.contents["."])

        # root.ids.app_title.text = self.folder.root


class SLSApp(App):
    def build(self):
        return SLSView()


if __name__ == "__main__":
    SLSApp().run()
