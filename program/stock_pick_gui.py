import stock_pick
from tkinter import *


#
#   stock_pick.py
#   DD 1318 @ KTH
#   For P-assignment 2020
#
#   GUI for stock_pick program
#
#   Author Tom K. Axberg
#   Last edit 27.03.06
#   Contact: taxberg@kth.se
# _____________________________________________________________


class Application(Frame):

    def __init__(self, master):
        """
        creates a frame with widgets, a welcome message and the available stocks
        :param master: The parameter used to represent the parent window.
        """
        Frame.__init__(self, master)
        self.days = 30
        self.grid()
        self.create_widgets()
        self.welcome()
        self.get_stocks()

    # ---------- THIS IS WHERE ALL THE GUI ITEMS ARE CREATED ---------
    def create_widgets(self):

        # Lables and buttons for navigation

        self.bttn_add = Button(self,
                               text="Option 1",
                               command=self.option_1)
        self.bttn_add.grid(row=3, column=2, sticky=W)
        self.bttn_add = Button(self,
                               text="Option 2",
                               command=self.option_2)
        self.bttn_add.grid(row=3, column=3, sticky=W)
        self.bttn_add = Button(self,
                               text="Option 3",
                               command=self.option_3)
        self.bttn_add.grid(row=3, column=4, sticky=W)
        self.bttn_add = Button(self,
                               text="  Update  ",
                               command=self.update)
        self.bttn_add.grid(row=22, column=5, sticky=E)
        self.bttn_add = Button(self,
                               text="Information",
                               command=self.information)
        self.bttn_add.grid(row=23, column=5, sticky=E)
        self.bttn_add = Button(self,
                               text="  Exit  ",
                               command=self.master.quit)
        self.bttn_add.grid(row=24, column=5, sticky=E)


        Label(self, text="Type field").grid(row=0, column=2, columnspan=3)

        self.entry = Entry(self)
        self.entry.grid(row=2, column=2, sticky=W, columnspan=3)

        # Text fields for information
        # Text box 1. Standing text field to the left
        self.output_txt_1 = Text(self, width=20, height=35, wrap=WORD)
        self.output_txt_1.grid(row=7, column=1, columnspan=1, rowspan=20)
        # Text box 2. Message fieald in middle
        self.output_txt_2 = Text(self, width=40, height=15, wrap=WORD)
        self.output_txt_2.grid(row=5, column=2, columnspan=15, rowspan=10)

    # ---------- SOME HELPING FUNCTIONS ---------

    def get_stocks(self):
        '''
        Used to print out the available stocks and option information in text box 1.
        :return: nothing
        '''

        self.output_txt_1.delete(0.0, END)
        self.output_txt_1.insert(0.5, "\nCurrent time period: " + str(self.days) + " days.\n")
        self.output_txt_1.insert(0.5, "\nOption 3: Sorted list of available stocks by their beta value\n")
        self.output_txt_1.insert(0.5, "\nOption 2: Technical analysis (Short term)\n")
        self.output_txt_1.insert(0.5, "------------\nOption 1: Fundamental analysis (Long term)\n")
        for stock in stock_pick.stock_list:
            self.output_txt_1.insert(0.5, str(stock.name + "\n"))
        self.output_txt_1.insert(0.5, "Available Stocks:\n------------\n")

    def welcome(self):
        """
        Welcome message. Used when the program starts. (Creates an instance of the class)
        :return: nothing
        """
        self.output_txt_2.insert(0.5, "Welcome to the stock picking guide!\n\n"
                                      "Information:\n\n"
                                      "Options can be executed on the stocks showing to the left.\n\n"
                                      "Please type in the choise in the type field and select an option.\n\n"
                                      "If you want an other time period than 30 days, type in days in type field and "
                                      "press update!"
                                 )

    def information(self):
        """
        Information message. Used when the user wants info on how to use the program.
        :return: nothing
        """
        self.output_txt_2.insert(0.5, "Information:\n\n"
                                      "Options can be executed on the stocks showing to the left.\n\n"
                                      "Options can be executed on the stocks showing to the left.\n\n"
                                      "Please type in the choise in the type field and select an option.\n\n"
                                      "If you want an other time period than 30 days, type in days in type field and "
                                      "press update!")

    def update(self):
        """
        Used to update data from fresh files downloaded from nasdaq.
        :return: nothing
        """

        try:
            if self.entry.get() != "":
                self.days = int(self.entry.get())
                my_app.get_stocks()
            self.output_txt_2.delete(0.0, END)
            stock_pick.stock_list = stock_pick.data_files_updater()
            stock_pick.stock_data_updater(self.days)
            self.output_txt_2.insert(0.5, "All data was successfully updated!\n\n"
                                          "Options can be executed on the stocks showing to the left.\n\n"
                                          "Please type in the choise in the type field and select an option.")
        except ValueError as error:
            self.output_txt_2.insert(0.5, "Not a valid number of days. Please type in a positive integer.\n\n")
        except ZeroDivisionError as error:
            self.output_txt_2.insert(0.5, "There is no data for that period of days. Please update files or try "
                                          "with a shorter time period.\n\n")
            self.days = 30
            my_app.get_stocks()

        except IndexError as error:
            self.output_txt_2.insert(0.5, "There is no data for that period of days. Please update files or try "
                                          "with a shorter time period.\n\n")
            self.days = 30
            my_app.get_stocks()

    def option_1(self):
        """
        Used when fundamental analysis is selected (option 1).
        :return: nothing
        """
        try:
            stock = str(self.entry.get()).upper()
            print(str(stock))
            for item in stock_pick.stock_list:
                if stock == str(item.name).upper():
                    self.output_txt_2.insert(0.5,
                                             stock_pick.stock_list[
                                                 stock_pick.stock_list.index(item)].fundamental_analysis() + "\n\n")
                elif stock == str(item.name).upper().split("_")[0]:
                    self.output_txt_2.insert(0.5,
                                             stock_pick.stock_list[
                                                 stock_pick.stock_list.index(item)].fundamental_analysis() + "\n\n")
        except AttributeError as error:
            self.output_txt_2.insert(0.5, "Stock is not available.\n\n")

    def option_2(self):
        '''
        Used when technical analysis is selected (option 2).
        :return: nothing
        '''
        try:
            stock = str(self.entry.get()).upper()
            print(str(stock))
            for item in stock_pick.stock_list:
                if stock == str(item.name).upper():
                    self.output_txt_2.insert(0.5,
                                             stock_pick.stock_list[
                                                 stock_pick.stock_list.index(item)].technical_analysis(
                                                 self.days) + "\n\n")
                elif stock == str(item.name).upper().split("_")[0]:
                    self.output_txt_2.insert(0.5,
                                             stock_pick.stock_list[
                                                 stock_pick.stock_list.index(item)].technical_analysis(
                                                 self.days) + "\n\n")
        except AttributeError as error:
            self.output_txt_2.insert(0.5, "Stock is not available.\n\n")

    def option_3(self):
        """
        Used when sorted beta list is selected (option 3).
        :return: nothing
        """
        try:
            for item in sorted(stock_pick.stock_list, reverse=True):
                self.output_txt_2.insert(0.5,
                                         str(stock_pick.stock_list[stock_pick.stock_list.index(item)].name) +
                                         " " + str(stock_pick.stock_list[stock_pick.stock_list.index(item)].beta)
                                         + "\n\n")
        except AttributeError as error:
            self.output_txt_2.insert(0.5, "Stock is not available.\n\n")


# ---------- SETTING UP THE MAIN WINDOW ---------


root = Tk()
stock_pick.stock_list = stock_pick.data_files_updater()
root.title("The Stock Picking Guide")
root.geometry("450x550")
my_app = Application(root)

root.mainloop()
