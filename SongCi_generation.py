import json
import random
def load_Ci_title_format():
    # 读取词牌名和格式
    with open('./data/Ci_title_format.json', 'r', encoding='utf-8') as f:
        title_format = json.load(f)

    return title_format


def load_Ci_ngram_model():
    # 读取宋词的2gram模型(json文件)
    with open('./data/Ci_2_gram.json', 'r', encoding='utf-8') as f:
        songci_2_grams = json.load(f)
    songci_2_grams = sorted(list(songci_2_grams.items()), key=lambda x: x[1], reverse=True)

    # n_gram文章开始列表 n_gram文章结束列表 n_gram文章中间列表
    start_Ci_2_grams = [ngram for ngram in songci_2_grams if '<BOS>' in ngram[0]]
    end_Ci_2_grams = [ngram for ngram in songci_2_grams if '<EOS>' in ngram[0]]
    middle_Ci_2_grams = [ngram for ngram in songci_2_grams if '<BOS>' not in ngram[0] and '<EOS>' not in ngram[0]]

    return start_Ci_2_grams, end_Ci_2_grams, middle_Ci_2_grams, load_Ci_title_format()

# 带权重的n_gram生成
def generate_Sentence_with_weights(start_2_grams, end_2_grams, middle_2_grams, sentence_format, n = 2):
    weights = [int(ngram[1]) for ngram in start_2_grams]
    # 句子的第一个字
    generated_text = random.choices(start_2_grams, weights = weights)[0][0][5:] 
    
    # 句子中间的部分
    while len(generated_text)+1 < sentence_format:
        possible_next_ngrams = [ngram for ngram in middle_2_grams if generated_text[-n+1:] == ngram[0][:n-1]]
        if not possible_next_ngrams: # 如果找不到可能的下一个n-gram，则随机选择一个n-gram
            weights = [int(ngram[1]) for ngram in middle_2_grams]
            next_ngram = random.choices(middle_2_grams, weights = weights)
        else:
            weights = [int(ngram[1]) for ngram in possible_next_ngrams]
            next_ngram = random.choices(possible_next_ngrams, weights = weights)
        generated_text+=next_ngram[0][0][-1]
 
    # 句子的最后一个字 
    end_2_grams_no_weight = ''.join([ngram[0][0] for ngram in end_2_grams])
    possible_next_ngrams = [ngram for ngram in middle_2_grams if generated_text[-n+1:] == ngram[0
                                                            ][:n-1] and ngram[0][1:] in end_2_grams_no_weight]
    if not possible_next_ngrams: # 如果找不到可能的下一个n-gram，则随机选择一个n-gram
        weights = [int(ngram[1]) for ngram in end_2_grams]
        next_ngram = random.choices(end_2_grams, weights = weights)
    else:
        weights = [int(ngram[1]) for ngram in possible_next_ngrams]
        next_ngram = random.choices(possible_next_ngrams, weights = weights)
    generated_text+=next_ngram[0][0][-1]

    return generated_text
 
# 不带权重的n_gram生成

def generate_sentence(start_2_grams, end_2_grams, middle_2_grams, sentence_format, n = 2):
    # 句子的第一个字
    generated_text = random.choices(start_2_grams)[0][0][5:] 
    
    # 句子中间的部分
    while len(generated_text)+1 < sentence_format:
        possible_next_ngrams = [ngram for ngram in middle_2_grams if generated_text[-n+1:] == ngram[0][:n-1]]
        if not possible_next_ngrams: # 如果找不到可能的下一个n-gram，则随机选择一个n-gram
            next_ngram = random.choices(middle_2_grams)
        else:
            next_ngram = random.choices(possible_next_ngrams)
        generated_text+=next_ngram[0][0][-1]
 
    # 句子的最后一个字 
    end_2_grams_no_weight = ''.join([ngram[0][0] for ngram in end_2_grams])
    possible_next_ngrams = [ngram for ngram in middle_2_grams if generated_text[-n+1:] == ngram[0
                                                            ][:n-1] and ngram[0][1:] in end_2_grams_no_weight]
    if not possible_next_ngrams: # 如果找不到可能的下一个n-gram，则随机选择一个n-gram
        next_ngram = random.choices(end_2_grams)
    else:
        next_ngram = random.choices(possible_next_ngrams)
    generated_text+=next_ngram[0][0][-1]

    return generated_text

# 接口实现

def generate_SongCi(title, use_weights = True):
    start_Ci_2_grams, end_Ci_2_grams, middle_Ci_2_grams, title_format = load_Ci_ngram_model()  
    SongCi = ''
    # 遍历词格式
    for sentence_format in title_format[title]:
        # 生成一句话
        if use_weights:
            sentence = generate_Sentence_with_weights(start_Ci_2_grams, end_Ci_2_grams, middle_Ci_2_grams, int(sentence_format))
        else:
            sentence = generate_sentence(start_Ci_2_grams, end_Ci_2_grams, middle_Ci_2_grams, int(sentence_format))
        # 将生成的句子加入到总文章中
        SongCi += ' '+sentence

    # 返回生成文章  
    return SongCi      
        
