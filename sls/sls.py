import os.path
from typing import List

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from kivy.properties import StringProperty

from sls.image_folder import ImageFolder


class SLSImage(Image):
    def __init__(self, path, **kwargs):
        super(SLSImage, self).__init__(**kwargs)
        self.source = path


class SLSFolder(Image):
    def __init__(self, path, **kwargs):
        super(SLSFolder, self).__init__(**kwargs)
        self.source = path


class SLSSection(BoxLayout):
    path = StringProperty("New section")


class SLSView(BoxLayout):
    """Widget that holds the images being displayed.

    The SLSView widget contains any number of SLSSection widgets, which hold the
    actual images.

    Attributes
    ----------
    folder : ImageFolder
        The directory for which images are displayed.

    """

    def __init__(self, **kwargs):
        super(SLSView, self).__init__(**kwargs)

        self.folder = ImageFolder("~/src/Python/sls/Pictures")
        # We pass "" as the `directory` argument of `add_section`, not '.',
        # because the directory is combined with the names of its subdir using
        # `os.path.join`. With '.', this leads to paths like "./subdir", which
        # subsequently cannot be found in `self.folder.contents` when
        # `add_section` creates sections for the subdir.
        self.add_section("", *self.folder.contents["."])

        # root.ids.app_title.text = self.folder.root

    def add_section(self, directory: str, subdirs: List[str], files: List[str]):
        """Add one or more SLSSections to the SLSView.

        If `files` is not empty, a section is added for it. If `subdirs` is not
        empty, a section is added for each directory in `subdirs`.

        Parameters
        ----------
        directory : str
            Path of the directory to be added, relative to `self.folder.root`.
        subdirs : List[str]
            Paths of the subdirs in `directory`.
        files : List[str]
            The files in `directory`.

        """

        root = self.folder.root

        if files:
            section = SLSSection()
            section.path = os.path.join(root, directory)
            for file in files:
                thumbnail = self.folder.create_thumbnail(os.path.join(directory, file))
                image = SLSImage(thumbnail)
                section.ids.grid.add_widget(image)

            self.add_widget(section)

        for subdir in subdirs:
            section = SLSSection()
            folder_path = os.path.join(root, directory, subdir)
            section.path = folder_path
            image_path = self.folder.first_image(os.path.join(directory, subdir))
            folder = SLSFolder(image_path)

            section.ids.grid.add_widget(folder)
            self.add_widget(section)


class RootWidget(BoxLayout):
    pass


class SLSApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    SLSApp().run()
