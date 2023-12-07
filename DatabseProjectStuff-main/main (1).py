from PyQt6 import QtWidgets, uic, QtGui, QtCore
from PyQt6.QtWidgets import QDialog, QApplication, QWidget,  QGridLayout, QListWidget,  QPushButton, QMainWindow, QLineEdit, QMessageBox, QInputDialog
import sys
import pyodbc

server = 'DESKTOP-4SMGNIQ' 
database = 'student club'  # Name of database
use_windows_authentication = True  # Set to True to use Windows Authentication
username = ''  # Specify a username if not using Windows Authentication
password = ''  # Specify a password if not using Windows Authentication


# Create the connection string based on the authentication method chosen
if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'


admin = True
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("registration_1.ui", self)
        self.show()
        
        self.pushButton.clicked.connect(lambda: self.CreateAcc(1)) #admin
        self.pushButton_2.clicked.connect(lambda: self.CreateAcc(2)) #student
        self.pushButton_3.clicked.connect(self.DashBoard) #login/dashboard
        
    def CreateAcc(self, enable_num):
        self.new_form = Registration(enable_num)
        self.new_form.show()
    def DashBoard(self):
        self.new_form = DashBoard()
        self.new_form.show()
        self.close()

class Registration(QtWidgets.QMainWindow):
    def __init__(self, enable_num):
        super(Registration,self).__init__()
        uic.loadUi("create_acc_2.ui",self)
        self.show()
        
        if enable_num == 1:
            self.groupBox.setEnabled(True)
            self.groupBox_2.setEnabled(False)
        elif enable_num == 2:
            self.groupBox.setEnabled(False)
            self.groupBox_2.setEnabled(True)
            
        #need to add logic for differentiating between admin logging in or student logging in. right now global is used.

class DashBoard(QtWidgets.QMainWindow):
    def __init__(self):
        super(DashBoard,self).__init__()
        uic.loadUi("dashboard_3.ui",self)
        self.show()
        
        self.connection_string = connection_string
        self.load_events_data()
        self.load_clubs_data()  # Call the method to load club data
        
        if admin == True: #if condition for the add(admin only) for creating club.
            self.pushButton_4.setEnabled(True)
        else:
            self.pushButton_4.setEnabled(False)
            
        self.pushButton_5.clicked.connect(self.ClubDetails)
        self.pushButton_4.clicked.connect(self.ClubCreation)
        self.pushButton.clicked.connect(self.EventCreation)
        self.tableWidget.itemClicked.connect(self.EventDetails)
        
    def load_events_data(self): #function to display events in events table.
        try:
            connection = pyodbc.connect(self.connection_string)
            cursor = connection.cursor()

            # retrieving data from the events table.
            cursor.execute("SELECT EventID, EventName, Description, EventDate FROM Events")
            data = cursor.fetchall()

            # populate tableWidget with the retrieved data
            self.tableWidget.setRowCount(len(data))
            self.tableWidget.setColumnCount(len(data[0]) if data else 0)
            
            for row_num, row_data in enumerate(data):
                for col_num, col_data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(col_data))
                    self.tableWidget.setItem(row_num, col_num, item)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error fetching data from database: {str(e)}")
        
        finally:
            if connection:
                connection.close()
                
    def load_clubs_data(self): #function to display the clubs in club list widget.
        try:
            connection = pyodbc.connect(self.connection_string)
            cursor = connection.cursor()

            # retrieve club names from the Clubs table
            cursor.execute("SELECT ClubName FROM Clubs")
            data = cursor.fetchall()

            # populates the listWidget with the retrieved club names
            self.listWidget.clear()  # Clear existing items
            for row_data in data:
                club_name = row_data.ClubName  # Assuming the column name is ClubName
                item = QtWidgets.QListWidgetItem(club_name)
                self.listWidget.addItem(item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error fetching club data from database: {str(e)}")

        finally:
            if connection:
                connection.close()

        
    def ClubDetails(self):
        self.new_form = ClubDetails()
        self.new_form.show()
        
    def ClubCreation(self):
        self.new_form = ClubCreation()
        self.new_form.show()
        
    def EventCreation(self):
        self.new_form = ClubEvent()
        self.new_form.show()
        
    def EventDetails(self):
        self.new_form = ViewEvent()
        self.new_form.show()
    
class ClubDetails(QtWidgets.QMainWindow):
    def __init__(self):
        super(ClubDetails,self).__init__()
        uic.loadUi("club details.ui",self)
        self.show()
        
        self.pushButton.clicked.connect(self.MembersCall)
        
        if admin == True: #once again global admin used.
            self.pushButton_2.setEnabled(True)
            self.pushButton_2.clicked.connect(self.showInputDialog)
        else:
            self.pushButton_2.setEnabled(False)
    
    def MembersCall(self):
        self.new_form = ClubMembers()
        self.new_form.show()
    def showInputDialog(self): #using this to take club funds input.
        text, ok = QInputDialog.getText(self, 'Club Funds', 'Enter Amount:')
        
        

class ClubCreation(QtWidgets.QMainWindow):
    def __init__(self):
        super(ClubCreation,self).__init__()
        uic.loadUi("Club_Registration_4.ui",self)
        self.show()
        
class ClubEvent(QtWidgets.QMainWindow):
    def __init__(self):
        super(ClubEvent,self).__init__()
        uic.loadUi("create_Event.ui",self)
        self.show()

class ViewEvent(QtWidgets.QMainWindow):
    def __init__(self):
        super(ViewEvent,self).__init__()
        uic.loadUi("view_event.ui",self)
        self.show()
        
class ClubMembers(QtWidgets.QMainWindow):
    def __init__(self):
        super(ClubMembers,self).__init__()
        uic.loadUi("club_members_screen.ui",self)
        self.show()
        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()