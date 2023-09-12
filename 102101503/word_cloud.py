import pandas as pd
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# 读取Excel表格数据
data = pd.read_excel('弹幕统计.xlsx')

# 将数据转换为字典形式 {词: 出现次数}
word_freq = dict(zip(data['弹幕内容'], data['出现次数']))
# 打开图像文件并将其转化为numpy数组
mask = np.array(Image.open('yourpicture.jpg'))
# 创建WordCloud对象并配置参数
wordcloud = WordCloud(width=3000, height=2800, background_color='white',
                      font_path='yourtypeface.ttf',max_words=10000,
                      stopwords=set(STOPWORDS),mask=mask)

# 过滤停用词
stopwords = set(['的', '是', '在'])  # 自定义停用词列表
wordcloud.stopwords.update(stopwords)  # 添加停用词
# 根据出现次数设置字体大小
min_font_size = 20
max_font_size = 200
# 计算字体大小的动态范围
max_count = max(word_freq.values())
wordcloud.generate_from_frequencies(word_freq, max_font_size=max_font_size)
wordcloud.recolor(random_state=1000)

# 绘制词云图并展示
plt.figure(figsize=(5, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
