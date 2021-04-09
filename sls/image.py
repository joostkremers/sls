from kivy.uix.image import Image


class SLSImage(Image):
    """SLS image class.

    This is essentially a kivy Image.

    """

    def __init__(self, path, **kwargs):
        """Create an SLSImage instance.

        Parameters
        ----------
        path : str
            The absolute path of the image.

        """

        super(SLSImage, self).__init__(**kwargs)
        self.source = path
