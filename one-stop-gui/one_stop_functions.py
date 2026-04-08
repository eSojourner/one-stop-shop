import wx
import whisper
from datetime import datetime
from ollama import generate # to translate each of the different sections of the audio
from gtts import gTTS # for performing text to speech narration


def transcription(content, file_name):
        """Generates English Transcription of target_file"""

        #load whispher model of choice to transcribe target file
        print("Transcription in progress...\n")
        

        model = whisper.load_model("turbo")
        result = model.transcribe(content)

        # Saving transcription to a file named "transcription_file"
        transcription_file = file_name + "-" + "transcription"

        with open (f"{transcription_file}.txt", "w") as output:
            output.write(result["text"])

        print(f"Transcription complete. File saved as {transcription_file} \n")

        return transcription_file 

def translation(content, file_name):
        '''Translate the file_to_be_translated into target language'''
        #Give some breathing room in the terminal and indicate the beginning of translation phase
        # using Ollama gemma2 locally 
        print()
        print("Translation in progress... \n")
        translation_start_time = datetime.now() #begin time measurement for translation 

        # open transcript and split all words on spaces and add them to a temporary list    
        temp_list = content.split()

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
        translation_file = file_name + "-"+ "translation"

        with open(f"{translation_file}.txt","w") as output:
            for each in translated_sections:
                output.write(str(each))

        print(f"Translation complete. File saved as {translation_file} \n")

        # End time measurement for translation and print result 
        translation_end_time = datetime.now()  
        print(f"Translation took {translation_end_time - translation_start_time} \n") 

        return translation_file

def narration(content, file_name):
    '''Narrates file using Google's Text to Speech endpoint'''
    #Giving some breathing room in the terminal and indicating the beginning of narration phase
    print()
    print("Narration in progress...\n")

    # Begin time measurement for narration
    narration_start_time = datetime.now()  

    # Perform Spanish text to speech narration using Google Text To Speech Endpoint 
    # narrate the file that is written in Spanish ("es") and narrate it with a Mexican Spanish 
    # accent ("tld="com.mx"") 
    tts = gTTS(content, lang="es",tld="com.mx")

    # create a name for the narrated file and save it 
    narration_file = file_name + "-"+ "narrated" + ".mp3"

    tts.save(narration_file)

    # Indicate end of the final phase of the program and beep to let the user know the program 
    # has finished
    print(f"Narration complete. File saved as {narration_file} \n")

    # End time measurement for translation and print result 
    narration_end_time = datetime.now()  
    print(f"Narration took {narration_end_time - narration_start_time} \n") 
    return narration_file

def program_interrupt():
        program_interrupt = wx.MessageDialog(parent=None, message="Please review the translation file for errors. " \
                        "Press OK when finished", caption="Popup Message", style=wx.OK | wx.ICON_INFORMATION)
        result = program_interrupt.ShowModal()
        if result == wx.ID_OK:
            pass 
