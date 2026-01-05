print()
print("Loading program. Please wait...\n")

# Required Libraries
import whisper #for transcribing audio to text
from ollama import generate # to translate each of the different sections of the audio
from gtts import gTTS # for performing text to speech narration
import winsound # to play a sound when the program has finished various steps 
from datetime import datetime #for indicating how long each phase of the program took

# Functions
def transcription():
    """Generates English Transcription of target_file"""

    # begin clock and load whispher model of choice to transcribe target file
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

    return transcription_file

def translation(file_to_be_translated):
    '''Translate the file_to_be_translated into target language'''
    #Give some breathing room in the terminal and indicate the beginning of translation phase
    # using Ollama gemma2 locally 
    print()
    print("Translation in progress... \n")
    translation_start_time = datetime.now() #begin time measurement for translation 

    file_to_be_translated = transcription_file

    # open transcript and split all words on spaces and add them to a temporary list    
    with open(f"{transcription_file}.txt",'r') as file:
        text = file.read()
        temp_list = text.split()

    # all of the different lists and parameters required for splitting the document into 
    # 500 word chunks. They need to be in smaller chunks for the AI to translate them locally
    sections = []
    current_section = []
    translated_sections = []
    section_word_count = 0
    max_words_per_section = 500

    # splitting the document into max_words_per_section word chunks
    for each in temp_list: 
        if section_word_count < max_words_per_section: 
            current_section.append(each)
            section_word_count = section_word_count + 1

        if section_word_count >= max_words_per_section:
            sections.append(current_section)
            current_section = []
            section_word_count = 0

    # in case the translated text is less than the max_words_per_section
    if len(sections) == 0:
        sections.append(current_section)


    # ask the AI to translate each max_words_per_section word chunk into target language
    progress_tracker = 1

    for each in sections:
        print(f"Translating section {progress_tracker} out of {len(sections)}")
        file = ' '.join(each)
        translate = generate("gemma2",f"translate the following text into Spanish without any summarization or overview:{file}")
        translated_sections.append(translate["response"])
        progress_tracker = progress_tracker + 1

    # set name for translated file and save the output from the loop above to a .txt file
    translation_file = target_file + "-"+ "translation"

    with open(f"{translation_file}.txt","w") as output:
        for each in translated_sections:
            output.write(str(each))

    print(f"Translation complete. File saved as {translation_file} \n")

    # End time measurement for translation and print result 
    translation_end_time = datetime.now()  
    print(f"Translation took {translation_end_time - translation_start_time} \n") 

    # Encourage the review of translation
    winsound.MessageBeep()
    print(f"Please review {translation_file} and check for any errors.\n")
    resume_program = input("Once finished, please type yes: ")

    return translation_file

def narration(file_to_be_narrated):
        '''Narrates file using Google's Text to Speech endpoint'''
    #Giving some breathing room in the terminal and indicating the beginning of narration phase
    print()
    print("Narration in progress...\n")

    # Begin time measurement for narration
    narration_start_time = datetime.now()  

    # Perform Spanish text to speech narration using Google Text To Speech Endpoint 
    # Bringing in the translated file from the previous stage to narrate it
    file_to_be_narrated = translation_file

    with open(f"{translation_file}.txt","r") as file:
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

    # End time measurement for translation and print result 
    narration_end_time = datetime.now()  
    print(f"Narration took {narration_end_time - narration_start_time} \n") 

# Program Descriptions
program_modes = {1:"Full program: transcription, translation, and narration. Intakes an .mp3 file.",
                 2:"Bypass Transcription: only translation and narration. Intakes .txt file.",
                 3:"Translation only. Intakes .txt file."}

# Main

# welcome to the program!
print("Welcome to the One Stop Shop Program!")
print("This program supports 3 modes: ")
for key,value in program_modes.items():
    print(f"{key}:{value}")
print()

# selecting program mode
mode = input("Would you like Mode 1, 2, 3? ")
match mode:
    case "1":
        target_file = input("Please enter target file name: \n")
        transcription_file = transcription() #stores the return transcription_file name from the transcription
        # function, allowing it to be used by the translation function
        translation_file = translation(transcription_file)
        narration_file = narration(translation_file)
    case "2":
        target_file = input("Please enter target file name: ")
        transcription_file = target_file + "-" + "transcription"
        with open(f"{transcription_file}.txt",'w') as file:
            print(f"Please open the {transcription_file} file and paste in the text to be translated. ")
        resume_program = input("Once finished, please type yes: ")
        translation_file = translation(transcription_file)
        narration_file = narration(translation_file)
    case "3":
        target_file = input("Please enter target file name: ")
        transcription_file = target_file + "-" + "transcription"
        with open(f"{transcription_file}.txt",'w') as file:
            print(f"Please open the {transcription_file} file and paste in the text to be translated. ")
        resume_program = input("Once finished, please type yes: ")
        translation_file = translation(transcription_file)

print("Thank you for using the one stop shop program! ")
