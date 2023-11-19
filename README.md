# Cacheing-using-LRU-LFU-strategies-and-Text-Extraction-from-Images
This is a Website that allows for translation using the Google Translate API, while employing the LRU and LFU cacheing while allowing the user to upload images from which they want the text to be tranlated

Here I have given the code for a website using django, the website basically does three things
1) It uses an API for transaltion
2) It employs three different types of cacheing as per the users requirement. I create and empoy the three different tyoes of cacheing
3) It allows for the user to give an image from which test can be extracted and that extracted data can be translated. I employ pytessaract for text extraction

The cache structure is in utils.py in model1 
The API interecation is done in views.py
The pytessearct uasage for text extraction is done in views.py
