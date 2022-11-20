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



def upload(request):
    form = UploadForm
    model = Upload

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            # Get the latest image file
            list_of_files = glob.glob(location)        
            latest_file = max(list_of_files, key=os.path.getctime)

            # Reading and processing image using openCV
            img = cv2.imread(latest_file)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Extracting the text from the photo
            extracted_data = pytesseract.image_to_string(img)

            # Processing the extracted data to search for active pharmaceutical ingredients
            response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"Find the active pharmaceutical ingredients in the following text and write few lines about each ingredient:\nExample:\n\nPrompt:\nDirections for mixi\n\n1. Tap bottle sen <\n\nALL power :\n\nco OFWATER g\n(oon AUGMENTIN gS\nry often ate powder. AMOXICILLIN/ s 8\npain CLAVULANATE 2 5\n\nis ‘shat i. S\ni. Cawsrenanng er —- POTASSIUM eck\n= (about 44 ml). FOR ORAL SUSPENSION BKB\n\n> Permit When reconstituted, ee\n\n‘VIGOROUSLY. each 5 mL contains: 5 ome\nCO Dosage: See accompanying AMOXICILLIN, 125 MG, Sea\ni=) prescribing information. as the trihydrate sae B\nLO «5 Keep tghlly closed. CLAVULANIC ACID, 31.25 MG, 222 %\nShake well before as clavulanate potassium eos\nI  eashuse. 2e5\n& store reconstituted Bete\n=o 8 meter 150 mL Byes\n5 biscard after 10 days. ea22\nSome color ehange h S225\n‘normal during dosing neopnarma Ssesz\nperiod. id roy 2325\n\nResult:\namoxicillin\nAmoxicillin is an antibiotic that is used to treat bacterial infections. It works by stopping the growth of bacteria. It can be used to treat a wide variety of infections, including bronchitis, pneumonia, and ear infections.\nclavulanic acid\nClavulanic acid is a beta-lactamase inhibitor. It works by binding to beta-lactamase enzymes, thus preventing them from breaking down the beta-lactam ring of antibiotics. This allows the antibiotics to work effectively against bacteria that are otherwise resistant to them.\npotassium clavulanate\nPotassium clavulanate is a beta-lactam drug that is used in combination with other beta-lactam antibiotics to treat certain types of bacterial infections. It works by inhibiting the production of enzymes that are involved in the bacteria's cell wall synthesis.\n\nPrompt:\nNDC 63481-698-70 100 tablets\nEach tablet contains: an CJ\n\noa ., ZyYdone ~~\nAcetaminophen, Ut 00 ma \"\n\nUsual Dosage: See package insert (hydrocodone bitartrate and\n\nor complete prescribing information. acetaminophen tablets, USP)\n\nStore at 25°C (77°F); excursions\npermitted to 15°-20°C (69°-86°F,\n\nDispense in a tight, ight-resistant\ncontainer as defined in the USP, with\nacchild-resistant closure (as required)\n\nVerbal prescription where permitted by\nstate law\n\nManufactured for R, only Il\n\nEndo Pharmaceuticals Inc.\nChadds Ford, PA 19317 _ =o\n\nBy: Novartis, Lincoln, NE 68501 PHARMACEUTICALS.\n\nLot:\nEXP:\n\nResult:\nhydrocodone bitartrate\nHydrocodone bitartrate is an opioid analgesic that is used to relieve pain. It works by binding to the mu-opioid receptor, which is found in the brain and spinal cord. This prevents the transmission of pain signals to the brain.\nacetaminophen\nAcetaminophen is a pain reliever and fever reducer. It works by reducing the production of prostaglandins, which are substances that are involved in pain and inflammation.\n\n##\n\nPrompt:{extracted_data}\n\nResult:\n",
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
            
            # Processing the JSON response to a string
            parsedJSON = response["choices"][0]["text"]
            arrayAnswer = list(parsedJSON.split("\n")) # convert string into a list
            for item in arrayAnswer: # remove empty string elements
                if item == '':
                    arrayAnswer.remove(item)
            
            
            print(arrayAnswer)

            context = {'form': form, 'arrayAnswer': arrayAnswer}
            return render(request, 'base/result.html', context)
    
    context = {'form': form}
    return render(request, 'base/upload.html', context)