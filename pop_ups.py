import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date, datetime
import ticket_processor as txp
import random as r

class Add_Entry_Window(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.title("Tketer | Add Entry")
        self.resizable(False, False)
        self.geometry("+700+200")
        self.iconbitmap("images/ticket.ico")
        
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        
        # frames
        self.frm_main = ttk.Frame(self)
        
        self.frm_title = ttk.Frame(self.frm_main)
        self.frm_fields = ttk.Frame(self.frm_main)
        self.frm_actions = ttk.Frame(self.frm_main)

        # frm_title component
        self.lbl_title = ttk.Label(self.frm_title, text="Add Entry")

        # frm_fields components
        self.lbl_name = ttk.Label(self.frm_fields, text="Name")
        self.lbl_course = ttk.Label(self.frm_fields, text="Course")
        self.lbl_section = ttk.Label(self.frm_fields, text="Section")
        self.lbl_date = ttk.Label(self.frm_fields, text="Date")

        self.ent_name = ttk.Entry(self.frm_fields, width=40, font=("Arial", 11))
        self.ent_course = ttk.Entry(self.frm_fields, width=15, font=("Arial", 11))
        self.ent_section = ttk.Entry(self.frm_fields, width=10, font=("Arial", 11))
        self.ent_date = ttk.Entry(self.frm_fields, width=15, font=("Arial", 11))

        # frm_actions components
        self.custom_date = tk.BooleanVar()
        self.cbtn_custom_date = ttk.Checkbutton(self.frm_main, text="Set Custom Date", variable=self.custom_date, style="PopUp.TCheckbutton", command=self.update_date_state)

        self.btn_add = ttk.Button(self.frm_actions, text="Create Ticket", width=15, style="PopUp.TButton", command=self.add_data)
        self.btn_cancel = ttk.Button(self.frm_actions, text="Cancel", style="PopUp.TButton", command=self.destroy)

        # pack frame and components
        self.frm_main.pack(padx=10, pady=10)

        # configure frm_main rows and columns
        self.frm_main.grid_rowconfigure(0, weight=1)
        self.frm_main.grid_rowconfigure(1, minsize=30, weight=1)
        self.frm_main.grid_rowconfigure(2, minsize=30, weight=1)
        self.frm_main.grid_rowconfigure(3, weight=1)

        self.frm_main.grid_columnconfigure(0, minsize=50, weight=1)
        self.frm_main.grid_columnconfigure(1, minsize=150, weight=1)

        # pack frm_title and child
        self.frm_title.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.lbl_title.pack(pady=(5, 15))

        # pack frm_fields and children
        self.frm_fields.grid(row=1, column=0, rowspan=2, columnspan=2, sticky="nsew", pady=(0, 15))

        self.lbl_name.grid(row=0, column=0)
        self.lbl_course.grid(row=1, column=0, padx=10, pady=15)
        self.lbl_section.grid(row=1, column=2, padx=(30, 10))
        self.lbl_date.grid(row=2, column=0)

        self.ent_name.grid(row=0, column=1, columnspan=3)
        self.ent_course.grid(row=1, column=1)
        self.ent_section.grid(row=1, column=3)
        self.ent_date.grid(row=2, column=1)

        # pack frm_actions and children
        self.frm_actions.grid(row=3, column=1, sticky="nsew")

        #configure spacer column
        self.frm_actions.grid_columnconfigure(1, weight=1)

        self.cbtn_custom_date.place(x=14, y=175)
        self.btn_cancel.grid(row=0, column=2, padx=(0, 5))
        self.btn_add.grid(row=0, column=3)

        self.update_date_state()

    def update_date_state(self):
        if self.custom_date.get():
            self.ent_date.config(state=tk.NORMAL)
        else:
            self.ent_date.delete(0, tk.END)
            self.ent_date.insert(0, date.today().strftime("%m/%d/%Y"))
            self.ent_date.config(state=tk.DISABLED)

    def add_data(self):
        all_filled = all(ent.get() for ent in [self.ent_name, self.ent_course, self.ent_section, self.ent_date])
        
        if all_filled:
            try:
                formatted_date = (datetime.strptime(self.ent_date.get(), "%m/%d/%Y")).strftime("%Y-%m-%d")
                formatted_course_section = f"{self.ent_course.get()} - {self.ent_section.get()}"

                if datetime.strptime(self.ent_date.get(), "%m/%d/%Y") > datetime.strptime(self.parent.event_date, "%m/%d/%Y"):
                    messagebox.showwarning("Invalid Date", "The entered date is beyond the event date. Please provide a valid date.")
                    return

                data = (self.ent_name.get(), formatted_course_section, formatted_date)
                
                self.parent.dataManager.add_ticket_entry(*data)
                self.parent.update_list()
                self.destroy()
            except ValueError as e:
                print(e)
                messagebox.showwarning("Invalid Date Format", "The date format is incorrect. Please enter the date in MM/DD/YYYY format.", parent=self)
        else:
            messagebox.showwarning("Incomplete Form", "Please fill in all required fields before proceeding.", parent=self)


class Update_Entry_Window(tk.Toplevel):
    def __init__(self, ticket_number: int, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.ticket_number = ticket_number
        self.name = None
        self.course_section = None
        self.date = None

        self.title("Tketer | Update Entry")
        self.resizable(False, False)
        self.geometry("+700+200")
        self.iconbitmap("images/ticket.ico")
        
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        
        # frames
        self.frm_main = ttk.Frame(self)
        
        self.frm_title = ttk.Frame(self.frm_main)
        self.frm_fields = ttk.Frame(self.frm_main)
        self.frm_actions = ttk.Frame(self.frm_main)

        # frm_title component
        self.lbl_title = ttk.Label(self.frm_title, text="Update Entry")

        # frm_fields components
        self.lbl_name = ttk.Label(self.frm_fields, text="Name")
        self.lbl_course = ttk.Label(self.frm_fields, text="Course")
        self.lbl_section = ttk.Label(self.frm_fields, text="Section")
        self.lbl_date = ttk.Label(self.frm_fields, text="Date")

        self.ent_name = ttk.Entry(self.frm_fields, width=40, font=("Arial", 11))
        self.ent_course = ttk.Entry(self.frm_fields, width=15, font=("Arial", 11))
        self.ent_section = ttk.Entry(self.frm_fields, width=10, font=("Arial", 11))
        self.ent_date = ttk.Entry(self.frm_fields, width=15, font=("Arial", 11))

        # frm_actions components
        self.custom_date = tk.BooleanVar()
        self.cbtn_custom_date = ttk.Checkbutton(self.frm_main, text="Set Custom Date", variable=self.custom_date, style="PopUp.TCheckbutton", command=self.update_date_state)

        self.btn_add = ttk.Button(self.frm_actions, text="Update Ticket", width=15, style="PopUp.TButton", command=lambda: self.update_data(self.ticket_number))
        self.btn_cancel = ttk.Button(self.frm_actions, text="Cancel", style="PopUp.TButton", command=self.destroy)

        # pack frame and components
        self.frm_main.pack(padx=10, pady=10)

        # configure frm_main rows and columns
        self.frm_main.grid_rowconfigure(0, weight=1)
        self.frm_main.grid_rowconfigure(1, minsize=30, weight=1)
        self.frm_main.grid_rowconfigure(2, minsize=30, weight=1)
        self.frm_main.grid_rowconfigure(3, weight=1)

        self.frm_main.grid_columnconfigure(0, minsize=50, weight=1)
        self.frm_main.grid_columnconfigure(1, minsize=150, weight=1)

        # pack frm_title and child
        self.frm_title.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.lbl_title.pack(pady=(5, 15))

        # pack frm_fields and children
        self.frm_fields.grid(row=1, column=0, rowspan=2, columnspan=2, sticky="nsew", pady=(0, 15))

        self.lbl_name.grid(row=0, column=0)
        self.lbl_course.grid(row=1, column=0, padx=10, pady=15)
        self.lbl_section.grid(row=1, column=2, padx=(30, 10))
        self.lbl_date.grid(row=2, column=0)

        self.ent_name.grid(row=0, column=1, columnspan=3)
        self.ent_course.grid(row=1, column=1)
        self.ent_section.grid(row=1, column=3)
        self.ent_date.grid(row=2, column=1)

        # pack frm_actions and children
        self.frm_actions.grid(row=3, column=1, sticky="nsew")

        #configure spacer column
        self.frm_actions.grid_columnconfigure(1, weight=1)

        self.cbtn_custom_date.place(x=14, y=175)
        self.btn_cancel.grid(row=0, column=2, padx=(0, 5))
        self.btn_add.grid(row=0, column=3)

        self.get_and_set_data(self.ticket_number)
        self.update_date_state()

    def update_date_state(self):
        if self.custom_date.get():
            self.ent_date.config(state=tk.NORMAL)
        else:
            self.ent_date.delete(0, tk.END)
            self.ent_date.insert(0, self.date.strftime("%m/%d/%Y"))
            self.ent_date.config(state=tk.DISABLED)
    
    def get_and_set_data(self, current_ticket_number):
        datum = self.parent.dataManager.get_datum(current_ticket_number)
        self.name = datum[1]
        self.course_section = datum[2].split(" - ")
        self.date = datum[3]

        self.ent_name.delete(0, tk.END)
        self.ent_name.insert(0, self.name)
        self.ent_course.delete(0, tk.END)
        self.ent_course.insert(0, self.course_section[0])
        self.ent_section.delete(0, tk.END)
        self.ent_section.insert(0, self.course_section[1])

    def update_data(self, ticket_number):
        all_filled = all(ent.get() for ent in [self.ent_name, self.ent_course, self.ent_section, self.ent_date])
        
        if all_filled:
            try:
                ticket_no = ticket_number

                formatted_date = (datetime.strptime(self.ent_date.get(), "%m/%d/%Y")).strftime("%Y-%m-%d")
                formatted_course_section = f"{self.ent_course.get()} - {self.ent_section.get()}"

                if datetime.strptime(self.ent_date.get(), "%m/%d/%Y") > datetime.strptime(self.parent.event_date, "%m/%d/%Y"):
                    messagebox.showwarning("Invalid Date", "The entered date is beyond the event date. Please provide a valid date.")
                    return

                data = (ticket_no, self.ent_name.get(), formatted_course_section, formatted_date)
                
                self.parent.dataManager.update_ticket_entry(*data)
                self.parent.update_list()
                self.destroy()
            except ValueError as e:
                print(e)
                messagebox.showwarning("Invalid Date Format", "The date format is incorrect. Please enter the date in MM/DD/YYYY format.", parent=self)
        else:
            messagebox.showwarning("Incomplete Form", "Please fill in all required fields before proceeding.", parent=self)


class PreviewTicketWindow(tk.Toplevel):
    def __init__(self, image: tk.PhotoImage, id, event_data: list, parent=None):
        super().__init__(parent)

        self.event_data = event_data
        self.id = id
        self.parent = parent

        self.title("Tketer | Ticket Preview")
        self.resizable(False, False)
        self.geometry("+600+100")
        self.iconbitmap("images/ticket.ico")
        
        self.transient(parent)
        self.grab_set()
        self.focus_set()

        # frames
        self.frm_main = ttk.Frame(self)

        self.frm_image = ttk.Frame(self.frm_main)
        self.frm_buttons = ttk.Frame(self.frm_main)

        # frm_image component
        self.img = tk.Canvas(self.frm_image, height=250, width=500)

        self.image = image

        self.img.create_image(0, 0, anchor="nw", image=self.image)

        # frm_buttons components
        self.btn_export = ttk.Button(self.frm_buttons, text="Export Ticket", width=15, style="PopUp.TButton", command=self.export)
        self.btn_cancel = ttk.Button(self.frm_buttons, text="Cancel", width=10, style="PopUp.TButton", command=self.destroy)

        # pack frame and components
        self.frm_main.pack(padx=10, pady=10)

        # pack frm_image and child
        self.frm_image.grid(row=0, column=0, sticky="nsew")

        self.img.pack()

        # pack frm_buttons and children
        self.frm_buttons.grid(row=1, column=0, sticky="nsew")
        
        # configure spacer
        self.frm_buttons.grid_columnconfigure(0, weight=1)

        self.btn_cancel.grid(row=0, column=1, padx=(0, 5))
        self.btn_export.grid(row=0, column=2)

    def export(self):
        confirmation = messagebox.askquestion("Export ticket", "Export current entry into a ticket?")

        if confirmation == "yes":
            try:
                folder_path = filedialog.askdirectory()

                if not folder_path:
                    return

                txp.create_ticket_image(self.parent.dataManager, self.event_data[0], self.event_data[1], self.event_data[2], self.event_data[3], folder_path, 3, self.id)
                messagebox.showinfo("Export Successful", "Entry has been successfully exported.", parent=self)
            except Exception as e:
                print("Something happened:", e)
                messagebox.showerror("Error", "Something went wrong.")

def simulate_progress(parent): # should make message and title dynamic !!!
    def go(i = 0, period_count = 1):
        if i < 51:
            progress_bar['value'] = i
            random = r.randint(1, 2)
            add_value = 5 if random == 1 else 10

            period_count = (period_count % 3) + 1
            periods = "." * period_count

            lbl.config(text=f"Exporting data{periods}")
            root.after(150, go, i + add_value, period_count)
        else:
            root.destroy()
            messagebox.showinfo("Export Successful", "Data has been successfully exported into an Excel file.", parent=parent)

    root = tk.Toplevel(parent)
    root.title("Tketer | Export")
    root.resizable(False, False)
    root.iconbitmap("images/ticket.ico")

    root.transient(parent)
    root.grab_set()
    root.focus_set()

    lbl = tk.Label(root, text="Exporting data...")
    lbl.pack(pady=(10, 5), padx=(0, 160))

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=250)
    progress_bar['maximum'] = 50
    progress_bar.pack(padx=10, pady=(0, 10))

    go()

class Settings(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.title("Tketer | Settings")
        self.resizable(False, False)

        self.geometry("+400+200")
        self.iconbitmap("images/ticket.ico")

        self.transient(parent)
        self.grab_set()
        self.focus_set()

        # define frames
        self.frm_main = ttk.Frame(self)
        self.frm_fields = ttk.Frame(self.frm_main)
        self.frm_buttons = ttk.Frame(self.frm_main)

        # define frm_main components

        # define frm_fields components
        self.ent_event_name = ttk.Entry(self.frm_fields, width=25, font=("Arial", 10))
        self.ent_event_venue = ttk.Entry(self.frm_fields, width=30, font=("Arial", 10))
        self.ent_event_date = ttk.Entry(self.frm_fields, width=12, font=("Arial", 10))

        self.lbl_event_name = ttk.Label(self.frm_fields, text="Event Name", style="Settings.TLabel")
        self.lbl_event_venue = ttk.Label(self.frm_fields, text="Event Venue", style="Settings.TLabel")
        self.lbl_event_date = ttk.Label(self.frm_fields, text="Event Date", style="Settings.TLabel")

        # define frm_fields subframe and children
        self.frm_sub = ttk.Frame(self.frm_fields)

        self.ent_start_time = ttk.Entry(self.frm_sub, width=5, font=("Arial", 10))
        self.lbl_to = ttk.Label(self.frm_sub, text="to", style="Settings.TLabel")
        self.ent_end_time = ttk.Entry(self.frm_sub, width=5, font=("Arial", 10))
        self.lbl_time = ttk.Label(self.frm_sub, text="Time", style="Settings.TLabel")


        # define frm_buttons components
        self.btn_apply = ttk.Button(self.frm_buttons, text="Apply", width=12, style="Settings.TButton", command=self.change_settings)
        self.btn_cancel = ttk.Button(self.frm_buttons, text="Cancel", width=10, style="Settings.TButton", command=self.destroy)

        # pack frames and components
        self.frm_main.pack(padx=10, pady=10)

        # pack frm_fields and children
        self.frm_fields.pack()
        
        self.ent_event_name.pack()
        self.lbl_event_name.pack(pady=(0, 10))

        self.ent_event_venue.pack()
        self.lbl_event_venue.pack(pady=(0, 10))

        self.ent_event_date.pack()
        self.lbl_event_date.pack(pady=(0, 10))

        # pack frm_fields subframe and children
        self.frm_sub.pack(pady=(0, 10))

        self.ent_start_time.grid(row=0, column=0)
        self.lbl_to.grid(row=0, column=1)
        self.ent_end_time.grid(row=0, column=3)
        self.lbl_time.grid(row=1, column=0, columnspan=3, padx=(55, 0), pady=(5, 0))

        # pack frm_buttons and children
        self.frm_buttons.pack()

        self.btn_cancel.pack(side=tk.LEFT, padx=(0, 5))
        self.btn_apply.pack(side=tk.LEFT)

        self.set_values()

    def change_settings(self):
        all_filled = all([ent.get() for ent in [self.ent_event_name, self.ent_event_venue, self.ent_event_date, self.ent_start_time, self.ent_end_time]])

        if all_filled:
            try:
                self.apply_values()
            except ValueError as e:
                return
        else:
            messagebox.showwarning("Incomplete Form", "Please fill in all required fields before proceeding.", parent=self)

    def set_values(self):
        self.ent_event_name.delete(0, tk.END)
        self.ent_event_venue.delete(0, tk.END)
        self.ent_event_date.delete(0, tk.END)
        self.ent_start_time.delete(0, tk.END)
        self.ent_end_time.delete(0, tk.END)

        if not self.parent.event_name:
            self.ent_event_date.insert(tk.END, "MM/DD/YYYY")
            self.ent_start_time.insert(tk.END, "00:00")
            self.ent_end_time.insert(tk.END, "23:00")
        else:
            self.ent_event_name.insert(tk.END, self.parent.event_name)
            self.ent_event_venue.insert(tk.END, self.parent.event_venue)
            self.ent_event_date.insert(tk.END, self.parent.event_date)
            self.ent_start_time.insert(tk.END, self.parent.event_time[0])
            self.ent_end_time.insert(tk.END, self.parent.event_time[1])

    def apply_values(self):
        try: 
            event_name = self.ent_event_name.get()
            event_venue = self.ent_event_venue.get()
            event_date = (datetime.strptime(self.ent_event_date.get(), "%m/%d/%Y")).strftime("%m/%d/%Y")

            event_time = [datetime.strptime(self.ent_start_time.get(), "%H:%M").time(), datetime.strptime(self.ent_end_time.get(), "%H:%M").time()]
            event_time = [t.strftime("%H:%M") for t in event_time]
            # print(event_time[0].strftime("%I:%M %p"), event_time[1].strftime("%I:%M %p"))

            if self.parent.event_date: # check if there is pre-existinn event date
                if event_date < self.parent.event_date: # check if new event date is earlier than current event date
                    if datetime.strptime(self.ent_event_date.get(), "%m/%d/%Y").date() < datetime.today().date(): # check if new event date is earlier than today
                     messagebox.showwarning("Invalid Date", "The event date cannot be in the past. Please select a present/future date.", parent=self)
                     return
                    
                    confirm = messagebox.askyesno("Confirm Date Change",
                                                  f"The new date ({event_date}) is earlier than the current date ({self.parent.event_date}).\n"
                                                  "Entries with dates beyond this new event date will be removed.\n"
                                                  "Do you want to proceed?", icon="warning", parent=self)
                    if confirm:
                        self.parent.dataManager.delete_multiple(1, (datetime.strptime(self.ent_event_date.get(), "%m/%d/%Y")))
                        self.parent.update_list()
                    else:
                        return 
            else:
                if datetime.strptime(self.ent_event_date.get(), "%m/%d/%Y").date() < datetime.today().date():
                     messagebox.showwarning("Invalid Date", "The event date cannot be in the past. Please select a present/future date.", parent=self)
                     return

            self.parent.event_name = event_name
            self.parent.event_venue = event_venue
            self.parent.event_date = event_date
            self.parent.event_time = event_time

            self.parent.dataManager.set_evnt_config(event_name, event_venue, event_date, event_time[0], event_time[1])

            self.destroy()
        except ValueError as e:
            messagebox.showwarning("Invalid Format", "Please ensure the date is in MM/DD/YYYY format and the time is in HH:MM (24-hour) format.", parent=self)
            raise ValueError


class Excel_Sort(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.title("Tketer | Export")
        self.resizable(False, False)

        self.geometry("+500+200")
        self.iconbitmap("images/ticket.ico")

        style = ttk.Style()
        style.configure("s.TButton", font=("Arial", 10), padding=(6, 3))

        self.transient(parent)
        self.grab_set()
        self.focus_set()

        self.frm_main = ttk.Frame(self)
        
        self.frm_message = ttk.Frame(self.frm_main)
        self.frm_choices = ttk.Frame(self.frm_main)

        self.lbl_message = ttk.Label(self.frm_message, text="Sort by:")

        self.btn_name = ttk.Button(self.frm_choices, text="Name", style="s.TButton", command=lambda: self.return_choice("name"))
        self.btn_ticket_no = ttk.Button(self.frm_choices, text="Ticket No.", style="s.TButton", command=lambda: self.return_choice("ticket_no"))
        self.btn_course_section = ttk.Button(self.frm_choices, text="Course & Section", style="s.TButton", command=lambda: self.return_choice("course_section"))
        self.btn_date = ttk.Button(self.frm_choices, text="Date", style="s.TButton", command=lambda: self.return_choice("date"))

        self.frm_main.pack(padx=10, pady=10)

        self.frm_message.pack(pady=(0, 10))
        self.lbl_message.pack()

        self.frm_choices.pack(expand=True)
        self.btn_name.pack(pady=(0, 5), fill="both")
        self.btn_ticket_no.pack(pady=(0, 5), fill="both")
        self.btn_course_section.pack(pady=(0, 5), fill="both")
        self.btn_date.pack(pady=(0, 5), fill="both")

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def return_choice(self, filter):
        self.result = filter
        self.destroy()
    
    def on_cancel(self):
        self.result = None
        self.destroy()

class PleaseWait(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.title("Tketer | Exporting...")
        self.resizable(False, False)
        self.iconbitmap("images/ticket.ico")

        self.geometry("+500+200")

        self.transient(parent)
        self.grab_set()
        self.focus_set()

        self.lbl_message = ttk.Label(self, text="Exporting Tickets... Please wait.")

        self.lbl_message.pack(padx=30, pady=30)

