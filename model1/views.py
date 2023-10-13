from django.shortcuts import render
import requests
from django.http import HttpResponse, HttpResponseRedirect
import googletrans 
from django.urls import reverse
from googletrans import Translator
from .utils import DLLNode, LRU_Cache, LFU_Cache
import os 
import pytesseract
import cv2
from PIL import Image
from pytesseract import Output
import googletrans 
from googletrans import Translator
import json




# Create your views here.
translator=Translator()
language_list=googletrans.LANGUAGES
cache= dict()
main_cache_lru=LRU_Cache(10)
main_cache_lfu=LFU_Cache(10)
    

def get_translation_lru(text_input,src_lang, dest_lang):
    if text_input in main_cache_lru.map:
        return main_cache_lru.get(text_input)
    else:
        translation=translator.translate(text_input,src=src_lang,dest=dest_lang)
        output=translation.text
        main_cache_lru.set(text_input, output)
        return output
    
def get_translation_lfu(text_input,src_lang,dest_lang):
    if text_input in main_cache_lfu.map:
        return main_cache_lfu.get(text_input)
    else:
        transaltion=translator.translate(text_input,src=src_lang,dest=dest_lang)
        output=transaltion.text
        main_cache_lfu.set(text_input,output)
        return output
    


def home(request):
    if(request.method=="POST"):
        text=request.POST["input"]
        source=request.POST["src-lang"]
        destination=request.POST["dest-lang"]
        if text:
            output= get_translation_lfu(text,source,destination)
        else:
            output="Input is Empty"

        request.session['output']=output
        return HttpResponseRedirect(reverse('output'))
    else:
        return render(request,"model1/home.html",{
            "language_list":list(language_list.items())
        })


def output(request):
    return render(request, "model1/output.html", {
        "output_final":request.session['output']
    })

def give_img(request):
    if(request.method=="POST"):
        uploaded_file=request.FILES['file']

        if uploaded_file:
            # Define the path where you want to save the uploaded file
            upload_path = os.path.join(r'D:/Naa Hi Pucho toh Behatr/Web/Practice/Cacheing-using-LRU-LFU-strategies-and-Text-Extraction-from-Images', uploaded_file.name)

            with open(upload_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            img=cv2.imread(upload_path)
            pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            myconfig="--psm 6 --oem 3"
            text=pytesseract.image_to_string(pil_image, config=myconfig)
            if text:
                output=get_translation_lru(text,'en','es')
            else:
                output="No text detected in Image"
            # Redirect or render a success page
            request.session['output']=output
            return HttpResponseRedirect(reverse('output'))
            

    return render(request,"model1/give_img.html")

