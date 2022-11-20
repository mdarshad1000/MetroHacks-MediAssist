# Importing dependencies
from django.shortcuts import render
from .forms import UploadForm
from django.contrib import messages
from .models import Upload

import openai
import os
import glob
import pytesseract
import cv2
from dotenv import load_dotenv

# Load API key and location path from .env file
load_dotenv()

# set openai api key
openai.api_key = os.getenv("OPENAI_API_KEY")
location = os.getenv("location")

# Create your views here.
def home(request):

    # If question asked to Chatbot
    if request.GET.get('question') != None:
        question = request.GET.get('question')
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"Answer the following question:\n{question}",
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        final_answer = response["choices"][0]["text"]
        context = {'final_answer':final_answer}
        return render(request, 'base/home.html', context)
    else:
        return render(request, 'base/home.html')
