import base64
import io
import numpy as np
import requests
from imageio import imsave
from PIL import Image
from deepface import DeepFace


def get_img_and_base64(url: str) -> (Image.Image, str):
    """
    returns image in base64 format (a string)
    that can be passed to html as context and rendered without saving to drive
    """
    blob = io.BytesIO(requests.get(url).content)
    img = Image.open(blob).convert('RGB')
    img_np = np.array(img).astype(np.uint8)
    fmem = io.BytesIO()
    imsave(fmem, img_np, 'png')
    fmem.seek(0)
    img64 = base64.b64encode(fmem.read()).decode('utf-8')
    return img, img64


def match_photo(photo_1: Image.Image, photo_2: Image.Image) -> str:
    try:
        if DeepFace.verify(np.array(photo_1), np.array(photo_2), model_name='ArcFace')['verified']:
            back_np = 'Same'

        else:
            back_np = 'Not same'
    except ValueError:
        back_np = 'Face not found'

    return back_np
