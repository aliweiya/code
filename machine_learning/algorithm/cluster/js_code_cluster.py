import os
import shutil

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import DBSCAN

splitter = [' ', ';', '.', '(', ')', '<', '>', '=',
            '"', '/', '{', '}', '&', ',', ':', '|',
            '?', '[', ']', '+', '!', '\\', '\n', "'",
            '-', '%']


def tokenize(string):
    start = 0
    for index in range(len(string)):
        if string[index] in splitter:
            substring = string[start:index].strip()
            if substring and 2 < len(substring) < 40:
                yield substring
            start = index + 1


def get_tfidf(filenames):
    dataset = []
    for index, filename in enumerate(filenames):
        if index % 100 == 0:
            print(index)
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            data = "".join(f.readlines())

        line = " ".join(tokenize(data))
        dataset.append(line)

    print('transform to tfidf')
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(dataset)

    print('deploy truncatedsvd')
    svd = TruncatedSVD(n_components=100)
    new_X = svd.fit_transform(X)

    # 距离，最少元素个数cd 
    print('deploy dbscan')
    model = DBSCAN(eps=0.2, min_samples=10)
    model.fit(new_X)

    y_hat = model.labels_

    _dict = {}
    for index, filename in enumerate(filenames):
        print(filename, y_hat[index])
        if y_hat[index] not in _dict:
            _dict[y_hat[index]] = []
        _dict[y_hat[index]].append(filename)

    for key, value in sorted(_dict.items(), key=lambda x: len(x[1])):
        print(key, len(value))
        if key == -1:
            continue

        if len(value) > 50:
            
            target_path = os.path.join('cluster', str(key))
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            for filename in value:
                shutil.copy(filename, os.path.join(target_path, os.path.basename(filename)))


def main(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        data = "".join(f.readlines())

    print(' '.join(tokenize(data)))


if __name__ == '__main__':
    base_path = "web"

    try:
        shutil.rmtree('cluster')
    except FileNotFoundError:
        pass
    filenames = []
    for item in os.listdir(base_path):
        filenames.append(os.path.join(base_path, item))

    get_tfidf(filenames)