import wx
import threading
from one_stop_functions import transcription,translation,narration,program_interrupt

# Global variables to be used by both threads
wildcard_based_on_radio_selection = ""
user_option_selection = 1
# variable to transfer the content of Myframe's self.target_file_name to something the worker thread can access
worldwide_target_file_name = ""
# list to hold names of the outputted files from the programs that will be displayed in the program_output report
program_output_files = []

# Thread class that executes primary program processing
class WorkerThread(threading.Thread):
    """Worker Thread Class."""
    def __init__(self, parent):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self.parent = parent
        self._want_abort = 0
       

    def run(self):
        """Run Worker Thread."""
        try:
            with open(f"{worldwide_target_file_name}",'r') as a:
                match user_option_selection:
                    case 1:
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,5)
                        # sets the  name of the target file as the input for  the transcription function
                        content = worldwide_target_file_name
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,15)
                        # sets the output of the transcription function as transcription_file object
                        transcription_file = transcription(content, worldwide_target_file_name)
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,25)
                        # adds the name of the transcribed file into the final output list
                        global program_output_files
                        program_output_files.append(transcription_file)
                        # opens previously made transcription file and reads it in
                        with open (f"{transcription_file}.txt",'r') as file:
                            content = file.read()
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,35)
                        # sets the result of the translation function as translation_file
                        translation_file = translation(content, worldwide_target_file_name)
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,45)
                        # appends name of translated file to final output list
                        program_output_files.append(translation_file)
                       # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,55)
                        # Pause program to allow for editing of file prior to translation
                        program_interrupt()
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,65)
                        # opens previously translated file and reads it in
                        with open (f"{translation_file}.txt",'r') as file:
                            content = file.read()
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,75)
                        # sets result of narration function as narration_file
                        narration_file = narration(content, worldwide_target_file_name)
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,85)
                        # appends narration_file name to output list
                        program_output_files.append(narration_file)
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,95)
                        # populates the wx.ListCtrl table with the contents of the output list
                        for i in range(len(program_output_files)):
                           frame.program_output.InsertItem(i,program_output_files[i])
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,100)
                        # clears selected_file_name variable upon successful program completion
                        wx.CallAfter(frame.program_reset)
                    case 2:
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,15)
                        # read in transcript and store it in content
                        content = a.read()
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,35)
                        # sets the result of the translation function as translation_file
                        translation_file = translation(content, worldwide_target_file_name)
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,55)
                        # appends name of translated file to final output list
                        program_output_files.append(translation_file)
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,65)
                        # opens previously translated file and reads it in
                        with open (f"{translation_file}.txt",'r') as file:
                            content = file.read()
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,75)
                        # sets result of narration function as narration_file
                        narration_file = narration(content, worldwide_target_file_name)
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,85)
                        # appends narration_file name to output list
                        program_output_files.append(narration_file)
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,95)
                        # populates the wx.ListCtrl table with the contents of the output list
                        # populates the wx.ListCtrl table with the contents of the output list
                        for i in range(len(program_output_files)):
                           frame.program_output.InsertItem(i,program_output_files[i])
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,100)
                        # clears selected_file_name variable upon successful program completion    
                        wx.CallAfter(frame.program_reset)
                    case 3:
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,25)
                        # read in target file and store it in content
                        content = a.read()
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,35)
                        # sets the result of the translation function as translation_file
                        translation_file = translation(content, worldwide_target_file_name)
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,65)
                        # appends name of translated file to final output list
                        program_output_files.append(translation_file)
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,95)
                        # populates the wx.ListCtrl table with the contents of the output list
                        for i in range(len(program_output_files)):
                           frame.program_output.InsertItem(i,program_output_files[i])
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,100)
                        # clears selected_file_name variable upon successful program completion
                        wx.CallAfter(frame.program_reset)
                    case 4:
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,15)
                        # read in target file and store it in content
                        content = a.read()
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,35)
                        # sets result of narration function as narration_file
                        narration_file = narration(content,worldwide_target_file_name)
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,65)
                        # populates the wx.ListCtrl table with the contents of the output list
                        for i in range(len(program_output_files)):
                           frame.program_output.InsertItem(i,program_output_files[i])
                        # check if user wants to cancel and update status gauge
                        if self._want_abort == 1:
                            return
                        else:
                            wx.CallAfter(frame.update_gauge,100)
                        # clears selected_file_name variable upon successful program completion
                        wx.CallAfter(frame.program_reset)
        
        except Exception as e:
                # TO_DO: think I have to adjust this to send an error back to the main thread..
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1


class MyFrame(wx.Frame):
    def __init__(self, parent, title, size =(700,600)):
        super(MyFrame, self).__init__(parent, title=title, size=size)
        self.panel = wx.Panel(self)

        # indicate that there is no worker thread yet
        self.worker_thread = None

        # static text objects 
        self.welcome_title = wx.StaticText(self.panel,label="Welcome to the Program!")
        welcome_font = wx.Font(wx.FontInfo(12).Bold())
        self.welcome_title.SetFont(welcome_font)

        self.method_selection_text = wx.StaticText(self.panel, label="Please select which method you want to use:")
        which_method_font = wx.Font(wx.FontInfo(10))
        self.method_selection_text.SetFont(which_method_font)
        
        # radio button objects for selecting different program methods 
        self.rb1 = wx.RadioButton(self.panel, label="One Stop Shop")
        self.rb2 = wx.RadioButton(self.panel, label="Translation and Narration")
        self.rb3 = wx.RadioButton(self.panel, label="Translation Only")
        self.rb4 = wx.RadioButton(self.panel, label="Narration Only")

        # binding radio buttons to On_Radio_Selection function 
        self.rb1.Bind(wx.EVT_RADIOBUTTON, self.On_Radio_Selection)
        self.rb2.Bind(wx.EVT_RADIOBUTTON, self.On_Radio_Selection)
        self.rb3.Bind(wx.EVT_RADIOBUTTON, self.On_Radio_Selection)
        self.rb4.Bind(wx.EVT_RADIOBUTTON, self.On_Radio_Selection)

        # text to instruct user for selecting a file
        self.browse_description = wx.StaticText(self.panel, label="Please select file by clicking the Browse button: ")
        
        # button for browsing file to import
        self.browse_button = wx.Button(self.panel, label="Browse")

        # binding the button to the function FileSelection
        self.Bind(wx.EVT_BUTTON, self.FileSelection, self.browse_button)

        # selected file static text object
        self.selected_file_text = wx.StaticText(self.panel, label="Selected file: ")
        
        # an empty static text object that will be populated with the selected file from FileSelection 
        self.selected_file_name = wx.StaticText(self.panel, label="")

        # begin and cancel button objects to start and cancel primary program functionality 
        self.begin_program_button = wx.Button(self.panel,label="Begin")
        self.cancel_program_button = wx.Button(self.panel,label="Cancel")

        # binding begin_program_button and cancel_program buttons corresponding functions 
        self.Bind(wx.EVT_BUTTON, self.OnBeginProgram, self.begin_program_button)
        self.Bind(wx.EVT_BUTTON, self.OnCancelProgram,self.cancel_program_button)

        # static text title to indicate the Progress section of the GUI
        self.progress_title_text = wx.StaticText(self.panel, label="Progress: ")

        # gauge bar object for demonstrating progress 
        self.gauge = wx.Gauge(self.panel, range=100, size=(570,25) , style=wx.GA_PROGRESS)

        # static text title for output section of GUI
        self.program_output_title = wx.StaticText(self.panel, label="Output: ")

        # table for displaying program output
        self.program_output = wx.ListCtrl(parent=self.panel,style=wx.LC_REPORT)
        self.program_output.InsertColumn(0,"Name")
        self.program_output.InsertColumn(1,"Description")

        # primary vertical sizer to hold all widgets
        self.primary_vertical_container = wx.BoxSizer(wx.VERTICAL)

        # defining first horizontal container to hold radio buttons
        self.radio_container = wx.BoxSizer(wx.HORIZONTAL)

        # adding radio buttons to the container
        self.radio_container.Add(self.rb1, wx.EXPAND)
        self.radio_container.Add(self.rb2, wx.EXPAND)
        self.radio_container.Add(self.rb3, wx.EXPAND)
        self.radio_container.Add(self.rb4, wx.EXPAND)

        # defining second horizontal container to hold selected file name objects 
        self.file_name_container = wx.BoxSizer(wx.HORIZONTAL)

        # adding selected file name objects to container
        self.file_name_container.Add(self.selected_file_text, flag=wx.ALL | wx.EXPAND)
        self.file_name_container.Add(self.selected_file_name, flag=wx.ALL | wx.EXPAND)

        # defining another horizontal container for holding the begin and cancel buttons
        self.begin_cancel_container = wx.BoxSizer(wx.HORIZONTAL)

        # adding browse and cancel buttons to the container
        self.begin_cancel_container.Add(self.begin_program_button, flag=wx.ALL | wx.EXPAND)
        self.begin_cancel_container.Add(self.cancel_program_button, flag=wx.ALL | wx.EXPAND)
        
        # defining another horizontal container for holding the progress text and gauge
        self.progress_container = wx.BoxSizer(wx.HORIZONTAL)

        # adding progress section title and status bar objects to container 
        self.progress_container.AddSpacer(20)
        self.progress_container.Add(self.progress_title_text, flag=wx.ALIGN_LEFT, border=10)
        self.progress_container.AddSpacer(20)
        self.progress_container.Add(self.gauge)

        # defining another horizontal container for holding program output objects
        self.output_container = wx.BoxSizer(wx.HORIZONTAL)

        # adding program output objects to the container and adding spacers 
        self.output_container.AddSpacer(20)
        self.output_container.Add(self.program_output_title, flag=wx.ALIGN_LEFT, border=10)
        self.output_container.AddSpacer(20)
        self.output_container.Add(self.program_output, 1, flag=wx.EXPAND)
        self.output_container.AddSpacer(20)

        # adding all descriptions and horizontal containers to primary_vertical_container
        self.primary_vertical_container.AddSpacer(10)
        self.primary_vertical_container.Add(self.welcome_title,0,wx.CENTER, border=20)
        self.primary_vertical_container.AddSpacer(3)
        self.primary_vertical_container.Add(self.method_selection_text,0,wx.LEFT, border=10)
        self.primary_vertical_container.AddSpacer(10)
        self.primary_vertical_container.Add(self.radio_container, 0, flag=wx.ALIGN_CENTER, border=10)
        self.primary_vertical_container.AddSpacer(15)
        self.primary_vertical_container.Add(self.browse_description,0, flag=wx.LEFT, border=10)
        self.primary_vertical_container.AddSpacer(10)
        self.primary_vertical_container.Add(self.browse_button, 0, flag=wx.ALIGN_CENTER, border=10)
        self.primary_vertical_container.AddSpacer(10)
        self.primary_vertical_container.Add(self.file_name_container, 0, flag=wx.ALL | wx.EXPAND, border=10)
        self.primary_vertical_container.AddSpacer(10)
        self.primary_vertical_container.Add(self.begin_cancel_container,0,flag=wx.ALIGN_CENTER, border=10 )
        self.primary_vertical_container.AddSpacer(15)
        self.primary_vertical_container.Add(self.progress_container,0,flag=wx.EXPAND,border=10)
        self.primary_vertical_container.AddSpacer(15)
        self.primary_vertical_container.Add(self.output_container, 0, flag=wx.EXPAND)

        self.panel.SetSizer(self.primary_vertical_container)

    # Function used to get the status of the radio buttons and to adjust the wildcard file 
    # selector accordingly adjust the file selector once the user has clicked "browse". 
        # Note: one stop shop method accepts mp3 
        # Note: all other options intake .txt 
    def On_Radio_Selection(self, event):
        """Function used to get the status of the radio buttons and to adjust 
        the wildcard file selector accordingly when user clicks Browse"""
        selected_option = event.GetEventObject()
        global wildcard_based_on_radio_selection 
        global user_option_selection

        match selected_option:
            case self.rb1:        
                wildcard_based_on_radio_selection = "*.mp3"
                user_option_selection = 1
            case self.rb2:
                wildcard_based_on_radio_selection = "*.txt"
                user_option_selection = 2
            case self.rb3:
                wildcard_based_on_radio_selection = "*.txt"
                user_option_selection = 3
            case self.rb4:
                wildcard_based_on_radio_selection = "*.txt"
                user_option_selection = 4

    # the below function is called when the user clicks "Browse" to look for a file to import 
    # Note: the wildcard in the wx.FileDialog reflects whichever radio button the user has 
    # selected using the OnRadioSelection function     
    def FileSelection(self, event):
        global wildcard_based_on_radio_selection
        dialog = wx.FileDialog(self, "Open a file", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST, wildcard=wildcard_based_on_radio_selection)

        if dialog.ShowModal() == wx.ID_OK:
            try:
                with open(dialog.GetPath(), 'r') as a:
                    # the below code takes the absolute file path from the io.TextIOWrapper object,
                    # splits on the "\" character, and then selects the last item from the list 
                    # The last item from the list is the actual file name that will be used for 
                    # the rest of the program. 
                    self.target_file_name = a.name.split("\\")[-1]
                    self.selected_file_name.SetLabel(f"{self.target_file_name}")
                    global worldwide_target_file_name
                    worldwide_target_file_name = self.target_file_name
                    
            except Exception as e:
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

    # this is where the main thread will task a worker thread with running the primary processing
    # of the program. This function is called when the user clicks the "Begin" button 
    
    def OnBeginProgram(self,event):
        if not self.worker_thread:
            self.program_output.DeleteAllItems()
            global program_output_files
            program_output_files = []
            self.worker_thread = WorkerThread(self)
            self.worker_thread.start()
        
        
    # this function will cancel the worker thread's processing
    def OnCancelProgram(self, event):
        if self.worker_thread:
            self.worker_thread.abort()
            self.selected_file_name.SetLabel("")
            self.update_gauge(0)
            self.worker_thread = None
            global worldwide_target_file_name
            worldwide_target_file_name = ""

    # update progress gauge. To be run from worker thread 
    def update_gauge (self, value):
        self.gauge.SetValue(value)

    # function to reset program after successful completion 
    def program_reset(self):
        global wildcard_based_on_radio_selection
        global user_option_selection
        global target_file_name
        global worldwide_target_file_name
        wildcard_based_on_radio_selection = ""
        user_option_selection = 1
        target_file_name = ""
        worldwide_target_file_name = ""
        self.selected_file_name.SetLabel("")
        self.update_gauge(0)
        self.worker_thread = None


# START_HERE: trying to get the worker thread access it needs to all of the variables
# after that, have to test the logic for the status gauge to update itself as worker thread progresses          

app = wx.App()
frame = MyFrame(None, "One-Stop-Shop Program")
frame.Show()
app.MainLoop()
