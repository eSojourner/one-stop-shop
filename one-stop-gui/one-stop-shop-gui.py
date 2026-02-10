import wx
import whisper
from datetime import datetime
from ollama import generate # to translate each of the different sections of the audio
from gtts import gTTS # for performing text to speech narration
import winsound # to play a sound when the program has finished various steps 

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
    winsound.MessageBeep()

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

class MyFrame(wx.Frame):
    def __init__(self, parent, title, size =(700,500)):
        super(MyFrame, self).__init__(parent, title=title, size=size)
        self.panel = wx.Panel(self)

        # static text funcitoning as user instructions/guidance 
        self.description1 = wx.StaticText(self.panel,label="Welcome to the Program!")
        font1 = wx.Font(wx.FontInfo(12).Bold())
        self.description1.SetFont(font1)

        self.description2 = wx.StaticText(self.panel, label="Please select which method you want to use:")
        font2 = wx.Font(wx.FontInfo(10))
        self.description2.SetFont(font2)
        
        # radio buttons for selecting different program options 
        self.rb1 = wx.RadioButton(self.panel, label="One Stop Shop")
        self.rb2 = wx.RadioButton(self.panel, label="Translation and Narration")
        self.rb3 = wx.RadioButton(self.panel, label="Only Translation")
        self.rb4 = wx.RadioButton(self.panel, label="Only Narration")

        self.rb1.Bind(wx.EVT_RADIOBUTTON, self.On_Radio_Selection)
        self.rb2.Bind(wx.EVT_RADIOBUTTON, self.On_Radio_Selection)
        self.rb3.Bind(wx.EVT_RADIOBUTTON, self.On_Radio_Selection)
        self.rb4.Bind(wx.EVT_RADIOBUTTON, self.On_Radio_Selection)

        # button for browsing which file to pick for the program and binding the OnFileSelection function to the button
        self.button1 = wx.Button(self.panel, label="Browse")
        self.Bind(wx.EVT_BUTTON, self.OnFileSelection, self.button1)

        # displaying the selected file 
        self.selected_file_text = wx.StaticText(self.panel, label="Selected file: ")
        self.selected_file_name = wx.StaticText(self.panel, label="")

        # button for executing the program 
        self.button2 = wx.Button(self.panel,label="Begin")
        self.Bind(wx.EVT_BUTTON, self.OnBeginProgram, self.button2)

        # static text title for the displayed output section of program
        self.program_output_title = wx.StaticText(self.panel, label="Output: ")

        # skeletal structure required for displaying program output
        self.program_output = wx.ListCtrl(parent=self.panel,style=wx.LC_REPORT)
        self.program_output.InsertColumn(0,"Name")
        self.program_output.InsertColumn(1,"Description")

        # primary vertical sizer to hold all widgets
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # adding radio buttons for selecting which option for the program to the first horizontal sizer 
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.hbox1.Add(self.rb1, wx.EXPAND)
        self.hbox1.Add(self.rb2, wx.EXPAND)
        self.hbox1.Add(self.rb3, wx.EXPAND)
        self.hbox1.Add(self.rb4, wx.EXPAND)

        # second horizontal slider for displaying the selected file name
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2.Add(self.selected_file_text, flag=wx.ALL | wx.EXPAND)
        self.hbox2.Add(self.selected_file_name, flag=wx.ALL | wx.EXPAND)

        # Third horizontal slider for displaying program output
        self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox3.AddSpacer(20)
        self.hbox3.Add(self.program_output_title, flag=wx.ALIGN_LEFT, border=10)
        self.hbox3.AddSpacer(20)
        self.hbox3.Add(self.program_output, 1, flag=wx.EXPAND)
        self.hbox3.AddSpacer(20)

        # adding widgets to the vbox
        self.vbox.AddSpacer(10)
        self.vbox.Add(self.description1,0,wx.CENTER, border=20)
        self.vbox.AddSpacer(3)
        self.vbox.Add(self.description2,0,wx.CENTER, border=20)
        self.vbox.AddSpacer(10)
        self.vbox.Add(self.hbox1, 0,  flag=wx.ALIGN_CENTER, border=10)
        self.vbox.AddSpacer(15)
        self.vbox.Add(self.button1, 0, flag=wx.ALIGN_CENTER, border=10)
        self.vbox.Add(self.hbox2, 0, flag=wx.ALL | wx.EXPAND, border=10)
        self.vbox.Add(self.button2, 0, flag=wx.ALIGN_CENTER, border=10)
        self.vbox.AddSpacer(20)
        self.vbox.Add(self.hbox3, 0, flag=wx.EXPAND)

        self.panel.SetSizer(self.vbox)

    wildcard_based_on_radio_selection = ""
    user_option_selection = 1
    target_file_name = ""
    # list to hold names of the outputted files from the programs that will be displayed in program_output report
    output = []

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
        
    def OnFileSelection(self, event):
        dialog = wx.FileDialog(self, "Open a file", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST, wildcard=self.wildcard_based_on_radio_selection)

        if dialog.ShowModal() == wx.ID_OK:
            try:
                with open(dialog.GetPath(), 'r') as a:
                    # the below line of code takes the absolute file path from the io.TextIOWrapper object,
                    # splits on the "\" character, and then selects the last item from the list 
                    # (which is the actual file name that will be used in the rest of the program). 
                    self.target_file_name = a.name.split("\\")[-1]
                    self.selected_file_name.SetLabel(f"{self.target_file_name}")
                    
            except Exception as e:
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

    def OnBeginProgram(self,event):
        progress = wx.ProgressDialog("Processing","Please wait...",maximum=100,parent=self,style=wx.PD_CAN_ABORT |
                                    wx.PD_AUTO_HIDE | wx.PD_SMOOTH)
        try:
            with open(f"{self.target_file_name}",'r') as a:
                match self.user_option_selection:
                    case 1:
                        # update status bar 
                        keep_going = progress.Update(25,f"Transcribing...")
                        # sets the  name of the target file as the input for  the transcription function
                        content = self.target_file_name
                        # sets the result of the transcription function as transcription_file
                        transcription_file = transcription(content, self.target_file_name)
                        # adds the name of the transcribed file into the final output list
                        self.output.append(transcription_file)
                        # update status bar 
                        keep_going = progress.Update(50,f"Translating...")
                        # opens previously made transcription file and reads it in
                        with open (f"{transcription_file}.txt",'r') as file:
                            content = file.read()
                        # sets the result of the translation function as translation_file
                        translation_file = translation(content, self.target_file_name)
                        # appends name of translated file to final output list
                        self.output.append(translation_file)
                        # Pause program to allow for editing of file prior to translation
                        program_interrupt()
                        # update status bar 
                        keep_going = progress.Update(75,f"Narrating...")
                        # opens previously translated file and reads it in
                        with open (f"{translation_file}.txt",'r') as file:
                            content = file.read()
                        # sets result of narration function as narration_file
                        narration_file = narration(content, self.target_file_name)
                        # appends narration_file name to output list
                        self.output.append(narration_file)
                        keep_going = progress.Update(100,f"Complete!")
                        # populates the wx.ListCtrl table with the contents of the output list
                        for i in range(len(self.output)):
                            self.program_output.InsertItem(i,self.output[i])
                        # clears selected_file_name variable upon successful program completion
                        wx.CallAfter(self.OnEndProgram)

                    case 2:
                        # update status bar 
                        keep_going = progress.Update(50,f"Translating...")
                        # read in transcript and store it in content
                        content = a.read()
                        # sets the result of the translation function as translation_file
                        translation_file = translation(content, self.target_file_name)
                        # appends name of translated file to final output list
                        self.output.append(translation_file)
                        # update status bar 
                        keep_going = progress.Update(75,f"Narrating...")
                        # opens previously translated file and reads it in
                        with open (f"{translation_file}.txt",'r') as file:
                            content = file.read()
                        # sets result of narration function as narration_file
                        narration_file = narration(content, self.target_file_name)
                        # appends narration_file name to output list
                        self.output.append(narration_file)
                        keep_going = progress.Update(100,f"Complete!")
                        # populates the wx.ListCtrl table with the contents of the output list
                        for i in range(len(self.output)):
                            self.program_output.InsertItem(i,self.output[i])
                        # clears selected_file_name variable upon successful program completion    
                        wx.CallAfter(self.OnEndProgram)
                    case 3:
                         # update status bar 
                        keep_going = progress.Update(50,f"Translating...")
                        # read in target file and store it in content
                        content = a.read()
                        # sets the result of the translation function as translation_file
                        translation_file = translation(content, self.target_file_name)
                        # appends name of translated file to final output list
                        self.output.append(translation_file)
                        # method complete 
                        keep_going = progress.Update(100,f"Complete!")
                        # populates the wx.ListCtrl table with the contents of the output list
                        for i in range(len(self.output)):
                            self.program_output.InsertItem(i,self.output[i])
                        # clears selected_file_name variable upon successful program completion
                        wx.CallAfter(self.OnEndProgram)
                    case 4:
                        # update status bar 
                        keep_going = progress.Update(50,f"Narrating...")
                        # read in target file and store it in content
                        content = a.read()
                        # sets result of narration function as narration_file
                        narration_file = narration(content,self.target_file_name)
                        # method complete 
                        keep_going = progress.Update(100,f"Complete!")
                        # populates the wx.ListCtrl table with the contents of the output list
                        for i in range(len(self.output)):
                            self.program_output.InsertItem(i,self.output[i])
                        # clears selected_file_name variable upon successful program completion
                        wx.CallAfter(self.OnEndProgram)
        
        except Exception as e:
                # display error message 
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
    
    def OnEndProgram(self):
        self.selected_file_name.SetLabel("")    

                      
app = wx.App()
frame = MyFrame(None, "One-Stop-Shop Program")
frame.Show()
app.MainLoop()
