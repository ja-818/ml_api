import hashlib
import os


def allowed_file(filename):
    """
    Checks if the format for the file received is acceptable. For this
    particular case, we must accept only image files. This is, files with
    extension ".png", ".jpg", ".jpeg" or ".gif".

    Parameters
    ----------
    filename : str
        Filename from werkzeug.datastructures.FileStorage file.

    Returns
    -------
    bool
        True if the file is an image, False otherwise.
    """
    if filename.split(".")[1] in ["png", "jpg", "jpeg", "gif"]:
      return True
    else:
      return False


def get_file_hash(file):
    """
    Returns a new filename based on the file content using MD5 hashing.
    It uses hashlib.md5() function from Python standard library to get
    the hash.

    Parameters
    ----------
    file : werkzeug.datastructures.FileStorage
        File sent by user.

    Returns
    -------
    str
        New filename based in md5 file hash.
    """
    # m = hashlib.md5(os.path.basename(file.filename).encode('utf-8'))
    hash = hashlib.md5(file.read()).hexdigest()
    extension = os.path.basename(file.filename).split(".")[1]
    filename = f"{hash}.{extension}"
    return filename