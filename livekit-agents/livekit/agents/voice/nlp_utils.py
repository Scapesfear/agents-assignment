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

    # 1. Normalize: "Yeah... I see!" -> "yeah i see"
    # Replace punctuation with space to avoid merging words ("yeah.but" -> "yeah but")
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    clean_text = transcript.lower().translate(translator)
    
    # Split into a list of words for robust matching
    words = clean_text.split()
    
    if not words:
        return False

    # 2. Prepare Ignore Phrases (also normalized and split)
    # We sort by length descending so "that makes sense" matches before "that"
    normalized_phrases = []
    for phrase in ignore_list:
        phrase_clean = phrase.lower().translate(translator)
        phrase_words = phrase_clean.split()
        if phrase_words:
            normalized_phrases.append(phrase_words)
    
    normalized_phrases.sort(key=len, reverse=True)

    # 3. Consumption Loop
    # We keep eating valid phrases from the front of the 'words' list
    while words:
        matched = False
        for phrase_tokens in normalized_phrases:
            # Check if the remaining words start with this phrase
            # e.g. words=['i', 'see', 'now'], phrase=['i', 'see'] -> Match!
            phrase_len = len(phrase_tokens)
            
            if words[:phrase_len] == phrase_tokens:
                # Remove the matched phrase from the start
                words = words[phrase_len:]
                matched = True
                break # Restart loop to match next chunk
        
        if not matched:
            # We hit a word that IS NOT in the ignore list (e.g. "wait")
            # This implies "Mixed Input" -> Real Interruption
            return False

    # 4. Success: We consumed everything
    return True