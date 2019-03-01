from django.conf import settings
import os
import re
import numpy as np
from konlpy.tag import Mecab
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image

__all__ = [
    'gen_wc_png',
]


def gen_wc_png(
        data,
        max_word_size=100,
        word_len_min=1,
        bg_color='white',
        mask=None, mask_coloring=True, font=None, stopwords=None
):
    """Generate wc png file

    :param str data:
    :param int max_word_size:
    :param int word_len_min:
    :param str bg_color:
    :param django.core.files.uploadedfile.TemporaryUploadedFile mask:
    :param bool mask_coloring:
    :param django.core.files.uploadedfile.TemporaryUploadedFile font:
    :param str stopwords: Stopwords separated ','
    :return: none

    """
    nlp = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')  # Make Mecab(NLP) object
    data = re.sub(r'\W', ' ', data)  # Change Special Characters and blanks (Not words) to ' '(one blank)
    data_nouns = nlp.nouns(data)  # Extract nouns from data

    # -- Make Stop Word List -- #
    if stopwords:
        stopwords = stopwords.replace(' ', '')
        stopwords = stopwords.split(',')

    term_vectorizer = CountVectorizer(
        min_df=1,  # Frequency >= 1
        token_pattern=r'\w{%d,}' % word_len_min,
        stop_words=stopwords,
    )
    td_matrix = term_vectorizer.fit_transform(data_nouns)  # Get Term-Document Matrix
    term_names = term_vectorizer.fit(data_nouns).get_feature_names()
    tf_sum = td_matrix.toarray().sum(axis=0)
    tf_sum_dict = {}
    for i in range(len(term_names)):
        tf_sum_dict[term_names[i]] = tf_sum[i]

    # Set Font
    if font: wc_font = font.temporary_file_path()
    else: wc_font = os.path.join(settings.ROOT_DIR, 'extension/fonts/DOSGothic.ttf')

    # Set Image Mask
    if mask: wc_mask = np.array(Image.open(mask))
    else: wc_mask = np.array(Image.open(os.path.join(settings.ROOT_DIR, 'extension/wc_mask/default.png')))

    wc = WordCloud(
        max_font_size=max_word_size,
        background_color=bg_color,
        font_path=wc_font,
        mask=wc_mask,
    ).generate_from_frequencies(tf_sum_dict)

    if mask_coloring:
        mask_colors = ImageColorGenerator(wc_mask)
        plt.figure(figsize=(40, 20), dpi=55)
        plt.imshow(wc.recolor(color_func=mask_colors), interpolation="bilinear")
    else:
        plt.figure(figsize=(40, 20), dpi=55)
        plt.imshow(wc, interpolation="bilinear")

    plt.axis('off')

    if not os.path.exists(settings.VIZ_DIR):
        os.makedirs(settings.VIZ_DIR, exist_ok=True)
    plt.savefig(os.path.join(settings.VIZ_DIR, 'wc.png'), bbox_inches='tight')
    plt.close()
