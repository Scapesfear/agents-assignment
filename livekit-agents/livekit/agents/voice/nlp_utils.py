import string

def is_backchannel(transcript: str, ignore_list: list[str]) -> bool:
    """
    Determines if a transcript consists ENTIRELY of allowed backchannel phrases.
    
    Algorithm:
    1. Normalize text (remove punctuation, lowercase).
    2. Sort ignore list by length (longest phrases first) to handle "I see" before "I".
    3. Iteratively consume the transcript from left to right.
    4. If we cannot match the start of the remaining text to any ignored phrase, we stop.
    5. If the text is empty at the end, it was a pure backchannel.
    """
    if not transcript or not ignore_list:
        return False

    # Normalization Transcript
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    clean_text = transcript.lower().translate(translator)
    
    words = clean_text.split()
    
    if not words:
        return False

    # Prepare Ignore Phrases (also normalized and split)
    normalized_phrases = []
    for phrase in ignore_list:
        phrase_clean = phrase.lower().translate(translator)
        phrase_words = phrase_clean.split()
        if phrase_words:
            normalized_phrases.append(phrase_words)
    
    normalized_phrases.sort(key=len, reverse=True)

    # Consumption Loop
    while words:
        matched = False
        for phrase_tokens in normalized_phrases:
            phrase_len = len(phrase_tokens)
            
            if words[:phrase_len] == phrase_tokens:
                words = words[phrase_len:]
                matched = True
                break
        
        if not matched:
            return False

    return True