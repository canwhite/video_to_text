import re

def split_text_into_sentences(text):
    """
    将中文文本按照句子进行拆分。

    参数:
    text (str): 包含中文文本的字符串。

    返回:
    list: 拆分后的句子列表。
    """
    # 使用正则表达式拆分句子，并忽略标点符号
    sentences = re.split(r'(?<=。|！|？|；|…|”|）|】|》)', text)
    
    # 去除空字符串
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    
    return sentences

# 示例用法
if __name__ == "__main__":
    text = "这是一个关于巴黎和埃菲尔铁塔的长文本。巴黎是法国的首都，以其浪漫的氛围和丰富的文化遗产而闻名。埃菲尔铁塔是巴黎的标志性建筑之一，每年吸引数百万游客。"
    sentences = split_text_into_sentences(text)
    print("Sentences:", sentences)