import re
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def normalize_tokens(tokens):
    # Common keywords across Python, C, C++, and Java
    keywords = {
        'for', 'while', 'if', 'else', 'elif', 'print', 'printf', 'scanf',
        'def', 'return', 'in', 'range', 'int', 'float', 'char', 'double',
        'void', 'include', 'import', 'public', 'private', 'class', 'static',
        'struct', 'main', 'using', 'namespace', 'std', 'cout', 'cin'
    }

    normalized = []
    for token in tokens:
        if token in keywords:
            normalized.append(token)
        elif token.isdigit():
            normalized.append('NUM')
        else:
            normalized.append('VAR')
    return normalized

def calculate_similarity(code1, code2):
    # 1. Scikit-learn TF-IDF + Cosine Similarity
    vectorizer = TfidfVectorizer(tokenizer=tokenize, token_pattern=None, stop_words=None)
    try:
        tfidf_matrix = vectorizer.fit_transform([code1, code2])
        sklearn_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except ValueError:
        sklearn_score = 0

    # 2. Text similarity (difflib)
    text_score = SequenceMatcher(None, code1, code2).ratio()

    # 3. Token similarity (difflib)
    tokens1 = normalize_tokens(tokenize(code1))
    tokens2 = normalize_tokens(tokenize(code2))
    token_score = SequenceMatcher(None, tokens1, tokens2).ratio()

    # Weighted average combining all methods
    # Sklearn (0.4) + Token (0.4) + Text (0.2)
    final_score = (0.4 * sklearn_score + 0.4 * token_score + 0.2 * text_score) * 100
    return final_score

def tokenize(code):
    return re.findall(r'\b\w+\b|\S', code)

def highlight_code(code1, code2):
    lines1 = code1.splitlines()
    lines2 = code2.splitlines()

    h1, h2 = [], []

    for line1 in lines1:
        best_match = max(
            (SequenceMatcher(None, line1, line2).ratio() for line2 in lines2),
            default=0
        )

        is_main = re.search(r'\bint\s+main\s*\(', line1)
        is_return = re.search(r'^\s*return\s*0\b', line1)
        is_else = re.search(r'^\s*else\s*:?\s*\{?\s*$', line1)

        if best_match > 0.6 and not is_main and not is_return and not is_else:
            h1.append(f"<mark>{line1}</mark>")
        else:
            h1.append(line1)

    for line2 in lines2:
        best_match = max(
            (SequenceMatcher(None, line2, line1).ratio() for line1 in lines1),
            default=0
        )

        is_main = re.search(r'\bint\s+main\s*\(', line2)
        is_return = re.search(r'^\s*return\s*0\b', line2)
        is_else = re.search(r'^\s*else\s*:?\s*\{?\s*$', line2)

        if best_match > 0.6 and not is_main and not is_return and not is_else:
            h2.append(f"<mark>{line2}</mark>")
        else:
            h2.append(line2)

    return "\n".join(h1), "\n".join(h2)