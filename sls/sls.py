import os.path
from typing import List

import os

os.environ["KIVY_NO_CONSOLELOG"] = ""

from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

from kivy.properties import ObjectProperty, ListProperty, StringProperty

from kivy.metrics import dp

from sls.image_folder import ImageFolder
from sls.sparsegridlayout import SparseGridLayout, SparseGridEntry

images_rows = 0


class SLSLabel(Label, SparseGridEntry):
    def __repr__(self) -> str:
        return "<SLSLabel: " + self.text + ">"


class SLSImage(ButtonBehavior, Image, SparseGridEntry):
    def on_release(self):
        print(f"Image clicked: {self.source}")

    def __repr__(self) -> str:
        return "<SLSImage: " + self.source + ">"


class SLSFolder(ButtonBehavior, Image, SparseGridEntry):
    def on_release(self):
        print(f"Folder clicked: {self.source}")

    def __repr__(self) -> str:
        return "<SLSFolder " + self.source + ">"


class SLSRow(SparseGridLayout):

    name = StringProperty()
    widget_list = ListProperty()

    def __init__(self, **kwargs):
        super(SLSRow, self).__init__(**kwargs)

        # def on_widget_list(self, instance, widgets):
        print(f"Row: {self.name}")
        print(f"Children: {self.children}")
        print(f"Widgets: {self.widget_list}\n")

        for widget in self.widget_list:
            self.add_widget(widget)


class SLSView(BoxLayout):
    """The main window of the program.

    The SLSView contains a MenuBar and a RecycleView that holds the actual
    images.

    Attributes
    ----------
    folder : ImageFolder
        The directory for which images are displayed.
    view : RecycleView
        The RecycleView instance holding the images.

    """

    view = ObjectProperty()

    @staticmethod
    def chunk(lst: List, chunk_size: int):
        for i in range(0, len(lst), chunk_size):
            yield lst[i : i + chunk_size]

    @staticmethod
    def prettify_path(path: str) -> str:
        return path.replace(os.path.sep, " › ")

    def __init__(self, **kwargs):
        super(SLSView, self).__init__(**kwargs)

        self.folder = ImageFolder("~/src/Python/sls/Pictures")
        # We pass "" as the `directory` argument of `add_folder`, not '.',
        # because the directory is combined with the names of its subdir using
        # `os.path.join`. With '.', this leads to paths like "./subdir", which
        # subsequently cannot be found in `self.folder.contents` when
        # `add_folder` creates sections for the subdir.

        # An empty `directory` argument also means that no title label is added,
        # which is fine, because we want to add a special one here:

        label = SLSLabel()
        label.text = self.prettify_path(
            os.path.relpath(self.folder.root, os.path.expanduser("~"))
        )
        label.main = True

        print(f"Creating Main Label: {label.text}")
        self.view.data.append({"name": "Main", "widget_list": [label]})

        self.add_folder("", *self.folder.contents["."])

    def add_folder(self, directory: str, subdirs: List[str], files: List[str]):
        """Add the contents of a directory to the SLSView.

        Parameters
        ----------
        directory : str
            Path of the directory to be added, relative to `self.folder.root`.
        subdirs : List[str]
            Paths of the subdirs in `directory`.
        files : List[str]
            The files in `directory`.

        """

        if directory:
            self.view.data.append(self.create_label(directory))

        if files:
            rows = self.chunk(files, 3)
            for row in rows:
                row = self.create_image_row(
                    [os.path.join(directory, file) for file in row]
                )

                self.view.data.append(row)

        for subdir in subdirs:
            subdir_path = os.path.join(directory, subdir)
            self.view.data.append(self.create_label(subdir_path))
            self.view.data.append(self.create_folder(subdir_path))

    def create_label(self, path: str):
        label = SLSLabel(text=self.prettify_path(path), main=False, height=dp(20))
        print(f"Creating label {path} : {label}")
        return {"name": f"Label {path}", "widget_list": [label]}

    def create_image_row(self, image_paths: List[str]):
        global images_rows

        images_rows += 1

        thumbnail_paths = [self.folder.create_thumbnail(path) for path in image_paths]
        thumbnails = []
        for index, path in enumerate(thumbnail_paths):
            thumbnails.append(SLSImage(column=index, row=0, source=path))
        print(f"Creating image row {image_paths}")
        return {"name": f"Image Row {images_rows}", "widget_list": thumbnails}

    def create_folder(self, path: str):
        image_path = self.folder.first_image(path)
        thumbnail = SLSFolder(source=self.folder.create_thumbnail(image_path))
        print(f"Creating folder {path} : {thumbnail}")
        return {"name": f"Folder {path}", "widget_list": [thumbnail]}


class SLSApp(App):
    def build(self):
        return SLSView()


if __name__ == "__main__":
    SLSApp().run()
