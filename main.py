import pathlib
import pygubu
import threading
from bot import AutomamtionBot
import csv 
import webbrowser



PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "tkdesign.ui"


class App:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('mainwindow', master)
        builder.connect_callbacks(self)
        
        # Creating objects
        self.search_box = self.builder.get_object("search_box")
        self.civil_checkbox = self.builder.get_object("civil")
        self.penal_checkbox = self.builder.get_object("penal")
        self.contencioso_checkbox = self.builder.get_object("contencioso")
        self.social_checkbox = self.builder.get_object("social")
        self.militar_checkbox = self.builder.get_object("militar")
        self.special_checkbox = self.builder.get_object("special")
        self.search_button = self.builder.get_object("search_button")
        self.github_button = self.builder.get_object("github_button")
        self.gui_logger = builder.get_variable('curent_log')
        self.progressbar = self.builder.get_object("progressbar")
        
        # Start bot initialization in a separate thread
        threading.Thread(target=self.initialize_bot, daemon=True).start()

    def initialize_bot(self):
        # Disabling controls
        self.set_control_state("disabled")
        
        # Creating bot object and initializing
        self.bot = AutomamtionBot(self.gui_logger, self.progressbar)
        self.cookie = self.bot.obtain_cookie()
        
        if self.cookie:
            self.gui_logger.set(f"Bot initialized!")
            self.progressbar.destroy()
            self.builder.get_object("starting_label").pack_forget()

            # Enabling controls
            self.set_control_state("normal")

        else:
            self.progressbar.destroy()
            self.builder.get_object("starting_label").config(background="red")
            self.builder.get_variable("starting_label_text").set("Failed to initialize bot!")
            
            
    def open_github(self):
        threading.Thread(target=webbrowser.open, args=("https://github.com/tensor35/judicial_records_scrapper",), daemon=True).start()
        
        
    def start_bot(self):   
        threading.Thread(target=self.start_search, daemon=True).start()

    def start_search(self):
        self.set_control_state("disabled")
        search_string = self.search_box.get()
        
        # Define a mapping of checkbox widgets to their variable names
        checkboxes = {
            self.civil_checkbox: "civil_val",
            self.penal_checkbox: "penal_val",
            self.contencioso_checkbox: "contencioso_val",
            self.social_checkbox: "social_val",
            self.militar_checkbox: "militar_val",
            self.special_checkbox: "special_val",
        }
        
        selected_jurisdictions = []
        # Loop through each checkbox and check if it's selected
        for checkbox, var_name in checkboxes.items():
            variable = self.builder.tkvariables[var_name]
            if variable.get():
                selected_jurisdictions.append(checkbox.cget("text"))
                
        if not selected_jurisdictions:
            self.gui_logger.set("Please select at least one jurisdiction.")
            return
        
        self.gui_logger.set(f"Searching for: {search_string} in {', '.join(selected_jurisdictions)}")
        results = self.bot.get_total_results(search_string, selected_jurisdictions, self.cookie)
        
        
        if results:
            self.gui_logger.set(f"Total results: {int(results)}")
        else:
            self.gui_logger.set("Token expired or Somthing went wrong. Please restart the bot or see 'script.log'.")
            
        # Appending to CSV
        with open('results.csv', mode='a') as file:
            # eff empty add header
            if file.tell() == 0:
                writer = csv.writer(file)
                writer.writerow(['Search String', 'Jurisdictions', 'Results'])
            writer = csv.writer(file)
            writer.writerow([search_string, ', '.join(selected_jurisdictions), results])
        
        # Enabling controls
        self.set_control_state("normal")
        

    def set_control_state(self, state):
        # Disabling controls
        self.search_box.config(state=state)
        self.civil_checkbox.config(state=state)
        self.penal_checkbox.config(state=state)
        self.contencioso_checkbox.config(state=state)
        self.social_checkbox.config(state=state)
        self.militar_checkbox.config(state=state)
        self.special_checkbox.config(state=state)
        self.search_button.config(state=state)
        
    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
