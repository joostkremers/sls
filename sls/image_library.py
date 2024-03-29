import os
import hashlib
import base64

from typing import Dict, Optional, Tuple, List

from appdirs import AppDirs
from PIL import Image as PILImage
from PIL.ImageOps import exif_transpose


class ImageLibrary:
    """A directory containing image files.

    The absolute directory path is stored in the root attribute. The contents of
    the directory are listed in the `contents` attribute. This is a dictionary
    with the paths of all the directories under the root (including the root
    itself) as keys, mapped onto 2-tuples consisting of a list of the
    subdirectories and a list of the files in each directory. The paths used as
    keys are relative paths starting from `root`, which means that the root
    itself is stored under the entry '.'.

    When an ImageLibrary is instantiated, a thumbnail directory is created in the
    user's cache dir if one does not already exist.

    Attributes
    ----------
    root
        File path of the image directory.
    contents
        Dictionary of directory paths to their contents.
    app_dirs
        App-specific directories
    thumbnail_dir
        File path of the thumbnail directory.

    """

    root: str
    contents: Dict[str, Tuple[List[str], List[str]]]
    dirs: AppDirs
    thumbnail_dir: str

    def __init__(self, root: str):
        """
        Create an ImageLibrary instance.

        Parameters
        ----------
        root
            File path of the image directory.
        """

        # Set root, contents and dirs attributes.
        self.root = os.path.expanduser(root)
        self.contents = {}
        for directory, subdirs, files in os.walk(self.root):
            rel_dir = os.path.relpath(directory, self.root)
            self.contents[rel_dir] = (subdirs, files)

        self.app_dirs = AppDirs("sls", "ten.eleven")

        # Set thumbnail_dir attribute.
        self.thumbnail_dir = os.path.join(
            self.app_dirs.user_cache_dir,
            ImageLibrary.generate_dir_name(self.root),
            "thumbnails",
        )
        os.makedirs(self.thumbnail_dir, exist_ok=True)

    def __str__(self):
        result = ""
        for key, val in self.contents.items():
            result += f"{key}: {val}\n"

        return result

    @staticmethod
    def generate_dir_name(path: str) -> str:
        """Generate a unique directory name based on `path`.

        Return a directory name consisting of the base name of `path` followed
        by the first 8 characters of the base64-encoded sha256 hash of `path`.
        This should ensure that if we create two ImageLibrary objects with the
        same base name but different paths, they won't collide.

        Parameters
        ----------
        path
            Path to generate a directory name for.

        Returns
        -------
        Generated base name.

        """
        d = os.path.basename(path)
        h = hashlib.sha256(path.encode())
        b = base64.urlsafe_b64encode(h.digest()).decode()[:8]

        return f"{d}-{b}"

    def first_image(self, folder: str) -> str:
        """Return the first image in the folder.

        Take the first image in folder and return its absolute file path. The
        returned file is the first file listed for the folder in self.contents.
        If this folder does not contain any images, return the stock image
        'missing_image.png'.

        Parameters
        ----------
        folder
            Relative path of the folder, starting from `self.root`.

        Returns
        -------
        Relative path of the image, starting from `self.root`.

        """

        files = self.contents[folder][1]
        if files:
            return os.path.join(folder, files[0])
        else:
            return "resources/missing_image.png"

    def create_thumbnail(self, image_path: str) -> str:
        """Create a thumbnail for `image` and return its file path.

        If the thumbnail already exists, just return its path. If the thumbnail
        cannot be created, return the path to the stock image
        'missing_image.png'.

        Parameters
        ----------
        image_path
            Path of the image, relative to `self.root`.

        Returns
        -------
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
                transposed_image.thumbnail((100, 100))
                transposed_image.save(thumbnail_path)
        except OSError:
            thumbnail_path = "resources/missing_image.png"

        return thumbnail_path

    def thumbnail_to_image(self, thumb: str) -> str:
        """Return the path to the full image of a thumbnail.

        Parameters
        ----------
        thumb
            Absolute path of the thumbnail file.

        Returns
        -------
            Absolute path of the image file.
        """

        path, basename = os.path.split(thumb)
        rel_path = os.path.relpath(path, start=self.thumbnail_dir)
        return os.path.join(self.root, rel_path, basename)

    def thumbnail_to_dir(self, thumb: str) -> str:
        """Return the relative directory of a thumbnail.

        The relative path of the thumbnail's directory is also the relative path
        of the original image in the image library.

        Parameters
        ----------
        thumb
            Absolute path of the thumbnail file.

        Returns
        -------
            Relative path of the directory containing the thumbnail.

        """
        path = os.path.dirname(thumb)
        rel_path = os.path.relpath(path, start=self.thumbnail_dir)
        return rel_path

    def list_images(self, directory: str, first: Optional[str] = None) -> List[str]:
        """Return the file names of all images in `directory`.

        If `first` is given, it will be the first image in the list.

        Parameters
        ----------
        directory
            The relative directory for which the images should be listed.
        first
            The image that should be first in the list.

        Returns
        -------
            The list of file names.

        """
        images = self.contents[directory][1]
        if first:
            i = images.index(first)
            images = images[i:] + images[:i]
        return images


if __name__ == "__main__":
    imgfldr = ImageLibrary("~/src/Python/sls/Pictures")
