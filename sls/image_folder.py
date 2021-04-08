import os
import hashlib
import base64

from appdirs import AppDirs
from PIL import Image as PILImage
from PIL.ImageOps import exif_transpose


class ImageFolder:
    """A directory containing image files.

    The absolute directory path is stored in the root attribute. The contents of
    the directory are listed in the `contents` attribute. This is a dictionary
    with the paths of all the directories under the root (including the root
    itself) as keys, mapped onto 2-tuples consisting of a list of the
    subdirectories and a list of the files in each directory. The paths used as
    keys are relative paths starting from `root`, which means that the root
    itself is stored under the entry '.'.

    When an ImageFolder is instantiated, a thumbnail directory is created in the
    user's cache dir if one does not already exists.

    Attributes
    ----------
    root : str
        File path of the image directory.
    contents : Dict[str, str]
        Dictionary of directory paths to their contents.
    dirs: AppDirs
        App-specific directories
    thumbnail_dir : str
        File path of the thumbnail directory.

    """

    def __init__(self, root: str):
        """
        Create a ImageFolder instance.

        Parameters
        ----------
        root : str
            File path of the image directory.
        """

        # Set root, contents and dirs attributes.
        self.root = os.path.expanduser(root)
        self.contents = {}
        for directory, subdirs, files in os.walk(self.root):
            rel_dir = os.path.relpath(directory, self.root)
            self.contents[rel_dir] = (subdirs, files)

        self.dirs = AppDirs("sls", "ten.eleven")

        # Set thumbnail_dir attribute.
        self.thumbnail_dir = os.path.join(
            self.dirs.user_cache_dir,
            ImageFolder.generate_dir_name(self.root),
            "thumbnails",
        )
        os.makedirs(self.thumbnail_dir, exist_ok=True)

    def __str__(self):
        result = ""
        for key, val in self.contents.items():
            result += f"{key}: {val}\n"

        return result

    @staticmethod
    def generate_dir_name(path):
        """Generate a unique directory name based on `path`.

        Return a directory name consisting of the base name of `path` followed
        by the first 8 characters of the base64-encoded sha256 hash of `path`.
        This should ensure that if we create two ImageFolder objects with the
        same base name but different paths, they won't collide.

        Parameters
        ----------
        path : str
            Path to generate a directory name for.

        Returns
        -------
        str
            Generated base name.

        """
        d = os.path.basename(path)
        h = hashlib.sha256(path.encode())
        b = base64.urlsafe_b64encode(h.digest()).decode()[:8]

        return f"{d}-{b}"

    def first_image(self, folder: str):
        """Return the first image in the folder.

        Take the first picture in folder and return its absolute file path. The
        returned file is the first file listed for the folder in self.contents.
        If this folder does not contain any images, return the stock image
        'missing_image.png'.

        Parameters
        ----------
        folder : str
            Relative path of the folder, starting from `self.root`.

        Returns
        -------
        str
            Relative path of the image, starting from `self.root`.

        """

        files = self.contents[folder][1]
        if files:
            return os.path.join(folder, files[0])
        else:
            return "../Images/missing_image.png"

    def create_thumbnail(self, image_path: str) -> str:
        """Create a thumbnail for `image` and return its file path.

        If the thumbnail already exists, just return its path. If the thumbnail
        cannot be created, return the path to the stock image
        'missing_image.png'.

        Parameters
        ----------
        image_path : str
            Path of the image, relative to `self.root`.

        Returns
        -------
        str
            Absolute file path of the thumbnail.

        """
        thumbnail_path = os.path.join(self.thumbnail_dir, image_path)

        # https://openclipart.org/detail/298746/missing-image

        try:
            if os.path.exists(thumbnail_path):
                return thumbnail_path
            with PILImage.open(os.path.join(self.root, image_path)) as image:
                thumbnail_dir = os.path.dirname(thumbnail_path)
                if not os.path.exists(thumbnail_dir):
                    os.makedirs(thumbnail_dir)

                # Transpose the image, because `thumbnail()` doesn't retain
                # exif-data and thus removes the "Orientation".
                transposed_image = exif_transpose(image)
                transposed_image.thumbnail((500, 500))
                transposed_image.save(thumbnail_path)
        except OSError:
            thumbnail_path = "../Images/missing_image.png"

        return thumbnail_path


if __name__ == "__main__":
    imgfldr = ImageFolder("~/src/Python/sls/Pictures")
