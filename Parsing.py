from pdf2image import convert_from_path
import easyocr
import numpy as np
from PIL import ImageDraw

reader = easyocr.Reader(['en'])


def draw_boxes(image, bounds, color='yellow', width=2):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    return image


def parsing_pdf():
    images = convert_from_path('Resumes/Annas Furquan Pasha_20011A0503 (3).pdf')
    text = ''
    for i in range(len(images)):
        bounds = reader.readtext(np.array(images[i]), min_size=0, slope_ths=0.2, ycenter_ths=0.7, height_ths=0.6,
                                 width_ths=0.8, decoder='beamsearch', beamWidth=10)
        # draw_boxes(images[i], bounds)
        text = text + bounds[i][1] + '\n'
    print(text)
    return text


parsing_pdf()
