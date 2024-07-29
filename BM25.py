import math
from collections import Counter


# Hàm tính toán IDF (Inverse Document Frequency)
def compute_idf(corpus):
    N = len(corpus)
    idf = {}
    for document in corpus:
        for word in set(document):
            if word in idf:
                idf[word] += 1
            else:
                idf[word] = 1

    for word, doc_freq in idf.items():
        idf[word] = math.log((N - doc_freq + 0.5) / (doc_freq + 0.5) + 1)

    return idf


# Hàm tính toán điểm BM25 cho một tài liệu
def compute_bm25(doc, query, idf, avgdl, k1=1.5, b=0.75):
    score = 0.0
    doc_len = len(doc)
    doc_counter = Counter(doc)

    for word in query:
        if word in doc_counter:
            tf = doc_counter[word]
            idf_value = idf.get(word, 0)
            score += idf_value * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avgdl))

    return score


# Tiền xử lý tài liệu
def preprocess(text):
    return text.lower().split()


# Dữ liệu mẫu
corpus = [
    "The quick brown fox jumps over the lazy dog",
    "Never jump over the lazy dog quickly",
    "A quick brown dog outpaces a quick fox"
]

# Tiền xử lý tài liệu
preprocessed_corpus = [preprocess(doc) for doc in corpus]

# Tính IDF cho các từ trong tập hợp tài liệu
idf = compute_idf(preprocessed_corpus)

# Tính độ dài trung bình của các tài liệu
avgdl = sum(len(doc) for doc in preprocessed_corpus) / len(preprocessed_corpus)

# Truy vấn tìm kiếm
query = "Never"
preprocessed_query = preprocess(query)

# Tính điểm BM25 cho từng tài liệu
scores = []
for doc in preprocessed_corpus:
    score = compute_bm25(doc, preprocessed_query, idf, avgdl)
    scores.append(score)

# In kết quả
for i, score in enumerate(scores):
    print(f"Document {i}: {score}")
