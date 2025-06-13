from modeltranslation.translator import translator, TranslationOptions
from .models import Addmoney_info, UserProfile

class AddmoneyInfoTranslationOptions(TranslationOptions):
    fields = ('add_money', 'Category',)

class UserProfileTranslationOptions(TranslationOptions):
    fields = ('profession',)

translator.register(Addmoney_info, AddmoneyInfoTranslationOptions)
translator.register(UserProfile, UserProfileTranslationOptions)