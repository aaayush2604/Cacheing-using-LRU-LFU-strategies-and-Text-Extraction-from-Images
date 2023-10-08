from django.shortcuts import render
import requests
from django.http import HttpResponse
import googletrans 
from googletrans import Translator
from .utils import DLLNode, LRU_Cache


# Create your views here.
translator=Translator()
language_list=googletrans.LANGUAGES

cache= dict()
main_cache=LRU_Cache(10)
    

def get_translation_lru(text_input,src_lang, dest_lang):
    if text_input in main_cache.map:
        return main_cache.get(text_input)
    else:
        translation=translator.translate(text_input,src=src_lang,dest=dest_lang)
        output=translation.text
        main_cache.set(text_input, output)
        return output


def home(request):
    if(request.method=="POST"):
        text=request.POST["input"]
        source=request.POST["src-lang"]
        destination=request.POST["dest-lang"]
        if text:
            output= get_translation_lru(text,source,destination)
        else:
            output="Input is Empty"
        return render(request,"model1/home.html",{
            "output":output,
            "language_list":list(language_list.items())
        })
    else:
        return render(request,"model1/home.html",{
            "language_list":list(language_list.items())
        })

