import os.path

from kivy.app import App

from kivy.properties import ObjectProperty

from kivy.uix.boxlayout import BoxLayout

from sls.image_library import ImageLibrary
from sls.image_panel import ImagePanel
from sls.image_carousel import ImageCarousel


class SLSView(BoxLayout):
    """The main window of the program.

    The SLSView contains a MenuBar and a RecycleView that holds the actual
    images.

    Attributes
    ----------
    library
        The ImageLibrary instance holding the image data.
    view
        The ImagePanel instance displaying the images.

    """

    library: ImageLibrary = ObjectProperty()
    view: ImagePanel = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.library = ImageLibrary("~/src/Python/sls/Pictures")

        # We pass "" as the `directory` argument of `add_folder`, not '.',
        # because the directory is combined with the names of its subdirs using
        # `os.path.join`. With '.', this leads to paths like "./subdir", which
        # subsequently cannot be found in `self.folder.contents` when
        # `add_folder` creates sections for the subdir.

        # An empty `directory` argument also means that no title label is added,
        # which is fine, because we want to add a special one here:

        path = os.path.relpath(self.library.root, os.path.expanduser("~"))
        self.view.add_label(path=path, main=True)
        self.view.add_folder("", *self.library.contents["."])

        # root.ids.app_title.text = self.folder.root

    def show_carousel(self, thumbnail_path: str):
        """Open the image carousel.

        The image carousel is opened with the image corresponding to the
        thumbnail as the first image. The other images in the directory
        containing the thumbnail are part of the carousel.

        Parameters
        ----------
        thumbnail_path
            Path to the thumbnail for which the image should be shown.

        """
        img_dir = self.library.thumbnail_to_dir(thumbnail_path)
        img_name = os.path.basename(thumbnail_path)
        img_names = self.library.list_images(img_dir, first=img_name)
        img_paths = [os.path.join(self.library.root, img_dir, img) for img in img_names]
        carousel = ImageCarousel(img_paths)
        carousel.open()


class SLSApp(App):
    def build(self):
        return SLSView()


if __name__ == "__main__":
    SLSApp().run()
