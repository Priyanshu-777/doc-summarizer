import math
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer



def score_sentences(original_sentences, preprocessed_sentences):
    
    if not preprocessed_sentences or not original_sentences:
        return []

    # Filter out empty preprocessed sentence
    valid_indices = []
    valid_preprocessed = []
    for i, sent in enumerate(preprocessed_sentences):
        if sent.strip():
            valid_indices.append(i)
            valid_preprocessed.append(sent)

    if not valid_preprocessed:
        return []

    #TF-IDF Vectorization
   
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(valid_preprocessed)

    # Convert sparse matrix to dense numpy array for easier manipulation
    tfidf_array = tfidf_matrix.toarray()

 
    scored = []
    for idx, row_idx in enumerate(valid_indices):
        row = tfidf_array[idx]
        non_zero_values = row[row > 0]

        if len(non_zero_values) > 0:
            # Average TF-IDF score = sum of non-zero values / count of non-zero values
            score = float(np.mean(non_zero_values))
        else:
            score = 0.0

        scored.append((row_idx, original_sentences[row_idx], score))

    # Sort by score in descending order (most important sentences first)
    scored.sort(key=lambda x: x[2], reverse=True)

    return scored


def generate_summary(original_sentences, scored_sentences, ratio=0.2):
    
    if not  scored_sentences:
        return "", []

    # Calculate how many sentences to include 
    num_sentences = max(1, math.ceil(len(original_sentences) * ratio))

    # Select the top N highest-scoring sentences
    top_sentences = scored_sentences[:num_sentences]

    # Re-sort by original index to maintain document order
    # This is critical: without this step the summary would read
    # as a random collection of sentences rather than a coherent excerpt.
    top_sentences.sort(key=lambda x:x[0])

    # Build the summary text: mix of paragraphs and bullet points
    sentences = [sent.strip() for _, sent, _ in top_sentences]
    
    if len(sentences) <= 3:
        # If it's a very short summary, just make it a single paragraph
        summary = " ".join(sentences)
    else:
        # Intro paragraph 
        intro = " ".join(sentences[:2])
        
        # Middle sentences as bullet points
        bullets = "\n".join([f"- {s}" for s in sentences[2:-1]])
        
        # Outro paragraph 
        outro = sentences[-1]
        
        summary = f"{intro}\n\n**Key Highlights:**\n{bullets}\n\n{outro}"

    return summary, top_sentences
