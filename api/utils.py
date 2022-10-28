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
    return filename.lower().endswith(('.png', '.jpg', '.jpeg', ".gif"))

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
    # get unique hash for the file and digest it
    new_filename = hashlib.md5(file.read()).hexdigest()
    # return reading pointer to the first position
    file.seek(0)
    
    # Loop to get the extension of the image
    for ext in ('.png', '.jpg', '.jpeg', ".gif"):
      if os.path.basename(file.filename).endswith(ext):
        new_filename += ext
        break
    
    return new_filename