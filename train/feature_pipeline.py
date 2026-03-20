import re


def tokenize(text):
    return [token for token in re.findall(r"[A-Za-z]+", text.lower()) if token]


def build_feature_row(record, config):
    feature_config = config.get("features", {})
    boost_terms = set(feature_config.get("keyword_boost_terms", []))
    venue_bias = feature_config.get("venue_bias", {})

    title = record.get("title", "")
    abstract = record.get("abstract", "")
    venue = record.get("venue", "ArXiv")
    label = int(record.get("label", "0"))

    title_tokens = tokenize(title)
    abstract_tokens = tokenize(abstract)
    tokens = title_tokens + abstract_tokens
    keyword_hits = sum(1 for token in tokens if token in boost_terms)
    long_context = 1 if len(abstract_tokens) >= 14 else 0
    venue_score = float(venue_bias.get(venue, 0.0))
    length_score = float(len(tokens)) / 40.0

    return {
        "paper_id": record.get("paper_id", ""),
        "label": label,
        "token_count": len(tokens),
        "keyword_hits": keyword_hits,
        "long_context": long_context,
        "venue_score": venue_score,
        "length_score": length_score,
    }


def build_split_features(records, config):
    return [build_feature_row(record, config) for record in records]


def summarize_split(feature_rows):
    total = len(feature_rows)
    if total == 0:
        return {
            "samples": 0,
            "positive_ratio": 0.0,
            "avg_token_count": 0.0,
            "avg_keyword_hits": 0.0,
            "avg_venue_score": 0.0,
            "long_context_ratio": 0.0,
        }

    positive_count = sum(row["label"] for row in feature_rows)
    return {
        "samples": total,
        "positive_ratio": float(positive_count) / total,
        "avg_token_count": sum(row["token_count"] for row in feature_rows) / float(total),
        "avg_keyword_hits": sum(row["keyword_hits"] for row in feature_rows) / float(total),
        "avg_venue_score": sum(row["venue_score"] for row in feature_rows) / float(total),
        "long_context_ratio": sum(row["long_context"] for row in feature_rows) / float(total),
    }
