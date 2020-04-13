import stock_pick
from tkinter import *
import urllib


#
#   stock_pick_gui.py V.2
#   DD 1318 @ KTH
#   For P-assignment 2020
#
#   GUI for stock_pick.py program
#   In v.2 I have implementd the feature to add stocks by type in the stock shortening like "tsla" for Tesla inc.
#   I have also removed the update button because of simplicity reasons. The program is not aimd towards realtime traders.
#
#   Author Tom K. Axberg
#   Last edit 13.04.06
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
                               text="Add Stock",
                               command=self.add_stock)
        self.bttn_add.grid(row=20, column=5, sticky=E)
        self.bttn_add = Button(self,
                               text="Information",
                               command=self.information)
        self.bttn_add.grid(row=21, column=5, sticky=E)
        self.bttn_add = Button(self,
                               text="  Exit  ",
                               command=self.master.quit)
        self.bttn_add.grid(row=22, column=5, sticky=E)


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
        Used to print out the available stocks and options information in text box 1.
        :return: nothing
        '''

        self.output_txt_1.delete(0.0, END)
        self.output_txt_1.insert(0.5, "\nCurrent time period: " + str(self.days) + " days.\n")
        self.output_txt_1.insert(0.5, "\nOption 3:\nSorted list of available stocks by their beta value\n")
        self.output_txt_1.insert(0.5, "\nOption 2:\nTechnical analysis (Short term)\n")
        self.output_txt_1.insert(0.5, "------------\nOption 1: Fundamental analysis (Long term)\n")
        for stock in stock_pick.stock_list:
            if(stock.fullname == ""):
                self.output_txt_1.insert(0.5, str(stock.name + "\n"))
            else:
                self.output_txt_1.insert(0.5, str(stock.fullname + "\n"))
        self.output_txt_1.insert(0.5, "Available Stocks:\n------------\n")

    def welcome(self):
        """
        Welcome message. Used when the program starts. (Creates an instance of the class)
        :return: nothing
        """
        self.output_txt_2.insert(0.5, "Welcome to the stock picking guide!\n\n"
                                      "Information:\n\n"
                                      "Options can be executed on the stocks showing to the left.\n"
                                      "Please type in the stock of choice in the type field and select an option.\n\n"
                                      "If the stock you are looking for is not in the list,"
                                      " simply add it by typing the stock shortening (Tesla inc. -> tsla) and pressing -Add Stock-! \n\n"
                                      "Good luck!"
                                 )

    def add_stock(self):
        '''
        Used to add stocks. Because of that data is fetched from multiple sources all stocks at one sourcs
        may not be avaliable at another and from that a naiv exception handeling has been implemmented.
        :return: nothing
        '''
        try:
            in_list = False
            if self.entry.get() != "":
                for stock in stock_pick.stock_list:
                    print(stock.name)
                    if stock.name == str(self.entry.get()).upper():
                        in_list = True
                    print(in_list)
                if not in_list:
                    stock_pick.stock_list.append(stock_pick.Stock(self.entry.get()))
                    stock_pick.stock_list[-1].get_data_from_modules(self.days)
                    self.output_txt_2.delete(0.0, END)
                    self.output_txt_2.insert(0.5, "\nStock was successfully added!\n")
                    self.get_stocks()
                elif in_list:
                    self.output_txt_2.insert(0.5, "\nStock is already available.\n")
            elif self.entry.get() == "":
                self.output_txt_2.delete(0.0, END)
                self.output_txt_2.insert(0.5, "\nPlease input a stock.\n\n")
            else:
                self.output_txt_2.insert(0.5, "\nStock not found or could not get all data.\n\nAre you sure that you typed in a valid stock name?\n\n")
        except ValueError as error:
            self.output_txt_2.delete(0.0, END)
            self.output_txt_2.insert(0.5, "\nStock not found or could not get all data.\n\nAre you sure that you typed in a valid stock name?\n\n")
            del stock_pick.stock_list[-1] # Removes the stock that did not have all necessary data
        except IndexError as error:
            self.output_txt_2.delete(0.0, END)
            self.output_txt_2.insert(0.5, "\nStock not found or could not get all data.\n\nAre you sure that you typed in a valid stock name?\n\n")
            del stock_pick.stock_list[-1] # Removes the stock that did not have all necessary data
        except TypeError as error:
            self.output_txt_2.delete(0.0, END)
            self.output_txt_2.insert(0.5, "\nStock not found or could not get all data.\n\nAre you sure that you typed in a valid stock name?\n\n")
            del stock_pick.stock_list[-1] # Removes the stock that did not have all necessary data
        except urllib.error.HTTPError as error:
            self.output_txt_2.delete(0.0, END)
            self.output_txt_2.insert(0.5, "\nStock not found or could not get all data.\n\nAre you sure that you typed in a valid stock name?\n\n")
            del stock_pick.stock_list[-1] # Removes the stock that did not have all necessary data
        finally:
            self.entry.delete(0, END)


    def information(self):
        """
        Information message. Used when the user wants info on how to use the program.
        :return: nothing
        """
        self.output_txt_2.delete(0.0, END)
        self.output_txt_2.insert(0.5, "Information:\n\n"
                                      "Options can be executed on the stocks showing to the left.\n"
                                      "Please type in the stock of choice in the type field and select an option.\n\n"
                                      "If the stock you are looking for is not in the list,"
                                      " simply add it by typing the stock shortening (Tesla inc. -> tsla) and pressing -Add Stock-! \n\n"
                                      "Good luck!"
                                      )

    def updater(self):
        """
        Used to update data from fresh files downloaded from nasdaq.
        :return: nothing
        """
        try:
            if len(self.entry.get()) == 0:
                self.days = 30
            elif type(self.entry.get()) == int:
                self.days = int(self.entry.get())
                my_app.get_stocks()
            else:
                self.output_txt_2.delete(0.0, END)
                new_stock_list = stock_pick.data_files_updater()
                for stock in stock_pick.stock_list:
                    for item in new_stock_list:
                        if stock.name == item.name:
                            stock_pick.stock_list[stock_pick.stock_list.index(stock)] = item
                        else:
                            stock.get_data_from_fa_module(self.days)
                stock_pick.stock_attributes_updater(self.days)
                self.get_stocks()
                self.output_txt_2.insert(0.5, "All data was successfully updated!\n\n"
                                              "Options can be executed on the stocks showing to the left.\n\n"
                                              "Please type in the choise in the type field and select an option.")
        except ValueError as error:
            self.output_txt_2.insert(0.5, "Input not valid")
        finally:
            self.entry.delete(0, END)
            print(type(self.entry.get()))
        my_app.get_stocks()



    def option_1(self):
        """
        Used when fundamental analysis is selected (option 1).
        :return: nothing
        """
        try:
            if len(self.entry.get()) != 0:
                self.output_txt_2.delete(0.0, END)
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
            else:
                self.output_txt_2.delete(0.0, END)
                self.output_txt_2.insert(0.5, "\nPlease type in the stock of choice.\n\n")
        except AttributeError as error:
            self.output_txt_2.insert(0.5, "Stock is not available.\n\n")

    def option_2(self):
        '''
        Used when technical analysis is selected (option 2).
        :return: nothing
        '''
        try:
            if len(self.entry.get()) != 0:
                self.output_txt_2.delete(0.0, END)
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
            else:
                self.output_txt_2.delete(0.0, END)
                self.output_txt_2.insert(0.5, "\nPlease type in the stock of choice.\n\n")
        except AttributeError as error:
            self.output_txt_2.insert(0.5, "Stock is not available.\n\n")

    def option_3(self):
        """
        Used when sorted beta list is selected (option 3).
        :return: nothing
        """
        try:
            self.output_txt_2.delete(0.0, END)
            for item in sorted(stock_pick.stock_list, reverse=True):
                self.output_txt_2.insert(0.5,
                                         str(stock_pick.stock_list[stock_pick.stock_list.index(item)].name) +
                                         " " + str(stock_pick.stock_list[stock_pick.stock_list.index(item)].beta)
                                         + "\n\n")
            self.output_txt_2.insert(0.5, "\nSorted stocks by beta value:\n\n")
        except AttributeError as error:
            self.output_txt_2.insert(0.5, "Stock is not available.\n\n")
        finally:
            self.entry.delete(0, END)


# ---------- SETTING UP THE MAIN WINDOW ---------


root = Tk()
stock_pick.stock_list = stock_pick.data_files_updater()
stock_pick.stock_attributes_updater(30)
root.title("The Stock Picking Guide")
root.geometry("450x550")
my_app = Application(root)

root.mainloop()
