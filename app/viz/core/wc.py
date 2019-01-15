from django.conf import settings
import os
import re
import numpy as np
from konlpy.tag import Mecab
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image

__all__ = [
    'make_wc_png',
]


def make_wc_png(data, max_word_size=100, bg_color='white', mask=None, mask_coloring=True, font=None, sw=None):
    """Make and Save wc image file (``/.viz_raw/wc.png``)

    :param str data:
    :param int max_word_size:
    :param str bg_color:
    :param django.core.files.uploadedfile.TemporaryUploadedFile mask:
    :param bool mask_coloring:
    :param django.core.files.uploadedfile.TemporaryUploadedFile font:
    :param str sw: Stopwords separated ','
    :return: none

    """
    data = re.sub(r'\W', ' ', data)  # Use regular expression for data scailing
    
    nlp = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')  # Make Mecab(NLP) object
    
    data_nouns = nlp.nouns(data)  # Extract nouns from data and input it to data_nouns
    data_nouns_cnt = Counter(data_nouns)  # Count nouns from data_nouns and make it dict type data

    # Stop Words Process
    if sw:
        sw = sw.replace(' ', '')
        sw_list = sw.split(',')
        for word in sw_list:
            del data_nouns_cnt[word]

    # Set Font
    wc_font = os.path.join(settings.ROOT_DIR, 'extension/fonts/DOSGothic.ttf')
    if font:
        wc_font = font.temporary_file_path()

    # Set Image Mask
    wc_mask = np.array(Image.open(os.path.join(settings.ROOT_DIR, 'extension/wc_mask/default.png')))
    if mask:
        wc_mask = np.array(Image.open(mask))

    wc = WordCloud(max_font_size=max_word_size,
                   font_path=wc_font,
                   background_color=bg_color,
                   mask=wc_mask,
                   ).generate_from_frequencies(data_nouns_cnt)

    if mask_coloring:
        mask_colors = ImageColorGenerator(wc_mask)
        plt.figure(figsize=(40, 20), dpi=55)
        plt.imshow(wc.recolor(color_func=mask_colors), interpolation="bilinear")
    else:
        plt.figure(figsize=(40, 20), dpi=55)
        plt.imshow(wc, interpolation="bilinear")

    plt.axis('off')
    plt.savefig(os.path.join(settings.ROOT_DIR, '.viz_raw/wc.png'), bbox_inches='tight')
    plt.close()
