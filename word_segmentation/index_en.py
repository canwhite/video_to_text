import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from sklearn.feature_extraction.text import TfidfVectorizer
# import requests

# 文本预处理
def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalnum()]
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if not word in stop_words]
    tagged = pos_tag(tokens)
    entities = ne_chunk(tagged)
    return tokens, tagged, entities

# 关键词提取
def extract_keywords(text):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]
    keywords = [(feature_names[i], tfidf_scores[i]) for i in range(len(feature_names))]
    keywords.sort(key=lambda x: x[1], reverse=True)
    return keywords

# 生成图片（示例使用Unsplash API）
# def generate_image(keyword):
#     url = "https://api.unsplash.com/photos/random"
#     params = {
#         "query": keyword,
#         "client_id": "YOUR_UNSPLASH_API_KEY"
#     }
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         image_url = data['urls']['regular']
#         return image_url
#     else:
#         return None

# 主函数
def main():
    text = "这是一个关于巴黎和埃菲尔铁塔的长文本。巴黎是法国的首都，以其浪漫的氛围和丰富的文化遗产而闻名。埃菲尔铁塔是巴黎的标志性建筑之一，每年吸引数百万游客。"
    
    tokens, tagged, entities = preprocess_text(text)
    keywords = extract_keywords(text)
    
    print("Tokens:", tokens)
    print("Tagged:", tagged)
    print("Entities:", entities)
    print("Keywords:", keywords)
    
    for keyword, score in keywords[:5]:
        print(keyword)
        # image_url = generate_image(keyword)
        # if image_url:
        #     print(f"Keyword: {keyword}, Image URL: {image_url}")

if __name__ == "__main__":
    main()