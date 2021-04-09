from kivy.uix.image import Image


class SLSFolder(Image):
    """SLS folder class.

    This is essentially a kivy Image; the image being displayed is the first
    image in the folder.

    Parameters
    ----------
    path : str
        The absolute file path of the image.

    """

    def __init__(self, path, **kwargs):
        super(SLSFolder, self).__init__(**kwargs)
        self.source = path
