URGENT_KEYWORDS = [
    "immediate safety concern",
    "immediate danger",
    "unsafe",
    "hurt myself",
    "harm myself",
    "suicide",
    "self-harm",
]


AMBIGUOUS_PHRASES = [
    "do not know how much longer",
    "cannot continue",
    "can't continue",
    "cannot go on",
    "can't go on",
    "give up",

    # Ambiguous distress statements
    "everything feels difficult",
    "everything feels unclear",
    "feels difficult and unclear",
]


def contains_urgent_indicator(text: str) -> bool:

    text = text.lower()

    return any(
        keyword in text
        for keyword in URGENT_KEYWORDS
    )


def contains_ambiguous_indicator(text: str) -> bool:

    text = text.lower()

    return any(
        phrase in text
        for phrase in AMBIGUOUS_PHRASES
    )