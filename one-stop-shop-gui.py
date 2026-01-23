import wx
import whisper
from ollama import generate # to translate each of the different sections of the audio
from gtts import gTTS # for performing text to speech narration
import winsound # to play a sound when the program has finished various steps 
from datetime import datetime #for indicating how long each phase of the program took  

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
    narrated_file = file_name + "-"+ "narrated" + ".mp3"

    tts.save(narrated_file)

    # Indicate end of the final phase of the program and beep to let the user know the program 
    # has finished
    print(f"Narration complete. File saved as {narrated_file} \n")
    winsound.MessageBeep()

    # End time measurement for translation and print result 
    narration_end_time = datetime.now()  
    print(f"Narration took {narration_end_time - narration_start_time} \n") 


class MyFrame(wx.Frame):
    def __init__(self, parent, title, size =(700,500)):
        super(MyFrame, self).__init__(parent, title=title, size=size)
        self.panel = wx.Panel(self)
        
        self.description = wx.StaticText(self.panel, label="Please select one option from the following list:")

        self.rb1 = wx.RadioButton(self.panel, label="One Stop Shop")
        self.rb2 = wx.RadioButton(self.panel, label="Translation and Narration")
        self.rb3 = wx.RadioButton(self.panel, label="Only Translation")
        self.rb4 = wx.RadioButton(self.panel, label="Only Narration")

        self.rb1.Bind(wx.EVT_RADIOBUTTON, self.On_Radio_Selection)
        self.rb2.Bind(wx.EVT_RADIOBUTTON, self.On_Radio_Selection)
        self.rb3.Bind(wx.EVT_RADIOBUTTON, self.On_Radio_Selection)
        self.rb4.Bind(wx.EVT_RADIOBUTTON, self.On_Radio_Selection)


        self.button = wx.Button(self.panel, label="Browse")
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button)

        # primary vertical sizer to hold all widgets
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # horizontal sizer to hold the radio  buttons for selecting which option for the program
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.hbox.Add(self.rb1, wx.ALL | wx.EXPAND)
        self.hbox.Add(self.rb2, wx.ALL | wx.EXPAND)
        self.hbox.Add(self.rb3, wx.ALL | wx.EXPAND)
        self.hbox.Add(self.rb4, wx.ALL | wx.EXPAND)

        # adding widgets to the vbox
        self.vbox.Add(self.description,0,wx.ALIGN_CENTER | wx.ALL)
        self.vbox.Add(self.hbox, flag=wx.CENTER | wx.ALL)
        self.vbox.Add(self.button, 0, wx.ALIGN_CENTER | wx.ALL)
        
  
        self.panel.SetSizer(self.vbox)

    wildcard_based_on_radio_selection = ""
    user_option_selection = 1
    target_file_name = ""

    def On_Radio_Selection(self, event):
        """Function used to get the status of the radio buttons and to adjust the wildcard file selector accordingly"""
        selected_option = event.GetEventObject()
        
        match selected_option:
            case self.rb1:
                self.wildcard_based_on_radio_selection = "*.mp3"
                self.user_option_selection = 1
            case self.rb2:
                self.wildcard_based_on_radio_selection = "*.txt"
                self.user_option_selection = 2
            case self.rb3:
                self.wildcard_based_on_radio_selection = "*.txt"
                self.user_option_selection = 3
            case self.rb4:
                self.wildcard_based_on_radio_selection = "*.txt"
                self.user_option_selection = 4
        
    def OnButtonClick(self, event):
        dialog = wx.FileDialog(self, "Open a file", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST, wildcard=self.wildcard_based_on_radio_selection)

        if dialog.ShowModal() == wx.ID_OK:
            try:
                with open(dialog.GetPath(), 'r') as a:
                    # the below line of code takes the absolute file path from the io.TextIOWrapper object,
                    # splits on the "\" character, and then selects the last item from the list 
                    # (which is the actual file name that will be used in the rest of the program). 
                    self.target_file_name = a.name.split("\\")[-1]
                    match self.user_option_selection:
                        case 1:
                            content = self.target_file_name
                            transcription_file = transcription(content, self.target_file_name)
                            with open (f"{transcription_file}.txt",'r') as file:
                                content = file.read()
                            translation_file = translation(content, self.target_file_name)
                            with open (f"{translation_file}.txt",'r') as file:
                                content = file.read()
                            narration(content, self.target_file_name)
                        case 2:
                            content = a.read()
                            translation_file = translation(content, self.target_file_name)
                            with open (f"{translation_file}.txt",'r') as file:
                                content = file.read()
                            narration(content, self.target_file_name)
                        case 3:
                            content = a.read()
                            translation(content, self.target_file_name)
                        case 4:
                            content = a.read()
                            narration(content,self.target_file_name)
            except Exception as e:
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)


app = wx.App()
frame = MyFrame(None, "One-Stop-Shop Program")
frame.Show()
app.MainLoop()
