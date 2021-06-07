import io
from PIL import Image


def read_as_numpy_array(raw_bytes: bytes):
    """Converts bytes into image matrix"""
    return Image.open(io.BytesIO(raw_bytes)).convert('L')


def write_as_image(np_arr):
    """Converts numpy array into png image in bytes string"""
    buf = io.BytesIO()
    Image.fromarray(np_arr, 'L').save(buf, format="PNG")
    return buf
