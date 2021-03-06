import os.path
from typing import List

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

from kivy.properties import ObjectProperty, ListProperty, StringProperty

from kivy.metrics import dp

from sls.image_folder import ImageFolder
from sls.sparsegridlayout import SparseGridLayout, SparseGridEntry


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

        self.view.data.append(
            {
                "widget": "SLSFolderLabel",
                "text": self.prettify_path(
                    os.path.relpath(self.folder.root, os.path.expanduser("~"))
                ),
                "main": True,
            }
        )

        self.add_folder("", *self.folder.contents["."])

        # root.ids.app_title.text = self.folder.root

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
                self.view.data.append(
                    self.create_image_row(
                        [os.path.join(directory, file) for file in row]
                    )
                )

        for subdir in subdirs:
            subdir_path = os.path.join(directory, subdir)
            self.view.data.append(self.create_label(subdir_path))
            self.view.data.append(self.create_folder(subdir_path))

    def create_label(self, path: str):
        return {
            "widget": "SLSFolderLabel",
            "text": self.prettify_path(path),
            "main": False,
            "height": dp(20),
        }

    def create_image_row(self, images: List[str]):
        thumbnails = [self.folder.create_thumbnail(file) for file in images]
        return {
            "widget": "SLSImageRow",
            "columns": 3,
            "rows": 1,
            "image_paths": thumbnails,
        }

    def create_folder(self, path: str):
        image_path = self.folder.first_image(path)
        thumbnail = self.folder.create_thumbnail(image_path)
        return {
            "widget": "SLSFolderRow",
            "columns": 3,
            "rows": 1,
            "image_path": thumbnail,
        }


class SLSApp(App):
    def build(self):
        return SLSView()


if __name__ == "__main__":
    SLSApp().run()
