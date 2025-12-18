import whisper #for transcribing audio to text
import deepl #for translating text to Spanish
from gtts import gTTS # for performing text to speech narration
from dotenv import load_dotenv # for reading DeepL API key
import os # for reading DeepL API key

#Generating English Transcript of target file
target_file = input("Please enter target file name for transcription: ")
print()

# loading whispher model to transcribe target file 
model = whisper.load_model("turbo")
print("Transcription in progress...\n")
result = model.transcribe(target_file)

# saving transcription to a file named "transcription_file"
transcription_file = target_file + "-" + "transcription"

with open (f"{transcription_file}.txt", "w") as output:
    output.write(result["text"])

print(f"Transcription complete. File saved as {transcription_file}")

#Giving some breathing room in the terminal and indicating the beginning of translation phase
# using DeepL's free API
print()
print("Translation in progress... \n")

# Load environmental variable from .env file
load_dotenv()

# Retrieve API key and give that to the deepl_client
api_key = os.getenv("DEEPL_API_KEY")
if not api_key:
    raise ValueError ("DEEPL_API_KEY not found in environmental variables")

deepl_client = deepl.DeepLClient(api_key)

# Specifying the document to be translated (input_path) and what the name will be
# of the file once it has been translated (output_path)
input_path = transcription_file + ".txt"
output_path = target_file + "-" + "translated" + ".txt"

with open(input_path, "rb") as in_file, open(output_path, "wb") as out_file:
        deepl_client.translate_document(
            in_file,
            out_file,
            target_lang="ES",
            formality="more"
        )

print(f"Translation complete. File saved as {output_path}")

#Giving some breathing room in the terminal and indicating the beginning of narration phase
print()

print("Narration in progress...\n")

# Perform Spanish text to speech narration using Google Text To Speech library (gTTS) 
# Bringing in the translated file from the previous stage (output_path) to narrate it
with open(output_path,"r", encoding = "utf-8") as file:
    target = file.read()

# Narrate the file that is written in Spanish ("es") and narrate it with a Mexican Spanish 
# accent ("tld="com.mx"") 
tts = gTTS(target, lang="es",tld="com.mx")

# create a name for the narrated file and save it 
narrated_file = target_file + "-"+ "narrated" + ".mp3"

tts.save(narrated_file)

# Indicate end of the final phase of the program 
print(f"Narration complete. File saved as {narrated_file}")
