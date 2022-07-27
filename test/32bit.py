import tkinter as tk
from tkinter import ttk, CENTER, filedialog
from tkinter.messagebox import showinfo, showwarning
import sqlite3, sys ,os , psutil, pysftp



root = tk.Tk()

# config the root window
root.geometry("400x350")
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

# check tom old or new
def tom_type():
    info = psutil.virtual_memory().total
    if info < 10889192448:
        print("old")
        return "Tom-Old"
    else:
        print("new")
        return "Tom-New"
tom_type()

# serial number
my_string_var = tk.StringVar()
my_string_var.set(tom_type() + " : " + getMachine_addr().strip("SerialNumber"))

# serial number label
serial_device = tk.Label(root, textvariable=my_string_var, font=('Helvetica 12 bold'))
serial_device.pack(fill=tk.X, padx=6, pady=6)

device_path = 'C:\ENR-TOM\config'


def get_path():
    # check folder path
    if os.path.exists(device_path):
        end_path = device_path
    else:
        folder = filedialog.askdirectory()
        end_path = folder
    return end_path


myvar =  tk.StringVar()
myvar.set("Path: " + get_path())
label_path = tk.Label(root, textvariable=myvar, font=('Helvetica 10 bold'))
label_path.pack(fill=tk.X, padx=4, pady=4)


# Station label
station_label = ttk.Label(text="Select Station: ", font=('Helvetica 14 bold'))
station_label.pack(fill=tk.X, padx=5, pady=5)

my_list = []
# connect to database
conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()
# return all station arabic name
cur.execute("SELECT Arabic_Name FROM Stations ")
rows = cur.fetchall()
for row in rows:
    my_list.append(row)

# create a station combobox
selected_station = tk.StringVar()
station_combo = ttk.Combobox(root, textvariable=selected_station)
# values for station
station_combo['values'] = [item for result in my_list for item in result if item]
# change state to readonly

# change place for station combobox
station_combo.pack(fill=tk.X, padx=5, pady=5)

# office label
office_label = ttk.Label(text="Select Office: ", font=('Helvetica 14 bold'))
# change place
office_label.pack(fill=tk.X, padx=5, pady=5)
# create office combobox
selected_office = tk.StringVar()
office_combo = ttk.Combobox(root, textvariable=selected_office)
office_combo.pack(fill=tk.X, padx=6, pady=6)


# create window label
window_labal = ttk.Label(text="Select Window: ", font=('Helvetica 14 bold'))
window_labal.pack(fill=tk.X,  padx=5, pady=5)

selected_window = tk.StringVar()
window_combo = ttk.Combobox(root, textvariable=selected_window)
window_combo.pack(fill=tk.X, padx=6, pady=6)


# bind the selected value changes
def station_changed(event):
    # clear office data
    office_combo.set('')
    # station value
    x = selected_station.get()
    office_list = []
    query = conn.cursor()
    query.execute("SELECT nameEn FROM Offices as off, Stations as sta WHERE off.station_id=sta.English_Name and sta.Arabic_name=? ", (x,))

    rows = query.fetchall()

    if len(rows) > 0:
        for row in rows:
            office_list.append(row)

            office_combo['values'] = [o_item for o_result in office_list for o_item in o_result if o_item]
    else:
        office_combo['values'] = office_list

station_combo.bind('<<ComboboxSelected>>', station_changed)


# bind the selected value changes
def office_changed(event):
    window_combo.set('')
    x= selected_office.get()

    window_list = []
    query = conn.cursor()
    query.execute("SELECT name FROM Windows")
    rows = query.fetchall()
    print(rows)

    if len(rows) > 0:
        for row in rows:
            window_list.append(row)
            window_combo['values'] = [w_item for w_result in window_list for w_item in w_result if w_item]
    else:
        window_combo['values'] = window_list

office_combo.bind('<<ComboboxSelected>>', office_changed)


def create_file():
    x = selected_station.get()
    y = selected_office.get()
    if len(selected_station.get()) and len(selected_office.get()) != 0 and len(selected_window.get()) != 0:
        query3 = conn.cursor()
        query3.execute("SELECT * FROM Offices WHERE nameEn=?", (y,))
        f = query3.fetchall()
        for v in f:
            print(v[2])

        query = conn.cursor()
        query.execute("SELECT * FROM Stations WHERE Arabic_Name=?", (x,))
        m = query.fetchall()

        # loop throw selected station query
        for w in m:
            print(w[5], w[4], w[2], w[3])

        # ocity file date
        with open(os.path.join(get_path(), "ocity.yml"), "w", encoding="utf-8") as f:
            f.write("ocity:\n" + ' ' +"baseURL: https://obs.enr.gov.eg/" + w[5] + "/api/v2\n" +
                    ' ' + "oauth.authorizationURI: https://obs.enr.gov.eg/oauth/token\n" + ' '
                    + "oauth.tokenURI: https://obs.enr.gov.eg/oauth/token")

        # platform file data
        with open(os.path.join(get_path(), "platform.yml"), "w", encoding="utf-8") as x:
            x.write(
                "platform:\n" + ' ' + "ticketPrinterURL: custom\n" + ' ' + "ticketPrinterHost: COM2\n" +
               ' ' + "printerName: default\n" +  ' ' + "syncClock: false\n" +
                ' ' +"qrReaderPort: COM6")

        # terminal file data
        with open(os.path.join(get_path(), "terminal.yml"), "w", encoding="utf-8") as t:
            t.write("terminal:\n" + ' ' + "softwareVersion: 1.0.0\n" + ' ' + "merchant: " + w[5] + "\n" +
                   ' ' + "merchantId: 453215056520282074\n" + ' ' + "terminalId: " + getMachine_addr().strip(
                "SerialNumber") + "\n" +
                   ' ' + "terminalCode: 001\n" +  ' ' + "station: " + str(w[4]) + "\n" + ' ' + "stationName: " + w[
                        2] + "\n" + ' ' + "office: 456\n"
                    + ' ' + "officeName: " + selected_office.get() + "\n" + ' ' + "defaultPersonId: 580686677551349744\n" + ' ' + "returnTripAllowed: false\n" +
                   ' ' + "openReturnEnabled: false\n" + ' ' + "inactivityTimeout: 600000\n" + ' ' + "mandatoryNationalId: false\n"
                                                                                      ' ' + "ticketsPerPurchaseLimit: 4\n")

        # serial file
        with open(os.path.join(get_path(), "Serial" + getMachine_addr().strip("SerialNumber") + ".txt"), "w", encoding="utf-8") as j:
            j.write("Merchant: " + w[5] + '\n' +"station Name: " + str(w[2]) + '\n' + "Station Code: " + str(w[4]) + '\n' + "Device Number: " + getMachine_addr().strip("SerialNumber") + '\n'
                    + "Office En: " + str(v[2]) + '\n' + "Office Ar: " + selected_office.get() + '\n' + "Window: " + selected_window.get() + '\n' + "Type: " + tom_type())


        # send serial file to server
        def connect_to_server():
            host = '10.245.15.21'
            port = 22
            username = 'ecards'
            password = 'Ecards2022!'
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            try:
                conn = pysftp.Connection(host=host, port=port, username=username, password=password, cnopts=cnopts)
                print("connection established successfully")
                with conn.cd('/home/ecards/oldtoms'):  # chdir to public
                    conn.put('C:\ENR-TOM\config' + '\Serial' + getMachine_addr().strip("SerialNumber") + '.txt')
                    conn.close()


            except:
                print('failed to establish connection to targeted server')
        connect_to_server()


        showinfo('نجاح', 'تم التسجيل والانشاء بنجاح')




        # set value for combo none
        station_combo.set('')
        office_combo.set('')
        window_combo.set('')
    else:
         # info message
         showwarning('info', 'برجاء اكمال جميع الحقول')


# create button
download_icon = tk.PhotoImage(file='download.png')
create = ttk.Button(
    root,
    text="Create",
    image=download_icon,
    compound=tk.LEFT,
    command=create_file
    ).place(relx=.5, rely=.9, anchor=CENTER)

root.mainloop()