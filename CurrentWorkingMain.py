from PyQt6 import QtWidgets, uic, QtGui, QtCore
from PyQt6.QtWidgets import QDialog, QApplication, QWidget,  QGridLayout, QListWidget,  QPushButton, QMainWindow, QLineEdit, QMessageBox, QInputDialog
import sys
import pyodbc

# server = 'LAPTOP-A8JSD84F' 
server = 'DESKTOP-4SMGNIQ\SPARTA' 
database = 'student club'  # Name of database
use_windows_authentication = True  # Set to True to use Windows Authentication
username = ''  # Specify a username if not using Windows Authentication
password = ''  # Specify a password if not using Windows Authentication


# Create the connection string based on the authentication method chosen
if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
def showTable(tableName):
    # displays the table you want on the terminal
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    # Execute the SQL query to get the current database name
    table_name = tableName

    # SQL query to select all records from the specified table
    table_query = f"SELECT * FROM {table_name}"

    try:
        # Execute the SQL query
        cursor.execute(table_query)

        # Fetch all records from the table
        rows = cursor.fetchall()

        # Display the records
        if rows:
            print(f"Contents of '{table_name}':")
            for row in rows:
                print(row)
        else:
            print(f"No records found in '{table_name}'")

    except pyodbc.Error as e:
        print(f"Error fetching data from '{table_name}': {e}")

    # Close the cursor and connection
    cursor.close()
    connection.close()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("registration_1.ui", self)
        self.show()
        
        self.pushButton.clicked.connect(lambda: self.CreateAcc(1)) #admin
        self.pushButton_2.clicked.connect(lambda: self.CreateAcc(2)) #student
        self.LoginButton.clicked.connect(self.login)
        
        
    def CreateAcc(self, enable_num):
        self.new_form = Registration(enable_num)
        self.new_form.show()
        
    def login(self):
        entered_ID = self.EnterID.text()
        entered_password = self.EnterPassword.text()
        global admin
        # so we can use the logged in user to show details
        global UserIDLoggedIn
        UserIDLoggedIn = entered_ID

        # Check if the entered credentials belong to an admin
        if self.check_admin_credentials(entered_ID, entered_password):
            admin = True
            self.DashBoard() #login/dashboard
        # Check if the entered credentials belong to a student
        elif self.check_student_credentials(entered_ID, entered_password):
            admin = False
            self.DashBoard() #login/dashboard
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def check_admin_credentials(self, AdminID, password):
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Execute a query to check if the credentials match an admin record
            query = "SELECT * FROM Admin WHERE AdminID = ? AND Password = ?"
            cursor.execute(query, (AdminID, password))

            # Fetch one row
            admin_record = cursor.fetchone()

            return admin_record is not None

        except Exception as e:
            print(f"Error checking admin credentials: {str(e)}")
            return False

        finally:
            if connection:
                connection.close()

    def check_student_credentials(self, StudentID, password):
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Execute a query to check if the credentials match a student record
            query = "SELECT * FROM Students WHERE StudentID = ? AND Password = ?"
            cursor.execute(query, (StudentID, password))

            # Fetch one row
            student_record = cursor.fetchone()

            return student_record is not None

        except Exception as e:
            print(f"Error checking student credentials: {str(e)}")
            return False

        finally:
            if connection:
                connection.close()  
        
        
    def DashBoard(self):
        self.new_form = DashBoard()
        self.new_form.show()
        self.close()

class Registration(QtWidgets.QMainWindow):
    def __init__(self, enable_num):
        super(Registration,self).__init__()
        uic.loadUi("create_acc_2.ui",self)
        self.show()
        
        self.enable_num = enable_num
        if enable_num == 1:
            self.groupBox.setEnabled(True)
            self.groupBox_2.setEnabled(False)
        elif enable_num == 2:
            self.groupBox.setEnabled(False)
            self.groupBox_2.setEnabled(True)
            
        self.PushButton_OK.clicked.connect(self.create_account)
            
    def create_account(self):
        if self.enable_num == 1:
                # Admin registration logic
                admin_id = self.Admin_ID.text()
                admin_username = self.Admin_Name.text()
                admin_password = self.Admin_Password.text()
                admin_email = self.Admin_Email.text()

                # Validate inputs if needed
                if not (admin_id.isdigit() and admin_username and admin_password and '@' in admin_email):
                    print("Invalid input. Please check your admin details.")
                    QMessageBox.information(self, "Failure", "Kindly re-Check details")
                    return  # Exit the function if validation fails

                # Insert data into the Admin table
                self.insert_admin_data(admin_id, admin_username, admin_password, admin_email)

        elif self.enable_num == 2:
                # Student registration logic
                student_name = self.Student_Name.text()
                student_ID = self.Student_ID.text()
                student_password = self.Student_Password.text()
                student_email = self.Student_Email.text()
                student_batch = self.Student_Batch.text()

                # Validate inputs if needed
                if not (student_name and student_ID.isdigit() and student_password and '@' in student_email and student_batch.isdigit()):
                    print("Invalid input. Please check your student details.")
                    QMessageBox.information(self, "Failure", "Kindly re-Check details")
                    return  # Exit the function if validation fails

                # Insert data into the Students table (you'll need to implement this)
                self.insert_student_data(student_name, student_ID, student_password, student_email,student_batch)
                
    def insert_admin_data(self, admin_id, username, password, email):
        try:
                connection = pyodbc.connect(connection_string)
                cursor = connection.cursor()

                # Assuming the Admin table has columns AdminID, Username, Password
                # You may need to adjust this query based on your actual table structure
                query = f"INSERT INTO Admin (AdminID, Username, Password, email) VALUES (?, ?, ?, ?)"
                cursor.execute(query, (admin_id, username, password, email))
                connection.commit()

                QMessageBox.information(self, "Success", "Admin account created successfully!")

        except Exception as e:
                QMessageBox.critical(self, "Error", f"Error creating admin account: {str(e)}")

        finally:
                if connection:
                    connection.close() 
    def insert_student_data(self, student_id, username, password, email,batch):
        try:
                connection = pyodbc.connect(connection_string)
                cursor = connection.cursor()

                # Assuming the Admin table has columns AdminID, Username, Password
                # You may need to adjust this query based on your actual table structure
                query = f"INSERT INTO Students (Name, StudentID, Password, Email, Batch) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(query, (student_id, username, password, email, batch))
                connection.commit()

                QMessageBox.information(self, "Success", "Student account created successfully!")

        except Exception as e:
                QMessageBox.critical(self, "Error", f"Error creating student account: {str(e)}")

        finally:
                if connection:
                    connection.close()    
            
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
            self.pushButton.setEnabled(True)
        else:
            self.pushButton_4.setEnabled(False)
            self.pushButton.setEnabled(False)
            
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
        
        self.MembersButton.clicked.connect(self.MembersCall)
        
        if admin == True: #once again global admin used.
            self.FundsButton.setEnabled(True)
            self.FundsButton.clicked.connect(self.showInputDialog)
        else:
            self.FundsButton.setEnabled(False)
    
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