from django import template
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def translate_words(value):
    """
    Translate each word in a string individually.
    Usage: {{ "Hello world"|translate_words }}
    """
    if not value:
        return value
    
    # Convert to string if not already
    text = str(value)
    
    # Split by whitespace and translate each word
    words = text.split()
    translated_words = []
    
    for word in words:
        # Extract punctuation at the beginning and end of the word
        prefix_punct = ""
        suffix_punct = ""
        
        prefix_match = re.match(r'^([^\w]*)(.*)', word)
        if prefix_match:
            prefix_punct = prefix_match.group(1)
            word = prefix_match.group(2)
            
        suffix_match = re.match(r'(.*?)([^\w]*)$', word)
        if suffix_match:
            word = suffix_match.group(1)
            suffix_punct = suffix_match.group(2)
        
        # Translate the word if it's not empty
        if word:
            translated_word = _(word)
            translated_words.append(f"{prefix_punct}{translated_word}{suffix_punct}")
        else:
            translated_words.append(f"{prefix_punct}{suffix_punct}")
    
    # Join the translated words back together
    result = " ".join(translated_words)
    return mark_safe(result)

@register.filter
def wrap_words(value):
    """
    Wrap each word in a span for word-by-word translation.
    Usage: {{ "Hello world"|wrap_words }}
    """
    if not value:
        return value
    
    # Convert to string if not already
    text = str(value)
    
    # Split by whitespace and wrap each word
    words = text.split()
    wrapped_words = []
    
    for word in words:
        # Extract punctuation at the beginning and end of the word
        prefix_punct = ""
        suffix_punct = ""
        
        prefix_match = re.match(r'^([^\w]*)(.*)', word)
        if prefix_match:
            prefix_punct = prefix_match.group(1)
            word = prefix_match.group(2)
            
        suffix_match = re.match(r'(.*?)([^\w]*)$', word)
        if suffix_match:
            word = suffix_match.group(1)
            suffix_punct = suffix_match.group(2)
        
        # Wrap the word if it's not empty
        if word:
            wrapped_word = f'<span class="translated-word" data-original="{word}">{prefix_punct}{_(word)}{suffix_punct}</span>'
            wrapped_words.append(wrapped_word)
        else:
            wrapped_words.append(f"{prefix_punct}{suffix_punct}")
    
    # Join the wrapped words back together
    result = " ".join(wrapped_words)
    return mark_safe(result)