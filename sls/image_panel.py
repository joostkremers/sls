import os.path
from typing import List

from kivy.properties import ObjectProperty, ListProperty, StringProperty

from kivy.metrics import dp

from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

from sls.sparsegridlayout import SparseGridLayout, SparseGridEntry
from sls.image_library import ImageLibrary
from sls.utils import chunk, prettify_path


class SLSImage(ButtonBehavior, SparseGridEntry, Image):
    pass


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


class ImagePanel(RecycleView):
    library: ImageLibrary = ObjectProperty()

    def create_image_row(self, images: List[str], cols=3) -> dict:
        """Create a row of images.

        The returned dict can be added to the `data` attribute of the ImagePanel
        so that it can be displayed in the widget.

        Parameters
        ----------
        images
            List of image paths.
        cols
            Number of images per row.

        Returns
        -------
        dict
            Data representing the image row.

        """

        thumbnails = [self.library.create_thumbnail(file) for file in images]
        return {
            "widget": "SLSImageRow",
            "columns": cols,
            "rows": 1,
            "image_paths": thumbnails,
        }

    def create_folder_row(self, path: str) -> dict:
        """Create a folder row.

        A folder row consists of a single image (the thumbnail of the first
        image in the directory) inside a folder icon. The returned dict can be
        added to the data property of the ImagePanel so that it can be displayed
        in the widget.

        Parameters
        ----------
        path
            Path of the directory to display in the folder row.

        Returns
        -------
        dict
            Data representing the folder row.

        """
        image_path = self.library.first_image(path)
        thumbnail = self.library.create_thumbnail(image_path)
        return {
            "widget": "SLSFolderRow",
            "columns": 3,
            "rows": 1,
            "image_path": thumbnail,
        }

    def add_label(self, path: str, main: bool = False):
        label = {
            "widget": "SLSFolderLabel",
            "text": prettify_path(path),
            "main": main,
        }

        if not main:
            label["height"] = dp(20)

        self.data.append(label)

    def add_folder(self, directory: str, subdirs: List[str], files: List[str]):
        """Add the contents of a directory to the SLSView.

        This creates a label, a series of ImageRow objects to represent the
        images and a series of FolderRow objects to represent the subdirectories
        of `directory`.

        Parameters
        ----------
        directory
            Path of the directory to be added, relative to `self.folder.root`.
        subdirs
            Paths of the subdirs in `directory`.
        files
            The files in `directory`.

        """

        # Note: `directory` can be an empty string, which represents the root
        # directory of the image folder. In this case, no label needs to be
        # created.
        if directory:
            self.add_label(directory)

        if files:
            rows = chunk(files, 3)
            for row in rows:
                self.data.append(
                    self.create_image_row(
                        [os.path.join(directory, file) for file in row]
                    )
                )

        for subdir in subdirs:
            subdir_path = os.path.join(directory, subdir)
            self.add_label(subdir_path)
            self.data.append(self.create_folder_row(subdir_path))
