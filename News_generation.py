import json
import random

# 读取新闻的2gram模型
def load_news_ngram_model():
   with open('./data/news_2_gram.json', 'r', encoding='utf-8') as f:
      news_2_gram = json.load(f)
   news_2_gram = sorted(list(news_2_gram.items()), key=lambda x: x[1], reverse=True)
    
   # n_gram文章开始列表 n_gram文章结束列表 n_gram文章中间列表
   start_2_grams = [ngram for ngram in news_2_gram if '<BOS>' in ngram[0]]
   end_2_grams = [ngram for ngram in news_2_gram if '<EOS>' in ngram[0]]
   middle_2_grams = [ngram for ngram in news_2_gram if '<BOS>' not in ngram[0] and '<EOS>' not in ngram[0]]
   return start_2_grams, end_2_grams, middle_2_grams

def get_next_token(n_grams, generated_text, n, use_weights = True):

    if use_weights:

        possible_next_ngrams = [ngram for ngram in n_grams if generated_text[-n+1:] == ngram[0][:n-1]]
        if not possible_next_ngrams: # 如果找不到可能的下一个n-gram，则随机选择一个n-gram
            weights = [int(ngram[1]) for ngram in n_grams]
            next_ngram = random.choices(n_grams, weights = weights)[0]
        else:
            weights = [int(ngram[1]) for ngram in possible_next_ngrams]
            next_ngram = random.choices(possible_next_ngrams, weights = weights)[0]
    else:

        possible_next_ngrams = [ngram for ngram in n_grams if generated_text[-n+1:] == ngram[0][:n-1]]
        if not possible_next_ngrams: # 如果找不到可能的下一个n-gram，则随机选择一个n-gram
            next_ngram = random.choices(n_grams)[0]
        else:
            next_ngram = random.choices(possible_next_ngrams)[0]

    return next_ngram[0].split(',')[-1]


# 带权重的n_gram生成
def generate_news(text_length, n = 2, use_weights = True):
    start_2_grams, end_2_grams, middle_2_grams = load_news_ngram_model()

    # 文章的第一个字
    weights = [int(ngram[1]) for ngram in start_2_grams]
    generated_text = random.choices(start_2_grams, weights = weights)[0][0].split(',')[1]
    
    # 文章剩余部分
    while True:
        if len(generated_text) < text_length[0]:
            generated_text += get_next_token(middle_2_grams, generated_text, n, use_weights)
        else:
            generated_text += get_next_token(middle_2_grams+end_2_grams, generated_text, n, use_weights)
            if len(generated_text) > text_length[1]:
                generated_text = generated_text[:int(text_length[1]/3)]
                middle_2_grams = middle_2_grams[:int(len(middle_2_grams)/4)]
                end_2_grams = end_2_grams+end_2_grams
            elif '<EOS>' in generated_text:
                break

    return generated_text.replace('<EOS>', '')
