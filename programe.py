import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning
from calendar import month_name
from tkinter import CENTER
import sqlite3,sys, os
import requests
import json

root = tk.Tk()

# config the root window
root.geometry("600x300")
root.title('E-cards Config Tool')

# Get device serial number
def getMachine_addr():
    os_type = sys.platform.lower()
    if "win" in os_type:
        command = "wmic bios get serialnumber"
    elif "linux" in os_type:
        command = "hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid"
    elif "darwin" in os_type:
        command = "ioreg -l | grep IOPlatformSerialNumber"
    return os.popen(command).read().replace("\n", "").replace("	", "").replace(" ", "")

# serial number
my_string_var = tk.StringVar()
my_string_var.set("Device Serial Number : " + getMachine_addr().strip("SerialNumber"))

# serial number label
serial_device = tk.Label(root, textvariable=my_string_var, font=('Helvetica 12 bold'))
serial_device.pack(fill=tk.X, padx=6, pady=6)

# Station label
station_label = ttk.Label(text="Select Station: ", font=('Helvetica 14 bold'))
station_label.pack(fill=tk.X, padx=5, pady=5)

my_list = []
# connect to database
conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()
# return all station arabic name
cur.execute("SELECT Id FROM Enr_stations ")
rows = cur.fetchall()
for row in rows:
    my_list.append(row)

# create a combobox
selected_station = tk.StringVar()
station_combo = ttk.Combobox(root, textvariable=selected_station)
# values for station
station_combo['values'] = my_list
# change state to readonly
station_combo['state'] = 'readonly'
# change place for station combobox
station_combo.pack(fill=tk.X, padx=5, pady=5)

# office label
office_label = ttk.Label(text="Select Office: ", font=('Helvetica 14 bold'))
# change place
office_label.pack(fill=tk.X, padx=5, pady=5)

selected_office = tk.StringVar()
office_combo = ttk.Combobox(root, textvariable=selected_office)
office_combo.pack(fill=tk.X, padx=6, pady=6)


# bind the selected value changes
def station_changed(event):
    office_combo.set('')
    x = selected_station.get()
    office_list = []
    query = conn.cursor()
    query.execute("SELECT name FROM offices WHERE station_id=?", (x,))
    rows = query.fetchall()

    if len(rows) > 0:
        for row in rows:
            office_list.append(row)
            office_combo['values'] = office_list
    else:
        office_combo['values'] = office_list

station_combo.bind('<<ComboboxSelected>>', station_changed)

def office_value(event):
    office_value_var = selected_office.get()
    return office_value_var

office_combo.bind('<<ComboboxSelected>>', office_value)

download_icon = tk.PhotoImage(file='download.png')

def create_file():
    x = selected_station.get()

    if len(selected_station.get()) and len(selected_office.get()) != 0 :
        query = conn.cursor()
        query.execute("SELECT * FROM Enr_stations WHERE Id=?", (x,))
        m = query.fetchall()

        # loop throw selected station query
        for w in m:
            print(w[5], w[4], w[2], w[3])

        # ocity file date
        with open(os.path.join(sys.path[0], "ocity.yml"), "w") as f:
            f.write("ocity:\n" + "\tbaseURL: https://obs.enr.gov.eg/" + w[5] + "/api/v2\n" +
                    "\toauth.authorizationURI: https://obs.enr.gov.eg/oauth/token\n"
                    + "\toauth.tokenURI: https://obs.enr.gov.eg/oauth/token")

        # platform file data
        with open(os.path.join(sys.path[0], "platform.yml"), "w") as x:
            x.write(
                "platform:\n" + "\tticketPrinterURL: custom\n" + "\tticketPrinterHost: COM2\n" +
                "\tprinterName: default\n" + "\tsyncClock: false\n" +
                "\tqrReaderPort: COM6")


        # terminal file data
        with open(os.path.join(sys.path[0], "terminal.yml"), "w") as t:
            t.write("terminal:\n" + "\tsoftwareVersion: 1.0.0\n" + "\tmerchant: " + w[5] + "\n" +
                    "\tmerchantId: 453215056520282074\n" + "\tterminalId: " + getMachine_addr().strip("SerialNumber") + "\n" +
                    "\tterminalCode: 001\n" + "\tstation: " + str(w[4]) + "\n" + "\tstationName: " + w[2] + "\n" + "\toffice: 456\n"
                    + "\tofficeName: " + selected_office.get() + "\n" + "\tdefaultPersonId: 580686677551349744\n" + "\treturnTripAllowed: false\n" +
                    "\topenReturnEnabled: false\n" + "\tinactivityTimeout: 600000\n" + "\tmandatoryNationalId: false\n"
                     "\tticketsPerPurchaseLimit: 4\n")

        print(type(getMachine_addr()))
        # success message


        def signDate():
            end_point = "http://127.0.0.1:8000/api/create/"
            data = {
            'merchant' : w[5],
            'terminalId': getMachine_addr().strip("SerialNumber") ,
            'station': str(w[4]),
            'stationName': w[2],
            'officeName':  selected_office.get()
            }

            headers = {
                "Content-Type": "application/json",
            }

            response = requests.post(end_point, json=data, headers=headers)
            if response:
                showinfo('Done', 'Files Created Successfully')
                office_combo.set('')
                station_combo.set('')
        signDate()

    else:

         # info message
         showwarning('info', 'Please Select Station And Office ! ')

create = ttk.Button(
    root,
    text="Create",
    image=download_icon,
    compound=tk.LEFT,
    command=create_file
    ).place(relx=.5, rely=.7, anchor=CENTER)

root.mainloop()