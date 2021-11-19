import base64
import io
import numpy as np
import requests
from imageio import imsave, imread
from PIL import Image
import PIL
from deepface import DeepFace


def get_img_and_base64(url):
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
    return (img, img64)


def match_photo(mask, person):
    try:
        if DeepFace.verify(np.array(mask), np.array(person), model_name='ArcFace')['verified']:
            back_np = 'Same'

        else:
            back_np = 'Not same'
    except ValueError:
        back_np = 'Face not found'

    # fmem = io.BytesIO()
    # imsave(fmem, back_np, 'png')
    # fmem.seek(0)
    # merged64 = base64.b64encode(fmem.read()).decode('utf-8')
    return back_np
    # patch_under_person[:,:,0][mask_np > 0] = 0
