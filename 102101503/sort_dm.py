#提取弹幕文本
dms = []
for index, cid in enumerate(cids):
    dm_url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
    response = requests.get(dm_url, headers=headers)
    response.encoding = 'utf-8'
    root = ET.fromstring(response.text)
    
    for d in root.iter('d'):
        dm_text = d.text
        dms.append(dm_text)
    
    print(f"正在解析弹幕，现在已进行到 {index+1}/{len(cids)}")
    time.sleep(round(random.uniform(0, 2), 3))

# 统计每个弹幕的出现次数
word_counts = collections.Counter(dms)

# 对弹幕出现次数进行排序
sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

# 输出弹幕数量排名前20的弹幕
print("弹幕数量排名前20的弹幕：")
for i in range(min(20, len(sorted_word_counts))):
    print("{}: {}".format(sorted_word_counts[i][0], sorted_word_counts[i][1]))
# 创建一个空的 DataFrame
df = pd.DataFrame(columns=['弹幕内容', '出现次数'])
# 将弹幕和对应的出现次数添加到 DataFrame 中
for dm, count in sorted_word_counts:
    df = df.append({'弹幕内容': dm, '出现次数': count}, ignore_index=True)
# 将 DataFrame 保存为 Excel 文件
df.to_excel('弹幕统计.xlsx', index=False)
