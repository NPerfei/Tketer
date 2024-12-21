import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import database_manager as dbm
import xlsx_processor as exp
import ticket_processor as txp
import pop_ups as ppup

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.database = dbm.DatabaseManager()

        self.title("Tketer | Login")
        self.resizable(False, False)
        self.geometry("+300+200")
        self.iconbitmap("images/ticket.ico")

        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 11))
        style.configure("TEntry", padding=(10, 5))
        style.configure("Title.TLabel", font=("Arial", 14, "bold"))
        style.configure("TButton", padding=(12, 6), font=("Arial", 11))
        

        self.frm_main = ttk.Frame(self)
        self.frm_title = ttk.Frame(self.frm_main)
        self.frm_entries = ttk.Frame(self.frm_main)
        self.frm_button = ttk.Frame(self.frm_main)

        self.lbl_login_title = ttk.Label(self.frm_title, text="Login", style="Title.TLabel")

        self.lbl_username = ttk.Label(self.frm_entries, text="Username: ", justify="left")
        self.lbl_password = ttk.Label(self.frm_entries, text="Password: ", justify="left")
        self.ent_username = ttk.Entry(self.frm_entries, font=("Arial", 11), width=25)
        self.ent_password = ttk.Entry(self.frm_entries, show="*", font=("Arial", 11), width=25)

        self.btn_login_button = ttk.Button(self.frm_button, text="Login", command=self.authenticate_login)

        self.frm_main.pack(padx=20, pady=20)

        self.frm_title.pack(pady=(0, 15))
        self.lbl_login_title.pack()

        self.frm_entries.pack(pady=(0, 20))
        self.lbl_username.pack(fill="both")
        self.ent_username.pack(pady=(0, 10))
        self.lbl_password.pack(fill="both")
        self.ent_password.pack()

        self.frm_button.pack(fill="both")
        self.btn_login_button.pack(fill="both")

        if self.database.is_logged_in()[0]:
            self.destroy()
            DashBoard().mainloop()

    def authenticate_login(self):
        entered_username = self.ent_username.get()
        entered_password = self.ent_password.get()

        if entered_username and entered_password:
            username, password = self.database.get_admin_credentials()

            if entered_username == username and entered_password == password:
                messagebox.showinfo("Login Successful", "You have successfully logged in.", parent=self)
                self.database.log_in_out(1)

                self.unbind_all("<KeyPress>")
                self.update_idletasks()
                self.update()

                self.destroy()
                DashBoard().mainloop()
            else:
                messagebox.showwarning("Login Failed", "Invalid admin credentials. Please try again.", parent=self)
        else:
            messagebox.showwarning("Incomplete Form", "Please fill in all fields before proceeding.", parent=self)


class DashBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.dataManager = dbm.DatabaseManager()

        self.event_name = None
        self.event_venue = None
        self.event_date = None
        self.event_time = None

        self.title("Tketer | Dasboard")
        self.resizable(False, False)
        self.geometry("+200+25")
        self.iconbitmap("images/ticket.ico")

        # styles
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=(10, 5))
        style.configure("TEntry", padding=(10, 5))
        style.configure("TCombobox", padding=(10, 5))
        self.option_add("*TCombobox*Listbox*Font", ("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 12), rowheight=29)
        style.configure("TLabel", font=("Arial", 11))

        # popup styles
        style.configure("PopUp.TButton", font=("Arial", 10), padding=(8, 4))
        style.configure("PopUp.TCheckbutton", font=("Arial", 10))

        # settings styles
        style.configure("Settings.TButton", font=("Arial", 10), padding=(4, 2))
        style.configure("Settings.TLabel", font=("Arial", 10))

        style.configure("Mini_icons.TButton", padding=(0, 0))

        # ticket_count_label_style
        style.configure("Count.TLabel", font=("Arial", 12))

        # frame and widget creation
        self.frm_main = tk.Frame(self)

        self.frm_sort_search = ttk.Frame(self.frm_main)
        self.frm_tree_view = ttk.Frame(self.frm_main)
        self.frm_crud = ttk.Frame(self.frm_main)
        self.frm_misc = ttk.Frame(self.frm_main)

        # frm_sort_search components
        self.ent_search = ttk.Entry(self.frm_sort_search, width=30, font=("Arial", 12))

        self.criteria_var = tk.StringVar()
        self.cmbbx_criteria = ttk.Combobox(self.frm_sort_search, textvariable=self.criteria_var, font=("Arial", 12), width=15)
        self.cmbbx_criteria['state'] = "readonly"
        self.cmbbx_criteria['values'] = ["Name", "Course & Section", "Ticket No.", "Date"]
        self.cmbbx_criteria.set('Ticket No.')

        self.btn_search = ttk.Button(self.frm_sort_search, text="Search", command=lambda: self.update_list(True))

        # frm_tree_view components
        self.tree = ttk.Treeview(self.frm_tree_view, columns=("Ticket No.", "Name", "Course & Section", "Date"), show=" headings")

        self.tree.heading("Ticket No.", text="Ticket No.", anchor="center")
        self.tree.heading("Name", text="Name", anchor="center")
        self.tree.heading("Course & Section", text="Course & Section", anchor="center")
        self.tree.heading("Date", text="Date", anchor="center")

        self.tree.column("Ticket No.", width=50, anchor="center")
        self.tree.column("Name", width=200, anchor="w")
        self.tree.column("Course & Section", width=100, anchor="center")
        self.tree.column("Date", width=100, anchor="center")

        # frm_crud components
        self.add_icon = tk.PhotoImage(file="images/add_icon.png")
        self.update_icon = tk.PhotoImage(file="images/update_icon.png")
        self.remove_icon = tk.PhotoImage(file="images/remove_icon.png")

        self.btn_add = ttk.Button(self.frm_crud, text="Add", width=15, image=self.add_icon, compound="top", command=lambda: ppup.Add_Entry_Window(self))
        self.btn_update = ttk.Button(self.frm_crud, text="Update", width=15, image=self.update_icon, compound="top", command=self.call_update_window)
        self.btn_delete = ttk.Button(self.frm_crud, text="Delete", width=15, image=self.remove_icon, compound="top", command=self.delete_func)

        # frm_misc components
        self.btn_export_img = ttk.Button(self.frm_misc, text="Export Tickets", width=15, command=self.export_all_tickets)
        self.btn_export_xls = ttk.Button(self.frm_misc, text="Export Data", width=15, command=self.export_xlsx)
        self.btn_logout = ttk.Button(self.frm_misc, text="Logout", width=15, command=self.logout)

        # settings button
        self.settings_icon = tk.PhotoImage(file="images/settings.png")
        self.btn_settings = ttk.Button(self.frm_main, image=self.settings_icon, style="Mini_icons.TButton", command=lambda: ppup.Settings(self))

        # reset button
        self.reset_icon = tk.PhotoImage(file="images/reset.png")
        self.btn_reset = ttk.Button(self.frm_main, image=self.reset_icon, style="Mini_icons.TButton", command=self.reset_all)

        # ticket count label
        self.lbl_ticket_count = ttk.Label(self.frm_main, text=f"Tickets:\n{0:5d}", style="Count.TLabel")

        # configure frm_main row and columns
        self.frm_main.grid_rowconfigure(0, weight=1)
        self.frm_main.grid_rowconfigure(1, minsize=200, weight=1)
        self.frm_main.grid_rowconfigure(2, minsize=200, weight=1)
        self.frm_main.grid_rowconfigure(3, minsize=200, weight=1)
        self.frm_main.grid_rowconfigure(4, weight=1)

        self.frm_main.grid_columnconfigure(0, minsize=200, weight=1)
        self.frm_main.grid_columnconfigure(1, minsize=200, weight=1)
        self.frm_main.grid_columnconfigure(2, minsize=200, weight=1)
        self.frm_main.grid_columnconfigure(3, minsize=200, weight=1)
        self.frm_main.grid_columnconfigure(4, minsize=200, weight=1)
        self.frm_main.grid_columnconfigure(5, minsize=5, weight=1)
        self.frm_main.grid_columnconfigure(6, minsize=150, weight=1)

        # pack frame and components
        self.frm_main.pack(padx=20, pady=20)

        # pack settings, reset button, and ticket count label
        self.btn_settings.place(x=350, y=645)
        self.btn_reset.place(x=395, y=645)
        self.lbl_ticket_count.place(x=1070, y=400)

        # pack frm_sort_search and children
        self.frm_sort_search.grid(row=0, column=0, columnspan=5, sticky="nsew")

        self.ent_search.grid(row=0, column=0, padx=(0, 10))
        self.cmbbx_criteria.grid(row=0, column=1, padx=(0, 10))
        self.btn_search.grid(row=0, column=2)        

        # pack frm_tree_view and child
        self.frm_tree_view.grid(row=1, column=0, rowspan=3, columnspan=5, sticky="nsew", pady=5)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # pack frm_crud and children
        self.frm_crud.grid(row=1, column=6, rowspan=3, sticky="nsew")

        self.btn_add.grid(row=0, column=0, padx=10, pady=(0, 5)) #entire column will follow, no need additional padx
        self.btn_update.grid(row=1, column=0, pady=5)
        self.btn_delete.grid(row=2, column=0, pady=5)

        # pack frm_misc and children
        self.frm_misc.grid(row=4, column=0, columnspan=7, sticky="nsew")

        # configure frm_misc columns
        self.frm_misc.grid_columnconfigure(2, weight=1)

        self.btn_export_img.grid(row=0, column=0, padx=(0, 5), pady=10)
        self.btn_export_xls.grid(row=0, column=1, padx=5)
        self.btn_logout.grid(row=0, column=3, padx=(0, 10))

        self.tree.bind("<<TreeviewSelect>>", self.update_buttons_state)
        self.tree.bind("<Double-1>", self.export_ticket)
        self.check_event_config()
        self.update_list()


    def update_list(self, active: bool = False):
        search = None
        filter = None
        if active:
            search = self.ent_search.get()
            criteria = self.cmbbx_criteria.get()
            if criteria == "Name":
                filter = "name"
            if criteria == "Course & Section":
                filter = "course_section"
            if criteria == "Ticket No.":
                filter = "ticket_no"
            if criteria == "Date":
                filter = "date"
                if search:
                    search = search.split("/")
                    search = f"{search[2]}-{search[0]}-{search[1]}"

        for item in self.tree.get_children():
            self.tree.delete(item)
        list_data = self.dataManager.get_data(filter, search)

        ticket_count = len(list_data) if list_data else 0

        if list_data:
            for i in range(len(list_data)):
                vals = (f"{list_data[i][0]:06d}", list_data[i][1], list_data[i][2], list_data[i][3].strftime("%m/%d/%Y"))
                self.tree.insert("", tk.END, values=vals)
        self.lbl_ticket_count.config(text=f"Tickets:\n{ticket_count:5d}")

        self.update_buttons_state(None)

    def update_buttons_state(self, event):
        selection = self.tree.selection()
        if selection:
            self.btn_update.config(state=tk.NORMAL)
            self.btn_delete.config(state=tk.NORMAL)
        else:
            self.btn_update.config(state=tk.DISABLED)
            self.btn_delete.config(state=tk.DISABLED)

    def delete_func(self):
        selection = self.tree.selection()
        if selection:
            confirm = messagebox.askyesno("Delete Entry", "Do you want to permanently delete the selected item?", icon="warning", parent=self)
            if confirm:
                ticket_number = self.tree.item(selection, "values")[0].lstrip('0')
                self.dataManager.delete_ticket_entry(ticket_number)
        self.update_list()

    def call_update_window(self):
        selection = self.tree.selection()
        if selection:
            ticket_number = self.tree.item(selection, "values")[0].lstrip('0')
            ppup.Update_Entry_Window(ticket_number, self)

    def check_event_config(self):
        data = self.dataManager.get_evnt_config()
        if data:
            self.event_name = data[0]
            self.event_venue = data[1]
            self.event_date = data[2]
            self.event_time = [data[3], data[4]]
            print(self.event_name, self.event_venue, self.event_date, self.event_time)
        else:
            self.wait_window(ppup.Settings(self))
            if not self.dataManager.get_evnt_config():
                messagebox.showerror("Configuration Required", "No configurations were provided. The main dashboard cannot operate without proper setup.\n\nThe application will now close.\n\nPlease re-open and configure before proceeding.", parent=self)
                self.destroy()

    def export_xlsx(self):
        confirmation = messagebox.askquestion("Export to xlsx", "Export all data to Excel?")
        if confirmation == "yes":
            try:
                sort_popup = ppup.Excel_Sort(self)
                self.wait_window(sort_popup)
                choice_filter = sort_popup.result
                file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                         filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
                                                         title="Save Excel File",
                                                         initialfile="tickets.xlsx")
                if not file_path:
                    return
                if choice_filter:
                    exp.create_excel_sheet(self.dataManager, choice_filter, file_path)
                    ppup.simulate_progress(self)
            except Exception as e:
                print("Something happened:", e)
                messagebox.showerror("Error", "Something went wrong.")

    def export_all_tickets(self):
        confirmation = messagebox.askquestion("Export tickets", "Export all entries into tickets?")

        if confirmation == "yes":
            try:
                folder_path = filedialog.askdirectory()

                if not folder_path:
                    return

                formatted_event_date = datetime.strptime(self.event_date, "%m/%d/%Y").strftime("%B %d, %Y")
                formatted_event_time = [datetime.strptime(self.event_time[0], "%H:%M").strftime("%I:%M %p"), datetime.strptime(self.event_time[1], "%H:%M").strftime("%I:%M %p")]

                txp.create_ticket_image(self.dataManager, self.event_name, self.event_venue, formatted_event_date, formatted_event_time, folder_path, 1)
                messagebox.showinfo("Export Successful", "All entries have been successfully imported.", parent=self)

            except Exception as e:
                print("Something happened:", e)
                messagebox.showerror("Error", "Something went wrong.")

    def export_ticket(self, event):
        selection = self.tree.selection()
        if selection:
            ticket_number = self.tree.item(selection, "values")[0].lstrip('0')

            formatted_event_date = datetime.strptime(self.event_date, "%m/%d/%Y").strftime("%B %d, %Y")
            formatted_event_time = [datetime.strptime(self.event_time[0], "%H:%M").strftime("%I:%M %p"), datetime.strptime(self.event_time[1], "%H:%M").strftime("%I:%M %p")]

            img = txp.create_ticket_image(self.dataManager, self.event_name, self.event_venue, formatted_event_date, formatted_event_time, None, 2, ticket_number)
            ppup.PreviewTicketWindow(img, ticket_number, [self.event_name, self.event_venue, formatted_event_date, formatted_event_time], self)

    def reset_all(self):
        reset = messagebox.askyesno("Confirm Reset", "This action will delete all entries and configurations.\nPlease ensure that you have backed up your data.\nDo you want to proceed?", icon="warning", parent=self)

        if reset:
            self.dataManager.delete_multiple(2)
            self.update_list()
            
            self.dataManager.delete_evnt_config()
            self.event_name = None
            self.event_venue = None
            self.event_date = None
            self.event_time = None
            self.check_event_config()

    def logout(self):
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?", icon="question", parent=self)
        if confirm:
            self.tree.unbind("TreeviewSelect")
            self.dataManager.log_in_out(0)
            self.destroy()
            LoginWindow().mainloop()


LoginWindow().mainloop()