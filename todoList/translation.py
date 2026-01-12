from modeltranslation.translator import register, TranslationOptions, translator
#from modeltranslation import translator
from .models import TODO

#@register(TODO)
class TODOTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

translator.register(TODO, TODOTranslationOptions)
