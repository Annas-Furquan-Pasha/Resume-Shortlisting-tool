from pdf2image import convert_from_path, convert_from_bytes
import easyocr
import numpy as np
from PIL import ImageDraw

reader = easyocr.Reader(['en'])


# def draw_boxes(image, bounds, color='yellow', width=2):
#     draw = ImageDraw.Draw(image)
#     for bound in bounds:
#         p0, p1, p2, p3 = bound[0]
#         draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
#     return image


def parsing_pdf(file):
    images = convert_from_bytes(file.read(), poppler_path=r"C:\Users\annas\Downloads\poppler-24.02.0\Library\bin")
    text = ''
    for i in range(len(images)):
        bounds = reader.readtext(np.array(images[i]), min_size=0, slope_ths=0.2, ycenter_ths=0.7, height_ths=0.6,
                                 width_ths=0.8, decoder='beamsearch', beamWidth=10)
        print(bounds)
        # draw_boxes(images[i], bounds)
        for j in range(len(bounds)):
            text = text + bounds[j][1] + '\n'
    print(text)
    return text

# parsing_pdf()