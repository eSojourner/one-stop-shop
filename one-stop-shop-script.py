print("Loading program. Please wait...\n")

import whisper #for transcribing audio to text
import deepl #for translating text to Spanish
from gtts import gTTS # for performing text to speech narration
from dotenv import load_dotenv # for reading DeepL API key
import os # for reading DeepL API key
import winsound # to play a sound when the program has finished
from datetime import datetime #for indicating how long each phase of the program took

#Generating English Transcript of target file
target_file = input("Please enter target file name for transcription, translation, and narration: ")
print()

# loading whispher model of choice to transcribe target file
print("Transcription in progress...\n")
transcription_start_time = datetime.now() #begin time measurement for transcription 

model = whisper.load_model("turbo")
result = model.transcribe(target_file)


# Saving transcription to a file named "transcription_file"
transcription_file = target_file + "-" + "transcription"

with open (f"{transcription_file}.txt", "w") as output:
    output.write(result["text"])

print(f"Transcription complete. File saved as {transcription_file} \n")

# End time measurement for transcription and print result 
transcription_end_time = datetime.now() 
print(f"Transcription took {transcription_end_time - transcription_start_time} \n")

#Give some breathing room in the terminal and indicate the beginning of translation phase
# using DeepL's free API
print()
print("Translation in progress... \n")
translation_start_time = datetime.now() #begin time measurement for translation 

# Load environmental variable from .env file
load_dotenv()

# Retrieve API key and give that to the deepl_client
api_key = os.getenv("DEEPL_API_KEY")
if not api_key:
    raise ValueError ("DEEPL_API_KEY not found in environmental variables")

deepl_client = deepl.DeepLClient(api_key)

# Specifying the document to be translated (input_path) and what the name will be
# of the file once it is translated (output_path)
input_path = transcription_file + ".txt"
output_path = target_file + "-" + "translated" + ".txt"

with open(input_path, "rb") as in_file, open(output_path, "wb") as out_file:
        deepl_client.translate_document(
            in_file,
            out_file,
            target_lang="ES",
            formality="more"
        )

print(f"Translation complete. File saved as {output_path} \n")

# End time measurement for translation and print result 
translation_end_time = datetime.now()  
print(f"Translation took {translation_end_time - translation_start_time} \n") 


#Giving some breathing room in the terminal and indicating the beginning of narration phase
print()

print("Narration in progress...\n")

# Begin time measurement for narration
narration_start_time = datetime.now()  

# Perform Spanish text to speech narration using Google Text To Speech Endpoint 
# Bringing in the translated file from the previous stage (output_path) to narrate it
with open(output_path,"r", encoding = "utf-8") as file:
    target = file.read()

# narrate the file that is written in Spanish ("es") and narrate it with a Mexican Spanish 
# accent ("tld="com.mx"") 
tts = gTTS(target, lang="es",tld="com.mx")

# create a name for the narrated file and save it 
narrated_file = target_file + "-"+ "narrated" + ".mp3"

tts.save(narrated_file)

# Indicate end of the final phase of the program and beep to let the user know the program 
# has finished
print(f"Narration complete. File saved as {narrated_file} \n")
winsound.MessageBeep()
winsound.MessageBeep()

# End time measurement for translation and print result 
narration_end_time = datetime.now()  
print(f"Narration took {narration_end_time - narration_start_time} \n") 
