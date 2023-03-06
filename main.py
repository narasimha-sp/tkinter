from tkinter import ttk
import tkinter as tk
import sqlite3
from tkcalendar import Calendar,DateEntry

# Create a tkinter window
def run_sqllitecommand(command):
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()
    # create the table if it doesn't exist
    cursor.execute(command)
    out = cursor.fetchall()
    conn.commit()
    conn.close()
    return out
def check_userexists():
    exist_query = "SELECT password FROM user WHERE USERNAME='" + username_entry.get() + "'"
    user_exist = run_sqllitecommand(exist_query)
    if len(user_exist) == 0:
        return False
    else:
        return True
def login_fields():
     if username_entry.get() == "":
         return "Username Field is empty"
     elif password_entry.get() == "":
         return "Password Field is empty"
     else:
         return "green"





# Create a function to handle the login button click
def register():
    query_user = '''CREATE TABLE IF NOT EXISTS user
                                         (uid int, username text, password text)'''
    run_sqllitecommand(query_user)

    user_exist = check_userexists()
    field_status = login_fields()
    if field_status != "green":
        message_label.config(text=field_status,foreground="red")
    elif user_exist:
        message_label.config(text="User already registered,kindly login", foreground="red")
    else:
        uid_query = "SELECT COUNT(uid) FROM user"
        uid = run_sqllitecommand(uid_query)
        print(uid)
        user_query = "INSERT INTO user (uid, username, password)VALUES ('" + str(
            uid[0][0]) + "','" + username_entry.get() + "','" + password_entry.get() + "')"
        print(user_query)
        run_sqllitecommand(user_query)
        message_label.config(text="User registered,kindly login", foreground="green")
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def guest():
    field_status = login_fields()
    if field_status == "Username Field is empty" :
        message_label.config(text=field_status, foreground="red")
    elif check_userexists():
        message_label.config(text="The Guest user already registered,kindly login", foreground="red")
    else:
        global user
        user = username_entry.get()
        for i in root.winfo_children():
            i.destroy()
        create_new_page()

def login():
    # Check if username and password are correct
    global user
    user = username_entry.get()
    pswd = run_sqllitecommand("SELECT password from user WHERE username="+"'"+user+"'")
    print(pswd)
    field_status = login_fields()
    if field_status != "green":
        message_label.config(text=field_status, foreground="red")
    elif len(pswd) == 0:
        message_label.config(text="User not registered or invalid Username", foreground="red")
    elif password_entry.get() == pswd[0][0] :
        # Clear the login page and create the new page
        for i in root.winfo_children():
            i.destroy()
        create_new_page()
    else:
        # Display an error message
        message_label.config(text="Invalid password",foreground="red")


# Create a function to create the new page
def create_new_page():

    def submit():
        if type_entry.get() == "":
            st="Vehicle type field is empty"
        elif number_entry.get() == "":
            st="Vehicle Number field is empty"
        elif model_entry.get() == "":
            st= "Vehicle Model field is empty"
        elif centre_entry.get() == "":
            st= "Sevice centre field is empty"
        elif date_entry.get() == "":
            st= "Appointment Date is empty"
        elif time_entry.get() == "":
            st= "Appointment Time is empty"
        else :
            st ="green"

        if st != "green":
            status.config(text=st,foreground="red")
        else:
            # connect to the vehicle table
            query_vehicle = '''CREATE TABLE IF NOT EXISTS vehicle
                                         (vid int, vehicle_type text, vehicle_model text,vehicle_number text)'''
            run_sqllitecommand(query_vehicle)

            vid_query = "SELECT COUNT(VID) FROM vehicle"
            vid = run_sqllitecommand(vid_query)
            print(vid)
            vehicle_query = "INSERT INTO vehicle (vid, vehicle_type, vehicle_model,vehicle_number)VALUES ('" + str(vid[0][0]) + "','" + type_entry.get() + "','" + model_entry.get() + "','" + number_entry.get() +  "')"
            print(vehicle_query)
            run_sqllitecommand(vehicle_query)

            # create the table if it doesn't exist
            query_booking ='''CREATE TABLE IF NOT EXISTS booking
                                 (bid int,username text, vid, service_centre text, time text, date text)'''
            run_sqllitecommand(query_booking)

            query_BID = "SELECT COUNT(bid) FROM booking"
            bid = run_sqllitecommand(query_BID)
            print(bid)
            query4 = "INSERT INTO booking (bid, username, vid, service_centre,time,date)VALUES ('"+str(bid[0][0])+"','"+ user+"','"+ str(vid[0][0])+"','"+centre_entry.get()+"','" +time_entry.get()+"','"+date_entry.get()+"')"
            run_sqllitecommand(query4)
            # commit the changes and close the connection
            # clear the input fields
            type_entry.delete(0, tk.END)
            number_entry.delete(0, tk.END)
            model_entry.delete(0, tk.END)
            centre_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)
            time_entry.delete(0, tk.END)
            status.config(text="Booking Details updated.",foreground="green")
    for i in root.winfo_children():
        i.destroy()

    loginpage_button = tk.Button(root, text="Previous", command=user_login1,justify="left",background="#887FF3")
    loginpage_button.pack(side="top")

    root.title("Vehicle Service Appointment")
    root.geometry("400x300")

    # create the input fields
    page_label = tk.Label(root, text="Vehicle Details", height=4, font=("Arial Bold", 20),background="#EEC3E6")
    page_label.pack()
    type_label = tk.Label(root, text="Vehicle Type", height=2, background="#EEC3E6",font=("Arial", 12))
    type_label.pack()
    # Provide drop down values for Vehicle type here

    type_entry = ttk.Combobox(root, values=("two-wheeler","Four-Wheeler","Commerical"))
    type_entry.pack()

    label1 = tk.Label(root, text='', state='disabled', background="#EEC3E6")
    label1.pack()

    model_label = tk.Label(root, text="Vehicle Model", height=2,background="#EEC3E6",font=("Arial", 12))
    model_label.pack()
    model_entry = tk.Entry(root,width=23)
    model_entry.pack()

    label2 = tk.Label(root, text='', state='disabled', background="#EEC3E6")
    label2.pack()

    number_label = tk.Label(root, text="Vehicle Number", height=2,background="#EEC3E6",font=("Arial", 12))
    number_label.pack()
    number_entry = tk.Entry(root,width=23)
    number_entry.pack()

    label3= tk.Label(root, text='', state='disabled', background="#EEC3E6")
    label3.pack()

    centre_label = tk.Label(root, text="Service Centre", height=2,background="#EEC3E6",font=("Arial", 12))
    centre_label.pack()
    centre_entry = ttk.Combobox(root, values=("pune","hyderabad","Bengaluru","Vizag"))
    centre_entry.pack()

    label4 = tk.Label(root, text='', state='disabled', background="#EEC3E6")
    label4.pack()
    date_label = tk.Label(root, text="Appointment date", height=2,background="#EEC3E6",font=("Arial", 12))
    date_label.pack()
    date_entry = DateEntry(root, width= 20, background= "magenta3", foreground= "white")
    date_entry.pack(pady=7)

    label5 = tk.Label(root, text='', state='disabled', background="#EEC3E6")
    label5.pack()

    time_label = tk.Label(root, text="Appointment Time", height=2,background="#EEC3E6",font=("Arial", 12))
    time_label.pack()
    time_entry = tk.Entry(root,width=23)
    time_entry.pack()

    label = tk.Label(root, text='', state='disabled',background="#EEC3E6")
    label.pack()

    # create the submit button
    submit_button = tk.Button(root, text="Confirm", command=submit, width=15,height=2,background="#887FF3")
    submit_button.pack()

    status = tk.Label(root, text='', state='disabled',background="#EEC3E6")
    status.pack()
# Create a function to create the welcome page
def user_login1():
    for i in root.winfo_children():
        i.destroy()
    global loginpage_label,username_label,message_label,username_entry,password_entry,login_button,guest_button,password_label,register_button
    root.title("Login Page")
    # root.config(bg="#00FF00")
    # create labels
    loginpage_label = tk.Label(root, text="Garage Shop",background="#EEC3E6",font=("Arial Bold", 20))
    username_label = tk.Label(root, text="Username:",background="#EEC3E6",font=("Arial", 12))
    password_label = tk.Label(root, text="Password:",background="#EEC3E6",font=("Arial", 12))
    message_label = tk.Label(root, text="",background="#EEC3E6")

    # create entries

    username_entry = tk.Entry(root, font=12)
    password_entry = tk.Entry(root, show="*", font=12)

    # create buttons
    login_button = tk.Button(root, text=" Login ", command=login,background="#887FF3")
    guest_button = tk.Button(root, text=" Guest ", command=guest,background="#887FF3")
    register_button = tk.Button(root, text="Register", command=register,background="#887FF3")

    # add widgets to grid,
    loginpage_label.place(x=780, y=100)
    username_label.place(x=660, y=250)
    username_entry.place(x=770, y=250)
    password_label.place(x=660, y=300)
    password_entry.place(x=770, y=300)
    login_button.place(x=860, y=350)
    guest_button.place(x=950, y=350)
    register_button.place(x=770, y=350)
    message_label.place(x=770, y=380)

root = tk.Tk()
root['background']='#EEC3E6'
user_login1()
# Start the tkinter event loop
root.mainloop()
