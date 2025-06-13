from django.utils import translation
from django.conf import settings
from django.utils.translation import gettext as _

def language_context(request):
    """
    Add language-related context variables to the context.
    This ensures that LANGUAGE_CODE is always available in templates.
    """
    current_language = translation.get_language()
    return {
        'LANGUAGE_CODE': current_language,
        'LANGUAGES': getattr(settings, 'LANGUAGES', []),
        'TRANSLATE_WORD_BY_WORD': True,  # Enable word-by-word translation
    }