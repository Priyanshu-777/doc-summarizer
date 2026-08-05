
from src.preprocessing import tokenize_sentences, tokenize_words


def compute_statistics(original_text, summary_text, num_pages):

   
    original_words = len(tokenize_words(original_text))
    summary_words = len(tokenize_words(summary_text))
    original_sentences = len(tokenize_sentences(original_text))
    summary_sentences = len(tokenize_sentences(summary_text))

    # Compression ratio = how much text was removed
    if original_words > 0:
        compression_ratio = round((1 - summary_words / original_words) * 100, 1)
    else:
        compression_ratio = 0.0

    return {
        "num_pages": num_pages,
        "original_words": original_words,
        "summary_words": summary_words,
        "original_sentences": original_sentences,
        "summary_sentences": summary_sentences,
        "compression_ratio": compression_ratio,
    }


def create_download_text(summary, stats=None):
    
    lines = []
    lines.append("=" * 60)
    lines.append("        AI PDF SUMMARIZER — Generated Summary")
    lines.append("=" * 60)
    lines.append("")

    if stats:
        lines.append(f"Original Document: {stats['original_words']} words, "
                      f"{stats['num_pages']} pages")
        lines.append(f"Summary: {stats['summary_words']} words")
        lines.append(f"Compression: {stats['compression_ratio']}%")
        lines.append("")
        lines.append("-" * 60)
        lines.append("")

    lines.append(summary)
    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)
