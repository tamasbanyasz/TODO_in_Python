import customtkinter as ctk
import os.path
import csv


class Store:
    def __init__(self):
        self.DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.list_of_stored_days = []  # here do store the loaded days to updating

    def create_empty_csv_file(self):  # create first an empty csv file
        with open("todo_list.csv", "w") as empty_csv:
            csv_writer = csv.DictWriter(empty_csv, fieldnames=self.DAYS)
            csv_writer.writeheader()

    def csv_file_is_exist(self):  # if csv file does not exist
        if not os.path.exists("todo_list.csv"):
            self.create_empty_csv_file()

    def write_into_csv_at_first_time(self, csv_writer, day, text):  # firstly we have to write into csv file
        if not self.list_of_stored_days:
            csv_writer.writerow({day: text})

    # after fist time we wrote then we could update the text of the day in stored dictionary because its already loaded and stored
    def overwrite_text_of_the_day(self, text, day_name):
        for day in self.list_of_stored_days:
            day[day_name] = text

    def write_each_rows_into_csv(self, csv_writer):  # write the updated stored csv datas into csv
        for days in self.list_of_stored_days:
            csv_writer.writerow(days)

    def write_to_csv_file(self, text, day):  # writing method

        self.overwrite_text_of_the_day(text, day)

        with open("todo_list.csv", "w+") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.DAYS)
            csv_writer.writeheader()
            self.write_into_csv_at_first_time(csv_writer, day, text)
            self.write_each_rows_into_csv(csv_writer)

        # now we can see the first added text so we don't need to close the app and open it again
        self.read_from_csv_file()
        # but maybe there is another best way to handle it

    def read_from_csv_file(self):  # read the csv file
        with open("todo_list.csv", "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)  # read into dictionary
            self.list_of_stored_days = [days for days in csv_reader]  # store the dictionary in list


class SetInterface:
    def __init__(self, textbox, radio_str, current_day_label):
        self.class_store = Store()
        self.class_store.csv_file_is_exist()  # check the file is exist
        self.class_store.read_from_csv_file()  # then read from the file

        for days in self.class_store.list_of_stored_days:  # test print
            print(days)

        self.textbox = textbox
        self.radio_str = radio_str
        self.current_day_label = current_day_label

    def clear_textbox(self):
        self.textbox.delete("0.0", "end")
        self.current_day_label.configure(text=self.radio_str.get())

    def get_text_from_textbox(self):
        # take the text and the selected day to writing method
        self.class_store.write_to_csv_file(self.textbox.get('0.0', 'end'), self.radio_str.get())
        self.current_day_label.configure(text=f"Added to {self.radio_str.get()}")  # change the textbox label if we added a new text

    def insert_the_text_from_radiobutton(self):
        for day in self.class_store.list_of_stored_days:
            self.textbox.insert("0.0", day[self.radio_str.get()])  # insert the text into the textbox from selected day

    def display_text_by_selected_day(self):  # show the text from choosed radiobutton

        self.clear_textbox()

        self.current_day_label.configure(text=self.radio_str.get())  # show the selected day above the textbox

        self.insert_the_text_from_radiobutton()


class InterfaceOfTODO:

    ctk.set_appearance_mode("dark")  # set interface mode (light,dark)
    ctk.set_default_color_theme("green")

    def __init__(self):
        self.window = ctk.CTk()

        # Interface configs
        self.window.geometry("800x600")
        self.window.title("TODO")
        self.window.resizable(False, False)

        # RadioButton string value
        self.str = ctk.StringVar()

        # Frame around the day buttons
        self.frame = ctk.CTkFrame(self.window, corner_radius=10, height=400)

        # Days Label
        self.days_label = ctk.CTkLabel(master=self.frame, text='Days', fg_color="Black",
                                       font=('Ariel', 18), corner_radius=4, width=200)

        # Selected Day Label
        self.current_day_label = ctk.CTkLabel(master=self.window, text='Current Day', fg_color="Black", width=270,
                                              font=('Arial', 18), corner_radius=4)

        # TextBox
        self.textbox = ctk.CTkTextbox(master=self.window, height=433, width=270, font=('Times', 20))

        # Set Interface
        self.set_interface = SetInterface(self.textbox, self.str, self.current_day_label)

        # Buttons
        self.radio_buttons()
        self.add_button()

        # widget places
        self.textbox.place(x=10, y=38)
        self.days_label.place(x=0, y=1)
        self.current_day_label.place(x=10, y=10)
        self.frame.place(x=320, y=8)

        self.window.mainloop()

    def radio_buttons(self):  # create the seven radiobutton
        value_of_axis_y = 50
        for day in self.set_interface.class_store.DAYS:
            ctk.CTkRadioButton(master=self.frame, text=day, variable=self.str, value=day,
                               corner_radius=10, command=self.show_day).place(x=30, y=value_of_axis_y)

            value_of_axis_y += 40

    def add_button(self):

        submit_button = ctk.CTkButton(self.window, text='Add to day',
                                      command=lambda: self.set_interface.get_text_from_textbox(), font=('Arial', 16))
        submit_button.place(x=75, y=480)

    def show_day(self):
        self.set_interface.display_text_by_selected_day()


if __name__ == "__main__":
    gui = InterfaceOfTODO()
