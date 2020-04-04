import csv
import os

#
#   stock_pick.py
#   DD 1318 @ KTH
#   For P-assignment 2020
#
#   The program needs two folders in the same file as where the program exists.
#   One folder named data_files_in and one work_data_files.
#       - In data_files_in you save csv files from nasdaq just as they are.
#       - In the work_data_files folder the program will save necessary files.
#       - Fundamentals file needs to be updated manualy. This will be automated in v2.
#
#   If you se a variable "days" it is for further development. This verision does just handle time periods of 30 days.
#   Next verisione will give the user the ability to change time period.
#
#   NOTE: Program has been created from a given text with specified methods to go by. Like getting data from files.
#   To make the program flexible for fufure development I have decided to have more attributes to make it easier to
#   add calculation functions later.
#
#   Author Tom K. Axberg
#   Last edit 04.04.20
#   Contact: taxberg@kth.se
# _____________________________________________________________


# classes and methods

class Stock:
    """
    Stock is a stock with attributes specified below:
    Attributes:
    :param name:    Name of the stock 
    beta: 	        The Beta value
    movement:       Movement of stock the past 30 days
    high:           Highest price on stock the past 30 days
    low:            Lowest price on stock the past 30 days
    last:           Latest price on stock the past 30 days
    first:          Price on stock 30 days ago
    solidity:       Solidity of stock
    pe:             Price per earnings
    ps:             Price per sales
    """

    stock_list = []

    def __init__(self, name):
        """
        Creates instances of stocks. Why just the name is taken as a parameter is because all the other attributes are
        either calculated or fetched from files. This is because all other attributes, than the name, is going to change
        if the user whants to uptate the available stiocks data (attributes).
        :param name:
        """
        self.name = name
        self.stock_list.append(self)
        self.beta = 0
        self.movement = 0
        self.high = 0
        self.low = 0
        self.last = 0
        self.first = 0
        self.solidity = 0
        self.pe = 0
        self.ps = 0
        self.no_shares = 0

    def __lt__(self, other):
        """
        Used for the exsisting sorting algorithm ( sorted() ). Other is used to compare to. More info in python documentation
        :return: boolean for sorting algorithm
        """
        return self.beta > other.beta

    def fundamental_analysis(self):
        """
        Used to print out a fundamental analysis of the stock to the user
        :return: string of fundamental analysis
        """
        return "\nTechnical analysis - " + str(self.name) + "\n" \
                "\nThe solidity of the company is " + str(self.solidity) + " %" \
                "\nThe p/e value of the company is " + str(self.pe) + \
                "\nThe p/s value of the company is " + str(self.ps)

    def technical_analysis(self, days):
        """
        Used to print out a technical analysis of the stock to the user
        :return: string of technical analtsis
        """
        return "\nTechnical analysis - " + str(self.name) + "\n" \
                "\nMovement of the stock is " + str(self.movement) + "%" \
                "\nLowest price the past " + str(days) + " days is " + str(self.low) + \
                "\nHighest price the past " + str(days) + " days is " + str(self.high)


# Functions


def get_int_input(prompt_string):
    """
    Used to get an positive integer input from the user, asks again if input is not convertible to an integer or if
    it's negative.
    :param prompt_string: Message for the user
    :return: The inputed positive integer
    """

    done = False
    while not done:
        try:
            res = int(input(prompt_string))  # Result of input
            if 0 < res:  # Only if input is positive
                done = True
        except ValueError as error:
            print("Please type in an positive integer.")
        else:
            print("Please type in an positive integer.")
    return res


def data_files_updater():
    """
    Used to read all files in dir data_files_in and update/create the files in dir work_data_files folder.
    This is what the note is about in the beginning. It's specified from assignment to get data from three files uddated/created.
    Note: Third file is updated manualy. Will get automated in next verision.
    To make updates on these files I have chosen to use files fetched direktly from nasdaq. (Could have used json but
    i wanted to have a good sourse of data that didnt cost anything.)
    :return: a list of all available stocks.
    """

    function_specific_work_list = []  # Used to append all names of the stocks available in data_files_in dir.
    stock_list_out = []  # Used to append all created stocks instanses

    file_out_index = open("work_data_files/index.csv", 'w')  # First file created
    file_out_index.write("Format: date, index\n")
    file_out = open("work_data_files/movments.csv", 'w')  # Second file created
    file_out.write("Format: date, closeprice\n")

    for filename in os.listdir('data_files_in'):
        if filename == ".DS_Store":  # A hidden file (from macOS) in dir that is not readable.
            continue

        with open("data_files_in/" + filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            next(csv_reader)
            next(csv_reader)

            if filename.split("0")[0] == "_SE":  # _SE means that its the index file omxs30
                for line in csv_reader:
                    file_out_index.write(
                        str(line[0]) + ", " + ((str(line[3])).replace(",", ".") + "\n").replace(" ", ""))
            else:
                stock = filename.split("-")[0]  # all other files are stock dara files from nasdaq
                file_out.write(stock + "\n")
                function_specific_work_list.append(stock)
                for line in csv_reader:
                    file_out.write(
                        str(line[0]) + ", " + ((str(line[6])).replace(",", ".") + "\n").replace(" ", ""))
    file_out.close()
    file_out_index.close()

    for item in function_specific_work_list:
        stock_list_out.append(Stock(item))  # creating stocks and appends them in list

    return stock_list_out


def stock_data_updater(days):
    """
    Used to read from all files in dir work_data_files and update all available stock attributes with up to date data.
    :param days: How long the period is for calculating stocks attributes.
    :return: nothing
    """
    i = 0
    low = 0  # used to store lowest price on stock in stock csv file from nasdaq
    high = 0  # used to store highest price on stock in stock csv file from nasdaq
    values = [0, 0, 0, 0]  # array that is used to store values in during execution of this function

    with open("work_data_files/index.csv", 'r') as data:
        csv_reader = csv.reader(data)  # used to navigate through csv files
        next(csv_reader)
        for line in csv_reader:
            if i == 0:
                values[0] = (float(line[1]))
            if i == (days - 1):
                values[1] = (float(line[1]))
            i += 1

    i = 0  # reset i to 0

    for stock in stock_list:
        with open("work_data_files/movments.csv", 'r') as data1, open("work_data_files/fundamentals.txt", 'r') as data2:
            csv_reader = csv.reader(data1)  # used to navigate through csv files
            for line in csv_reader:
                if line[0].strip().upper() == stock.name.upper():
                    for row in csv_reader:
                        if i == 0:
                            high = float(row[1])
                            low = float(row[1])
                            values[2] = (float(row[1]))
                        if i == (days - 1):
                            values[3] = (float(row[1]))
                        if i <= (days - 1):
                            if low <= float(row[1]):
                                high = float(row[1])
                            elif high >= float(row[1]):
                                low = float(row[1])
                        i += 1
                    i = 0

            for row in data2:  # Reads fundamental data from specified file.
                if row.strip() == stock.name:
                    stock.solidity = float(data2.readline().strip())
                    stock.pe = float(data2.readline().strip())
                    stock.ps = float(data2.readline().strip())

            stock.movement = round(100 * ((values[2] - values[3]) / values[2]), 2)
            stock.beta = round((values[2] / values[3]) / (values[0] / values[1]), 3)
            stock.last = values[2]
            stock.first = values[3]
            stock.high = high
            stock.low = low


def available_stocks():
    """
    Used to display all available stocks.
    :return: nothing
    """
    i = 1
    for stock in stock_list:
        print(str(i) + " - " + stock.name)
        i += 1


def main():
    """
    Main program. Starts with a welcome message and then executes the menue.
    :return: nothing
    """
    print(
        "\n——————————-—————Welcome to the stock picking guide!——————————-————— \n   All data is not to be taken seriously. "
        "\n   Go with your gut.\n\nPlease press enter to start! ")
    input()
    menu()


def menu_choice():
    """
    Used to get input on what the user wants to do
    :return: an integer correspondning to the chosen menu option.
    """
    done = False

    while not done:
        res = get_int_input("Type in your choice here:\n> ")
        if res <= 4:
            done = True
        else:
            print("Your input is not a valid choice. Please type in an integer 1 - 4. \n")

    return res


def analysis_choice(prompt_string):
    """
    Used to display the available stocks and
    :param prompt_string:
    :return:
    """
    done = False
    while not done:
        try:
            i = 1
            print("\n" + prompt_string + "can be done on the following stocks:\n")
            for item in stock_list:
                print(str(i) + " - " + item.name)
                i += 1
            res = get_int_input("\nWhich stock do you want to analyse?\n> ")
            if res <= i - 1:
                done = True
            else:
                print("Your input is not a valid choice. Please type in an integer 1 -", len(stock_list), "\n")
        except IndexError as error:
            print("Your input is not a valid choice. Please type in an integer 1 -", len(stock_list), "\n")
    return res


def execute(choice, days):
    """
    Used to execute the option that the user chose.
    :param choice: an integer corresponding the the chosen option
    :return: (nothing)
    """
    if choice == 1:

        print(stock_list[analysis_choice("Fundamental analysis") - 1].fundamental_analysis())
        input("\nPlease press enter to continue.\n\n\n\n")
        menu()

    elif choice == 2:

        print(stock_list[analysis_choice("Technical analysis") - 1].technical_analysis(days))
        input("\nPlease press enter to continue.\n\n\n\n")
        menu()

    elif choice == 3:

        done = False
        i = 1
        while not done:
            try:
                print("\n—————Available stocks sorted by beta value———— \n")
                for stock in sorted(stock_list):
                    print(i, "-", stock.name, stock.beta)
                    i += 1
            except NameError as error:
                print("There are no avaliable stocks to sort.\n Please add stocks in to the program.")
            else:
                done = True
        input("\nPlease press enter to continue.\n\n\n\n")
        menu()

    elif choice == 4:
        exit()


def menu():
    """  	Used to display the menu:
    ———————--———-—————Meny——————————————————— 
    What would you like to do? 
    1 - Fundamental analysis (Long term)  
    2 - Technical analysis (Short term) 
    3 - List of available stocks by their beta value  
    4 - Exit
    Which alternative do you choose?
    And then execute the execute function with the menu_choice function so that the user can make a chioce.
    :return: (nothing)  
    """
    print(
        "\n——————————-—————Meny——————————————————— \n What would you like to do?\n\n 1 - Fundamental analysis (Long term)\n 2 - Technical analysis (Short term) "
        "\n 3 - List of available stocks by their beta value\n 4 - Exit\n")
    execute(menu_choice(), days=30)  # Execute the chioce of menu_choice


if __name__ == "__main__":
    stock_list = data_files_updater()
    stock_data_updater(30)
    main()
