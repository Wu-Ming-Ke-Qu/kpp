import os
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def word_cloud(tar_path, *text):
    #函数功能，为text list生成词云，存放到tar_path
    #tar_path为生成图片存放地址，格式为xx/xx/xx.png

    # 设置中文字体
    font_path = 'static/fonts/simhei.ttf'

    # stopword
    stopword_path = 'comment/stopwords.txt'

    # 读入 stopword
    with open(stopword_path,encoding='UTF-8') as f_stop:
        f_stop_text = f_stop.read()
        f_stop_seg_list = f_stop_text.splitlines()

    # 中文分词
    text = ";".join(text)
    seg_list = jieba.cut(text, cut_all=False)
    # 把文本中的stopword剃掉
    my_word_list = []

    for my_word in seg_list:
        if len(my_word.strip()) > 1 and not (my_word.strip() in f_stop_seg_list):
            my_word_list.append(my_word)

    my_word_str = ' '.join(my_word_list)

    # 生成词云
    wc = WordCloud(
        font_path=font_path,
        background_color="white",
        random_state=42,
        width=1000,
        height=1000,
    )
    wc.generate(my_word_str)

    # 生成图片
    wc.to_file(tar_path)