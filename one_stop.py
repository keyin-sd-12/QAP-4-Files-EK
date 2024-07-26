"""  
QAP-4, EK, SD-12 Group17
"""

import os, sys, signal, atexit, time, datetime, math, random, shutil
import functions as Fn

# print IOError message and exit
def file_error_print(e, width=60, terminal_width=80):
    work_msg = f"Processing file: '{e.filename}'"
    raise_runtime_error(77, 0, e.filename, "", True, 13, work_msg, width, terminal_width, e)
    #print(f"\nOS Error {e.errno}: {e.strerror} - '{e.filename}'")
    #exit(e.errno)

# print runtime error message and exit    
def raise_runtime_error(error_code, file_line=0, file_name="", wrong_field="", display_progress=False, progress_end=10, progress_message="", width=60, terminal_width=80, e=None):
    if display_progress:
        progress_rotating(progress_end, progress_message, "ERROR!", width, terminal_width, 0.07, 1, 2)
    print(f"{terminal_width*' '}\r--> Runtime Error {error_code}:\n", end="")
    if error_code == 1:
        print(f"    Numerical value is missing!\n    (file '{file_name}', line {file_line})")
    elif error_code == 2:
        print(f"    Incorrect data field '{wrong_field}'!\n    (file '{file_name}', line {file_line})")
    elif error_code == 3:
        print(f"    Required separator '{wrong_field}' is missing!\n    (file '{file_name}', line {file_line})")
    elif error_code == 4:
        print(f"    Value '{wrong_field}' is of wrong numeric type/format!\n    (file '{file_name}', line {file_line})")
    elif error_code == 5:
        print(f"    Duplicate setting field '{wrong_field}'!\n    (file '{file_name}', line {file_line})")
    elif error_code == 6:
        print(f"    Setting field '{wrong_field}' is missing!\n    (file '{file_name}').")
    elif error_code == 7:
        print(f"    File '{file_name}' doesn't contain any information!")
    elif error_code == 8:
        print(f"    Value is of wrong numeric type/format!")
    elif error_code == 77:
        print(f"    OS Error {e.errno}: {e.strerror} - '{e.filename}'")  
    else: print("    Unknown exception")    
    exit(error_code)

# open file and handle exceptions
def open_file(file_name, mode="r"):
    try:
        file = open(file_name, mode)
    except OSError as e:
        file_error_print(e, COLPRINTWIDTH, CLAIMPRINTWIDTH)
    return file

def write_file(file_object, write_str, flush_file=True):
    try:
        file_object.write(write_str)
    except OSError as e:
        file_error_print(e)
    try:
        if flush_file: file_object.flush()
    except OSError as e:
        file_error_print(e)
    return 0    

# making backup of the policies file
def backup_file(file_name):    
    if os.path.isfile(file_name):
        try:
            shutil.copy(file_name, os.path.splitext(file_name)[0] + ".bak")
        except IOError as e:
            file_error_print(e)

# find field_name element index in a list        
def find_field_index(field_name, field_list):
    count = -1
    for line in field_list:
        count += 1
        if line[1] == field_name: 
            return count
    return (-1)

# defer defining file cleanup function until program exits
# so that file_list[] is populated with file objects
# FUN FACT: a function can return another function
def create_file_cleanup(list_of_files):
    def file_cleanup():
        print("\n"+Fn.FormatString(CH2 * (COLPRINTWIDTH), CLAIMPRINTWIDTH, Fn.CENTER))
        print(Fn.FormatString("Exiting - closing files", CLAIMPRINTWIDTH, Fn.CENTER))
        processed_names = []
        for f in reversed(list_of_files):
            file_message = f"File '{f.name}' "
            if not f.closed:
                f.close()
                file_message += "closed successfully"
            else:
                file_message += "was already closed"
                
            if f.name not in processed_names:
                print(Fn.FormatString(file_message, CLAIMPRINTWIDTH, Fn.CENTER))        
                processed_names.append(f.name)    

        print(Fn.FormatString("Done closing files", CLAIMPRINTWIDTH, Fn.CENTER))
        print(Fn.FormatString(CH2 * (COLPRINTWIDTH-6), CLAIMPRINTWIDTH, Fn.CENTER))
        list_of_files.clear()        
    return file_cleanup

# handle Ctrl-C signal
def handle_ctrl_c(signum, frame):
    print("\n\n"+Fn.FormatString("===== Ctrl-C Detected, Exiting Gracefully =====", CLAIMPRINTWIDTH, Fn.CENTER))
    exit(100)

# extract tuple from a string using a separator                    
def extract_tuple_from_string(string, separator):
    split_line = string.split(separator)
    if len(split_line) > 1:
        return split_line[0].strip(), split_line[1].strip()
    else: return split_line[0].strip(), ""
    
# convert integer or float number to string with 2-decimal digit formatting for a float
def format_settings_value(num): return str(num) if isinstance(num, int) else "{:.2f}".format(num) if isinstance(num, float) else raise_runtime_error(8)

# rotating progress display    
def progress_rotating(end=100, message="", message_end="", width=60, terminal_width=80, interval=0.04, interval_sleep1=0.5, interval_sleep2=1):
    CHARS = ['|', '/', '-', '\\']
    for i in range(101):
        if i % 5 == 0:  # Only change the display value for multiples of 5
            display_value = f"{i:3d}%"
        progress_message = Fn.JustifyText(message, f"{CHARS[i % len(CHARS)]} {display_value}", width)
        progress_message = Fn.FormatString(progress_message, terminal_width, Fn.CENTER)
        print(f"\r{progress_message}\r", end="")
        time.sleep(interval) 
        if i == end:
            time.sleep(interval_sleep1)
            if len(message_end) != 0:
                error_message = Fn.FormatString(message_end, terminal_width, Fn.CENTER)
                print(f"{error_message}\r", flush=True, end="")
                time.sleep(interval_sleep2)
            break
       
# generate random date within the specified range        
def get_random_date(start_date_object, end_date_object):
    delta = end_date_object - start_date_object
    random_days = random.randint(1, delta.days-1)
    random_date_object = start_date_object + datetime.timedelta(days=random_days)
    return random_date_object
        
COMPANY_NAME = "One Stop Insurance, Inc."            
SETTINGS_FILENAME = "const.dat"
SETTINGS_FILENAME_SEPARATOR = ":"
CMM = ", "
POLICY_FILENAME = "policy.dat"
CLAIMS_FILENAME = "claims.dat"

# FUN! - class name can be in a list as element (int/float - for string to number conversion)
SETTINGS_FILENAME_FIELDS = [ 
                            [0,     "NEXTPOLICY",       "Next Policy Number",                   int],
                            [0.00,  "BASICPREMIUM",     "Basic Premium",                        float],
                            [0.00,  "ADDITIONALCAR",    "Discount for Additional Cars",         float],
                            [0.00,  "EXTRALIAB",        "Cost of Extra Liability Coverage",     float],
                            [0.00,  "GLASSCOVER",       "Cost of Glass Coverage",               float],
                            [0.00,  "CARLOANER",        "Cost for Loaner Car Coverage",         float],
                            [0.00,  "HSTRATE",          "HST Percentage Rate",                  float],
                            [0.00,  "MONTHLYFEE",       "Processing Fee for Monthly Payments",  float]
]

# validation lists
YESNO = ["Y", "N", "YES", "NO"]
PAYTYPE = ["F", "M", "D", "FULL", "MONTHLY", "DOWN PAY"]
PROVINCELIST = ["AB", "BC", "MB", "NB", "NL", "NS", "ON", "PE", "QC", "SK"]

# I want to use dictionaries the abbraviations and full names
PROVINCES = {
    "AB": "Alberta",
    "BC": "British Columbia",
    "MB": "Manitoba",
    "NB": "New Brunswick",
    "NL": "Newfoundland and Labrador",
    "NS": "Nova Scotia",
    "ON": "Ontario",
    "PE": "Prince Edward Island",
    "QC": "Quebec",
    "SK": "Saskatchewan"
}

PAYTYPES = {
    "F": ("In Full", False),
    "M": ("Monthly", True),
    "D": ("Down Pay", True)
}

YESNOS = {
    "Y": ("Yes", True),
    "N": ("No", False)
}

ALLOWEDCHAR = set("ABCDEFGHIJKLMONPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
ALLOWEDNUM = set("0123456789")
ALLOWEDNAMESYM = set(" .-'")
ALLOWEDSYM = set(" .,;:()[]<>@#&*/~`-_'")
ALLOWEDADDRESSSYM = set(" .;:()[]<>@#&*/~-_'")
ALLOWEDPOSTALCODESEPARATOR = set(" ")
ALLOWEDPHONESEPARATOR = set("-() .")
ALLOWEDDATESEP = set("-/ ")
LOCATIONLENGTH = 45

ALLOWEDNAME = ALLOWEDCHAR | ALLOWEDNAMESYM
ALLOWEDLOCATION = ALLOWEDCHAR | ALLOWEDNUM | ALLOWEDADDRESSSYM
ALLOWEDPOSTALCODE = ALLOWEDCHAR | ALLOWEDNUM | ALLOWEDPOSTALCODESEPARATOR
ALLOWEDDATE = ALLOWEDNUM | ALLOWEDCHAR | ALLOWEDDATESEP
ALLOWEDPHONE = ALLOWEDNUM | ALLOWEDPHONESEPARATOR

# terminal width for a invoice printout
INVCOL1 = 34
INVCOL2 = 27
CLAIMPRINTWIDTH = 66
COLPRINTWIDTH = CLAIMPRINTWIDTH - 20
RIGHTCOLWIDTH = 33
CLAIMHISTORYWIDTH = 33
CH1 = "="
CH2 = "-"  
MG = "  "

DEFAULTFIRSTNAME = "John K."
DEFAULTLASTNAME = "O'Malkovich-Simpson"
DEFAULTADDRESS = "55-1A Bad Route Road"
DEFAULTCITY = "Come By Chance"
DEFAULTPROVINCE = "NL"
DEFAULTPOSTALCODE = "A0B0A2"
DEFAULTPHONE = "709-555-8893"
DEFAULTCARS = 3
DEFAULTEXTRALIABILITY = "Y"
DEFAULTGLASSCOVERAGE = "Y"
DEFAULTCARLOANER = "Y"
DEFAULTPAY = "D"
NUMBEROFMONTHS = 8
EXTRALIABILITYAMOUNT = 1000000.00
INVOICEHEAD = "INVOICE"
INVOICEBEGIN = "BEGIN"
INVOICEEND = "END"

file_list = []
invoice_printout = []
policy_information = []
policy_past_claims = []   

# register file cleanup function to run at exit, so that all files are closed if program
atexit.register(create_file_cleanup(file_list))

# want to catch Ctrl-C exception, so the files are closed properly
# (ideally, would catch all exceptions, but that's a bit more involved)
signal.signal(signal.SIGINT, handle_ctrl_c)
# alternatively, Ctrl-C can be disabled:
#signal.signal(signal.SIGINT, signal.SIG_IGN)

print(); print(CH1 * CLAIMPRINTWIDTH)
print(Fn.FormatString(COMPANY_NAME, CLAIMPRINTWIDTH, Fn.CENTER))
print(CH2 * CLAIMPRINTWIDTH)

# open the settings file
settings_file = open_file(SETTINGS_FILENAME, "r")
file_list.append(settings_file)

message_status = f"Reading Settings File '{settings_file.name}'"

# read values from the settings file
# fields can be in any order, but must be present
# thorough error checking is done to ensure that the const.dat file is in the correct format
count = 0
empty_file = True
for line in settings_file:
    count += 1
    stripped_line = line.strip()
    #print(stripped_line, len(stripped_line))
    if len(stripped_line) > 0:
        empty_file = False
        if SETTINGS_FILENAME_SEPARATOR not in stripped_line:
            raise_runtime_error(3, count, SETTINGS_FILENAME, SETTINGS_FILENAME_SEPARATOR, True, 47, message_status, COLPRINTWIDTH, CLAIMPRINTWIDTH)
        else: setting_name, setting_value = extract_tuple_from_string(stripped_line, SETTINGS_FILENAME_SEPARATOR)
        #print(setting_name, setting_value)
        if setting_value == "":
            raise_runtime_error(1, count, SETTINGS_FILENAME, "", True, 56, message_status, COLPRINTWIDTH, CLAIMPRINTWIDTH)
        else:
            i = find_field_index(setting_name, SETTINGS_FILENAME_FIELDS)
            #print(i)
            if i == -1:
                raise_runtime_error(2, count, SETTINGS_FILENAME, setting_name, True, 68, message_status, COLPRINTWIDTH, CLAIMPRINTWIDTH)
            else:
                try:
                    SETTINGS_FILENAME_FIELDS[i][0] = SETTINGS_FILENAME_FIELDS[i][3](setting_value)
                except ValueError:
                    raise_runtime_error(4, count, SETTINGS_FILENAME, setting_value, True, 83, message_status, COLPRINTWIDTH, CLAIMPRINTWIDTH)    
                if len(SETTINGS_FILENAME_FIELDS[i]) < 5:
                    SETTINGS_FILENAME_FIELDS[i].append(True)
                else: raise_runtime_error(5, count, SETTINGS_FILENAME, setting_name, True, 91, message_status, COLPRINTWIDTH, CLAIMPRINTWIDTH)    

if empty_file:
    raise_runtime_error(7, 0, SETTINGS_FILENAME, "", True, 11, message_status, COLPRINTWIDTH, CLAIMPRINTWIDTH)

for i in range(len(SETTINGS_FILENAME_FIELDS)):
    if len(SETTINGS_FILENAME_FIELDS[i]) < 5:
        raise_runtime_error(6, 0, SETTINGS_FILENAME, SETTINGS_FILENAME_FIELDS[i][1], True, 89, message_status, COLPRINTWIDTH, CLAIMPRINTWIDTH)
        
# close the settings file        
settings_file.close()

# assigning the values to the variables
# probably would have been better to use a dictionary for this
NEXTPOLICY = SETTINGS_FILENAME_FIELDS[0][0]
BASICPREMIUM = SETTINGS_FILENAME_FIELDS[1][0]
ADDITIONALCAR = SETTINGS_FILENAME_FIELDS[2][0]
EXTRALIAB = SETTINGS_FILENAME_FIELDS[3][0]
GLASSCOVER = SETTINGS_FILENAME_FIELDS[4][0]
CARLOANER = SETTINGS_FILENAME_FIELDS[5][0]
HSTRATE = SETTINGS_FILENAME_FIELDS[6][0]
MONTHLYFEE = SETTINGS_FILENAME_FIELDS[7][0]

progress_rotating(100, message_status, "SUCCESS!", COLPRINTWIDTH, CLAIMPRINTWIDTH, 0.07, 1, 2)

print(Fn.FormatString("The following inital settings", CLAIMPRINTWIDTH, Fn.CENTER))
print(Fn.FormatString(f"were read from the file '{SETTINGS_FILENAME}'", CLAIMPRINTWIDTH, Fn.CENTER))
print(Fn.FormatString(CH2 * COLPRINTWIDTH, CLAIMPRINTWIDTH, Fn.CENTER))

for i in range(len(SETTINGS_FILENAME_FIELDS)):
    if (i == 0):
        formatted_number = Fn.FormatInteger(SETTINGS_FILENAME_FIELDS[i][0], 0, Fn.LEFT)
    elif (i == 2) or (i == 6):
        formatted_number = Fn.FormatFloat(Fn.PERCENT, SETTINGS_FILENAME_FIELDS[i][0], 0, 2, Fn.RIGHT, True)
    else:
        formatted_number = Fn.FormatFloat(Fn.DOLLAR, SETTINGS_FILENAME_FIELDS[i][0], 0, 2, Fn.RIGHT)
       
    print(Fn.JustifyText(f"{SETTINGS_FILENAME_FIELDS[i][2]} ({SETTINGS_FILENAME_FIELDS[i][1]}):", formatted_number, CLAIMPRINTWIDTH))

print(Fn.FormatString(CH2 * (COLPRINTWIDTH - 10), CLAIMPRINTWIDTH, Fn.CENTER))

policy_count = 1
while True:
    policy_id = NEXTPOLICY
  
    print(); print(); print(CH1 * CLAIMPRINTWIDTH)
    print(Fn.FormatString("Insurance Policy Information Processing", CLAIMPRINTWIDTH, Fn.CENTER))
    print(CH2 * CLAIMPRINTWIDTH)

    print()
    print(Fn.FormatString(CH1 * (COLPRINTWIDTH-10), CLAIMPRINTWIDTH, Fn.CENTER))
    print(Fn.FormatString("CURRENT POLICY #"+Fn.FormatInteger(policy_id,7,Fn.LEFT,True,0), CLAIMPRINTWIDTH, Fn.CENTER))
    print(Fn.FormatString(CH1 * (COLPRINTWIDTH-10), CLAIMPRINTWIDTH, Fn.CENTER))
    print()
    print(Fn.FormatString("Entering Customer Information", CLAIMPRINTWIDTH, Fn.CENTER))
    print(Fn.FormatString(CH2 * (COLPRINTWIDTH+6), CLAIMPRINTWIDTH, Fn.CENTER))
    print(Fn.FormatString("(Pressing ENTER will accept default values)", CLAIMPRINTWIDTH, Fn.CENTER))
    print()

    first_name = Fn.ValidStringInput("--> First Name (Enter=Default, -end/-END to exit): ", 0, 40, ALLOWEDNAME, True, False, True)
    if first_name == Fn.ENDSTR:
        exit(0)  # program end
    elif first_name == "":
        first_name = DEFAULTFIRSTNAME.title()
    else:
        first_name = first_name.title()
    print("*** Input Accepted:", first_name)

    last_name = Fn.ValidStringInput("--> Last Name (Enter=Default): ", 0, 40, ALLOWEDNAME, True, False, True).title()
    if last_name == "":
        last_name = DEFAULTLASTNAME.title()
    print("*** Input Accepted:", last_name)

    street_address = Fn.ValidStringInput("--> Street Address (Enter=Default): ", 0, 60, ALLOWEDLOCATION, True, False, True).title()
    if street_address == "":
        street_address = DEFAULTADDRESS.title()
    print("*** Input Accepted:", street_address)

    address_city = Fn.ValidStringInput("--> City (Enter=Default): ", 0, 30, ALLOWEDLOCATION, True, False, True).title()
    if address_city == "":
        address_city = DEFAULTCITY.title()
    print("*** Input Accepted:", address_city)

    address_province = Fn.ValidStringInput("--> Province (Enter=Default): ", 2, 2, PROVINCELIST, False, True, True, True)
    if address_province == "":
        address_province = DEFAULTPROVINCE.upper()
    print("*** Input Accepted:", address_province)

    address_postalcode = Fn.ValidPostalCode("--> Postal Code (Enter=Default): ", 6, 20, ALLOWEDPOSTALCODE)
    if address_postalcode == "":
        address_postalcode = DEFAULTPOSTALCODE.upper()
    if (len(address_postalcode) == 6): address_postalcode = address_postalcode[:3] + " " + address_postalcode[3:]
    print("*** Input Accepted:", address_postalcode)

    phone_number = Fn.ValidPhoneNumber("--> Phone Number (Enter=Default): ", 10, 30, ALLOWEDPHONE, ALLOWEDPHONESEPARATOR)
    if phone_number == "":
        phone_number = DEFAULTPHONE
    if (len(phone_number) == 10): phone_number = phone_number[:3] + "-" +phone_number[3:6] + "-" + phone_number[6:]
    print("*** Input Accepted:", phone_number)

    print()
    print(Fn.FormatString("Entering Policy Options", CLAIMPRINTWIDTH, Fn.CENTER))
    print(Fn.FormatString(CH2 * (COLPRINTWIDTH+6), CLAIMPRINTWIDTH, Fn.CENTER))
    print()

    number_of_cars = Fn.ValidIntegerInput("--> Number of Cars Being Insured (Default=3): ", 1, 20, True, DEFAULTCARS)
    print("*** Input Accepted:", number_of_cars)

    extra_liability_str = Fn.ValidStringInput("--> Extra Liability Coverage up to $1M (yes/no, y/n, Default=Yes): ", 1, 3, YESNO, False, True, True, True).upper()[:1]
    if extra_liability_str == "":
        extra_liability_str = DEFAULTEXTRALIABILITY.upper()
    print("*** Input Accepted:", YESNOS[extra_liability_str][0])

    glass_coverage_str = Fn.ValidStringInput("--> Optional Glass Coverage (yes/no, y/n, Default=Yes): ", 1, 3, YESNO, False, True, True, True).upper()[:1]
    if glass_coverage_str == "":
        glass_coverage_str = DEFAULTGLASSCOVERAGE.upper()
    print("*** Input Accepted:", YESNOS[glass_coverage_str][0])

    loaner_car_str = Fn.ValidStringInput("--> Loaner Car Option (yes/no, y/n, Default=Yes): ", 1, 3, YESNO, False, True, True, True).upper()[:1]
    if loaner_car_str == "":
        loaner_car_str = DEFAULTCARLOANER.upper()
    print("*** Input Accepted:", YESNOS[loaner_car_str][0])

    payments_str = Fn.ValidStringInput("--> Payment Type (F/Full/M/Monthly/D/Down Pay, Default=D): ", 1, 8, PAYTYPE, True, True, True, True).upper()[:1]
    if payments_str == "":
        payments_str = DEFAULTPAY.upper()
    print("*** Input Accepted:", PAYTYPES[payments_str][0])

    if payments_str == PAYTYPE[2]:
        down_payment = Fn.ValidFloatInput("--> Down Payment Amount (Default=Random): ", 10, BASICPREMIUM*0.9, True, float(math.floor(random.uniform(BASICPREMIUM*0.1, BASICPREMIUM*0.8))))
        print("*** Input Accepted:", Fn.FormatFloat(Fn.DOLLAR, down_payment, 0, 2, Fn.RIGHT))
    else:
        down_payment = 0.00
    
    print()
    print(Fn.FormatString("Entering Previous Claim Information", CLAIMPRINTWIDTH, Fn.CENTER))
    print(Fn.FormatString(CH2 * (COLPRINTWIDTH+6), CLAIMPRINTWIDTH, Fn.CENTER))

    # entering past claim history
    claim_count = 0
    while True:
        print()
        print("Entering Past Claim History Record", claim_count+1)
        claim_number = Fn.ValidIntegerInput("--> Claim Number (Enter=Random, -1 to stop): ", 1, 99999, True, math.floor(random.uniform(1.0, 99999.9)), True)
        if claim_number == Fn.NEGONE:
            break
        print("*** Input Accepted: "+Fn.FormatInteger(claim_number, 5, Fn.RIGHT, True, 0))
        
        current_date = datetime.datetime.now()    
        date_10_years_ago = current_date - datetime.timedelta(days=3652)
        random_date = get_random_date(date_10_years_ago, current_date)
        claim_date = Fn.ValidDateInput("--> Claim Date (yyyy-/mm-/dd, yyyy-/mmm-/dd, Enter=Random): ", ALLOWEDDATE, True, random_date)
        print("*** Input Accepted:", claim_date.strftime("%B %d, %Y"))
        
        claim_amount = Fn.ValidFloatInput("--> Claim Amount (Default=Random): ", 10, 10000, True, float(math.floor(random.uniform(10.0, 3000.0))))
        print("*** Input Accepted:", Fn.FormatFloat(Fn.DOLLAR, claim_amount, 0, 2, Fn.RIGHT))
        
        claim_count += 1
        policy_past_claims.append([policy_id, claim_count, claim_number, claim_date, claim_amount])

    print()
    if claim_count == 0:
        past_claim_str = "No Past Claim History"
        print(Fn.FormatString(past_claim_str, CLAIMPRINTWIDTH, Fn.CENTER))
    else: 
        past_claim_str = "Past History: "+Fn.FormatInteger(claim_count, 0, Fn.LEFT)+" Claim"
        if claim_count > 1: past_claim_str += "s"
        print(Fn.FormatString("Total of "+Fn.FormatInteger(claim_count,0,Fn.LEFT)+" Claims Was Entered", CLAIMPRINTWIDTH, Fn.CENTER))
    print(Fn.FormatString(CH2 * (COLPRINTWIDTH-6), CLAIMPRINTWIDTH, Fn.CENTER))
      
    # main calculations
    insurance_cost = number_of_cars * BASICPREMIUM
    car_discount = BASICPREMIUM * ADDITIONALCAR / 100.00
    multiple_car_discount = (number_of_cars - 1) * car_discount
    
    total_insurance_cost = insurance_cost - multiple_car_discount
    
    extra_liability_option = EXTRALIAB * number_of_cars * int(YESNOS[extra_liability_str][1])
    glass_coverage_option = GLASSCOVER * number_of_cars * int(YESNOS[glass_coverage_str][1])
    loaner_car_option = CARLOANER * number_of_cars * int(YESNOS[loaner_car_str][1])
    
    total_extra_costs = extra_liability_option + glass_coverage_option + loaner_car_option
    
    total_insurance_premium = total_insurance_cost + total_extra_costs
    
    hst_total = total_insurance_premium * HSTRATE / 100.00
    total_cost = total_insurance_premium + hst_total
    
    # total due
    invoice_balance_due = total_cost - down_payment + MONTHLYFEE * (int(PAYTYPES[payments_str][1]))
    
    # calculate monthly payments (if any)
    monthly_payment = invoice_balance_due * (int(PAYTYPES[payments_str][1])) / NUMBEROFMONTHS

    # get due date
    current_date = datetime.datetime.now()
    due_date = Fn.AddMonths(current_date, 1).replace(day=1)
    
    # filling out the policy information list
    policy_information.append([policy_id, current_date, first_name, last_name, street_address, address_city, address_province, address_postalcode, phone_number, number_of_cars, extra_liability_str, glass_coverage_str, loaner_car_str, payments_str, down_payment, total_insurance_premium, policy_past_claims])
    number_of_data_entries_in_policy = len(policy_information[-1])-1
    
    additional_cars = YESNO[0] if number_of_cars > 1 else YESNO[1]
    
    # filling out the invoice printout
    invoice_printout.append(Fn.FormatString(2*CH1 + INVOICEBEGIN + CH1 * (CLAIMPRINTWIDTH - 4 - len(INVOICEHEAD+INVOICEBEGIN)) + INVOICEHEAD + 2*CH1, CLAIMPRINTWIDTH, Fn.CENTER))
    invoice_printout.append("")
    invoice_printout.append(Fn.FormatString(CH2 * (len(COMPANY_NAME)+20), CLAIMPRINTWIDTH, Fn.CENTER))
    invoice_printout.append(Fn.FormatString(COMPANY_NAME, CLAIMPRINTWIDTH, Fn.CENTER))
    invoice_printout.append(Fn.FormatString(CH2 * (len(COMPANY_NAME)+20), CLAIMPRINTWIDTH, Fn.CENTER))
    invoice_printout.append("")
    invoice_printout.append(Fn.FormatString("I n v o i c e".upper(), CLAIMPRINTWIDTH, Fn.CENTER))
    invoice_printout.append("")
    invoice_printout.append("")
    
    invoice_printout.append(Fn.JustifyText(Fn.FormatString(MG+"Date: "+current_date.strftime("%B %d, %Y"), INVCOL1, Fn.LEFT), Fn.JustifyText("Policy No.", Fn.FormatInteger(policy_id, 7, Fn.RIGHT, True, 0), INVCOL2)+MG, CLAIMPRINTWIDTH))
    invoice_printout.append(Fn.JustifyText(Fn.FormatString(MG+CH2*(INVCOL1-len(MG)), INVCOL1, Fn.LEFT), CH2*INVCOL2+MG, CLAIMPRINTWIDTH))    

    invoice_printout.append("")
    if payments_str == PAYTYPE[2]:
        invoice_str = Fn.JustifyText("Payment:", PAYTYPES[payments_str][0]+" & "+PAYTYPES[PAYTYPE[1]][0], INVCOL2)
    else: invoice_str = Fn.JustifyText("Payment Type:", PAYTYPES[payments_str][0], INVCOL2)
    invoice_printout.append(Fn.JustifyText(MG + "Billed To:", invoice_str+MG, CLAIMPRINTWIDTH))
        
    invoice_printout.append(Fn.JustifyText(Fn.FormatString(MG+CH2*(INVCOL1-len(MG)), INVCOL1, Fn.LEFT), CH2*INVCOL2+MG, CLAIMPRINTWIDTH))
    invoice_printout.append(Fn.JustifyText(Fn.FormatString(MG+first_name+" "+last_name, INVCOL1, Fn.LEFT), Fn.JustifyText("Addt'l Cars:", YESNOS[additional_cars][0], INVCOL2)+MG, CLAIMPRINTWIDTH))
    invoice_printout.append(Fn.JustifyText(Fn.FormatString(MG+street_address, INVCOL1, Fn.LEFT), Fn.JustifyText("Extra Liability:", YESNOS[extra_liability_str][0], INVCOL2)+MG, CLAIMPRINTWIDTH))
    invoice_printout.append(Fn.JustifyText(Fn.FormatString(MG+address_city+", "+address_province+" "+address_postalcode, INVCOL1, Fn.LEFT), Fn.JustifyText("Glass Coverage:", YESNOS[glass_coverage_str][0], INVCOL2)+MG, CLAIMPRINTWIDTH))
    invoice_printout.append(Fn.JustifyText(Fn.FormatString(MG+"Tel. "+phone_number, INVCOL1, Fn.LEFT), Fn.JustifyText("Loaner Car:", YESNOS[glass_coverage_str][0], INVCOL2)+MG, CLAIMPRINTWIDTH))
    invoice_printout.append(Fn.JustifyText(Fn.FormatString(MG+CH2*(INVCOL1-len(MG)), INVCOL1, Fn.LEFT), CH2*INVCOL2+MG, CLAIMPRINTWIDTH))
    
    invoice_printout.append("")
    invoice_printout.append(Fn.JustifyText(MG + "Description", "Rate      Qty        Cost" + MG, CLAIMPRINTWIDTH))
    invoice_printout.append(Fn.FormatString(CH2 * (CLAIMPRINTWIDTH-2*len(MG)), CLAIMPRINTWIDTH, Fn.CENTER))
    invoice_printout.append("")
    invoice_printout.append(Fn.JustifyText(MG + "Basic Premium", Fn.FormatFloat(Fn.DOLLAR, BASICPREMIUM, 7, 2, Fn.RIGHT) + "   " + Fn.FormatInteger(number_of_cars, 3, Fn.RIGHT) + "   " + Fn.FormatFloat(Fn.DOLLAR, insurance_cost, 10, 2, Fn.RIGHT) + MG, CLAIMPRINTWIDTH))

    if number_of_cars > 1:
        invoice_printout.append(Fn.JustifyText(MG + "- Discount (" + Fn.FormatFloat(Fn.PERCENT, ADDITIONALCAR, 0, 0, Fn.RIGHT, True) + " Off Addt'l Cars)", Fn.FormatFloat(Fn.DOLLAR, (-1) * car_discount, 7, 2, Fn.RIGHT) + "   " + Fn.FormatInteger(number_of_cars - 1, 3, Fn.RIGHT) + "   " + Fn.FormatFloat(Fn.DOLLAR, (-1) * multiple_car_discount, 10, 2, Fn.RIGHT) + MG, CLAIMPRINTWIDTH))
        invoice_printout.append(Fn.FormatString(CH2 * RIGHTCOLWIDTH + MG, CLAIMPRINTWIDTH, Fn.RIGHT))
        invoice_printout.append(Fn.FormatString(Fn.JustifyText("Insurance Subtotal:",Fn.FormatFloat(Fn.DOLLAR, total_insurance_cost, 10, 2, Fn.RIGHT), RIGHTCOLWIDTH)+MG, CLAIMPRINTWIDTH, Fn.RIGHT))
    
    invoice_printout.append("")

    optional_services_boolen = YESNOS[extra_liability_str][1] or YESNOS[glass_coverage_str][1] or YESNOS[loaner_car_str][1]
    optional_service_count = int(YESNOS[extra_liability_str][1]) + int(YESNOS[glass_coverage_str][1]) + int(YESNOS[loaner_car_str][1])
    if optional_services_boolen:
        opt_serv_str = "Optional Services:" if optional_service_count > 1 else "Optional Service:"
        invoice_printout.append(Fn.FormatString(MG + opt_serv_str, CLAIMPRINTWIDTH, Fn.LEFT))
        if YESNOS[extra_liability_str][1]:
            invoice_printout.append(Fn.JustifyText(MG + "* Extra Liability (up to $1M)", Fn.FormatFloat(Fn.DOLLAR, EXTRALIAB, 7, 2, Fn.RIGHT) + "   " + Fn.FormatInteger(number_of_cars, 3, Fn.RIGHT) + "   " + Fn.FormatFloat(Fn.DOLLAR, extra_liability_option, 10, 2, Fn.RIGHT) + MG, CLAIMPRINTWIDTH))
        if YESNOS[glass_coverage_str][1]:
            invoice_printout.append(Fn.JustifyText(MG + "* Glass Coverage", Fn.FormatFloat(Fn.DOLLAR, GLASSCOVER, 7, 2, Fn.RIGHT) + "   " + Fn.FormatInteger(number_of_cars, 3, Fn.RIGHT) + "   " + Fn.FormatFloat(Fn.DOLLAR, glass_coverage_option, 10, 2, Fn.RIGHT) + MG, CLAIMPRINTWIDTH))
        if YESNOS[loaner_car_str][1]:
            invoice_printout.append(Fn.JustifyText(MG + "* Loaner Car Option", Fn.FormatFloat(Fn.DOLLAR, CARLOANER, 7, 2, Fn.RIGHT) + "   " + Fn.FormatInteger(number_of_cars, 3, Fn.RIGHT) + "   " + Fn.FormatFloat(Fn.DOLLAR, loaner_car_option, 10, 2, Fn.RIGHT) + MG, CLAIMPRINTWIDTH))
        if optional_service_count > 1:
            invoice_printout.append(Fn.FormatString(CH2 * RIGHTCOLWIDTH + MG, CLAIMPRINTWIDTH, Fn.RIGHT))
            invoice_printout.append(Fn.FormatString(Fn.JustifyText("Extra Costs Subtotal:", Fn.FormatFloat(Fn.DOLLAR, total_extra_costs, 10, 2, Fn.RIGHT), RIGHTCOLWIDTH)+MG, CLAIMPRINTWIDTH, Fn.RIGHT))
        invoice_printout.append("")

    invoice_printout.append(Fn.FormatString(CH2 * (CLAIMPRINTWIDTH - 2*len(MG)), CLAIMPRINTWIDTH, Fn.CENTER))
    invoice_printout.append(Fn.JustifyText(MG+"Total Insurance Premium:", Fn.FormatFloat(Fn.DOLLAR, total_insurance_premium, 10, 2, Fn.RIGHT)+MG, CLAIMPRINTWIDTH))
    invoice_printout.append(Fn.JustifyText(MG+"HST ("+Fn.FormatFloat(Fn.PERCENT, HSTRATE, 0, 0, Fn.RIGHT, True) + "):", Fn.FormatFloat(Fn.DOLLAR, hst_total, 10, 2, Fn.RIGHT)+MG, CLAIMPRINTWIDTH))
    invoice_printout.append("")
    invoice_printout.append(Fn.FormatString(CH2 * (CLAIMPRINTWIDTH - 2*len(MG)), CLAIMPRINTWIDTH, Fn.CENTER))
    
    if PAYTYPES[payments_str][1]: invoice_str = "Invoice Total:"
    else: invoice_str = "Total Invoice Cost:".upper()
    
    invoice_printout.append(Fn.JustifyText(MG+invoice_str, Fn.FormatFloat(Fn.DOLLAR, total_cost, 10, 2, Fn.RIGHT)+MG, CLAIMPRINTWIDTH))
    
    if PAYTYPES[payments_str][1]:
        invoice_printout.append(Fn.JustifyText(MG+"Processing Fee:", Fn.FormatFloat(Fn.DOLLAR, MONTHLYFEE, 10, 2, Fn.RIGHT)+MG, CLAIMPRINTWIDTH))
        if down_payment > 0.00:
            invoice_printout.append(Fn.JustifyText(MG+"- Down Payment:", Fn.FormatFloat(Fn.DOLLAR, (-1)*down_payment, 10, 2, Fn.RIGHT) + MG, CLAIMPRINTWIDTH))

        invoice_printout.append(Fn.FormatString(CH2 * (CLAIMPRINTWIDTH - 2*len(MG)), CLAIMPRINTWIDTH, Fn.CENTER))        
        invoice_printout.append(Fn.JustifyText(MG+"Total Invoice Cost:".upper(), Fn.FormatFloat(Fn.DOLLAR, invoice_balance_due, 10, 2, Fn.RIGHT)+MG, CLAIMPRINTWIDTH))        
        invoice_printout.append("")
        # invoice_printout.append(Fn.FormatString(CH2 * RIGHTCOLWIDTH + MG, CLAIMPRINTWIDTH, Fn.RIGHT))
        invoice_printout.append(Fn.JustifyText(MG + CH2 * len(past_claim_str), CH2 * RIGHTCOLWIDTH + MG, CLAIMPRINTWIDTH))
        # invoice_printout.append(Fn.FormatString(Fn.JustifyText("Monthly Payment ("+str(NUMBEROFMONTHS)+" mo):", Fn.FormatFloat(Fn.DOLLAR, monthly_payment, 10, 2, Fn.RIGHT), RIGHTCOLWIDTH) + MG, CLAIMPRINTWIDTH, Fn.RIGHT))
        invoice_printout.append(Fn.JustifyText(MG+past_claim_str, Fn.JustifyText("Monthly Payment ("+str(NUMBEROFMONTHS)+" mo):", Fn.FormatFloat(Fn.DOLLAR, monthly_payment, 10, 2, Fn.RIGHT), RIGHTCOLWIDTH) + MG, CLAIMPRINTWIDTH))
        invoice_str = "* First Due:"
        invoice_printout.append(Fn.FormatString(Fn.JustifyText(invoice_str, due_date.strftime("%B %d, %Y"), RIGHTCOLWIDTH) + MG, CLAIMPRINTWIDTH, Fn.RIGHT))
    else: 
        invoice_printout.append("")
        # invoice_printout.append(Fn.FormatString(CH2 * RIGHTCOLWIDTH + MG, CLAIMPRINTWIDTH, Fn.RIGHT))
        invoice_printout.append(Fn.JustifyText(MG + CH2 * len(past_claim_str), CH2 * RIGHTCOLWIDTH + MG, CLAIMPRINTWIDTH))        
        invoice_str = "* Due in Full:"
        invoice_printout.append(Fn.JustifyText(MG+past_claim_str, Fn.JustifyText(invoice_str, due_date.strftime("%B %d, %Y"), RIGHTCOLWIDTH) + MG, CLAIMPRINTWIDTH))
    
    #invoice_printout.append(Fn.FormatString(Fn.JustifyText(invoice_str, due_date.strftime("%B %d, %Y"), RIGHTCOLWIDTH) + MG, CLAIMPRINTWIDTH, Fn.RIGHT))
    
    invoice_printout.append("")
    
    #writing the past claim history (if any)
    if claim_count > 0:
        invoice_printout.append(MG+"Claim #  Claim Date        Amount")
        invoice_printout.append(MG+CH2*CLAIMHISTORYWIDTH)
        for past_claim in policy_past_claims:
            invoice_printout.append(MG+Fn.FormatInteger(past_claim[2], 5, Fn.RIGHT, True, 0)+ "    "+past_claim[3].strftime("%Y-%m-%d")+"    "+Fn.FormatFloat(Fn.DOLLAR, past_claim[4], 10, 2, Fn.RIGHT))
   
    invoice_printout.append("")
    invoice_printout.append(Fn.FormatString(2*CH1 + INVOICEEND + CH1 * (CLAIMPRINTWIDTH - 4 - len(INVOICEHEAD+INVOICEEND)) + INVOICEHEAD + 2*CH1, CLAIMPRINTWIDTH, Fn.CENTER))
    
    # printing invoice to screen
    for invoice_printout_line in invoice_printout:
        print(invoice_printout_line)

    # file operations start, disable Ctrl-C
    signal.signal(signal.SIGINT, signal.SIG_IGN)
        
    # creating invoice printout file
    invoice_filename = "I"+Fn.FormatInteger(policy_id, 7, Fn.LEFT, True, 0)+".TXT"
    invoice_file = open_file(invoice_filename, "w")
    file_list.append(invoice_file)
    for invoice_printout_line in invoice_printout:
        write_file(invoice_file, invoice_printout_line+"\n")
    invoice_file.close()
      
    # making backup of the policies file
    backup_file(POLICY_FILENAME)
    
    # opening the policies data file with append mode
    policy_file = open_file(POLICY_FILENAME, "a")
    file_list.append(policy_file)
    
    policy_str =  ""
    for i in range(number_of_data_entries_in_policy):
        if i == 0 or i == 9 or i == 14 or i == 15:
            f_str = format_settings_value(policy_information[-1][i])
        elif i == 13:
            f_str = PAYTYPES[policy_information[-1][i]][0]
        elif i == 1:
            f_str = policy_information[-1][i].strftime("%Y-%m-%d")
        else:
            # ideally I need to use double quotes, because address can contain commas
            # but skip for now
            #f_str = '"{}"'.format(policy_information[last_policy_index][i])
            f_str = policy_information[-1][i]
            
        policy_str += f_str + CMM * int((i+1) != number_of_data_entries_in_policy)

    write_file(policy_file, policy_str+"\n", True)
    policy_file.close()    
    
    # opening the claims history data file with append mode
    if claim_count > 0:
        
        # making backup of the claims file
        backup_file(CLAIMS_FILENAME)

        claims_file = open_file(CLAIMS_FILENAME, "a")
        file_list.append(claims_file)
        
        for i in range(claim_count):
            claim_str = ""
            claim_record_length = len(policy_information[-1][-1][i])
            for j in range(claim_record_length):
                if j == 3:
                    f_str = policy_information[-1][-1][i][j].strftime("%Y-%m-%d")
                else:
                    f_str = format_settings_value(policy_information[-1][-1][i][j])
                    
                claim_str += f_str + CMM * int((j+1) != claim_record_length)
            
            write_file(claims_file, claim_str+"\n", True)
        
        claims_file.close()

    # emptying non-essential lists for the next loop iteration
    invoice_printout.clear()
    policy_past_claims.clear()
    
    # increasing the policy number
    NEXTPOLICY += 1
    SETTINGS_FILENAME_FIELDS[0][0] = NEXTPOLICY
        
    # making backup of the settings file    
    backup_file(SETTINGS_FILENAME)
        
    # opening the settings data file           
    settings_file = open_file(SETTINGS_FILENAME, "w")
    file_list.append(settings_file)    

    # rewriting the settings file with the new NEXTPOLICY value
    for i in range(len(SETTINGS_FILENAME_FIELDS)):
        settings_str =  SETTINGS_FILENAME_FIELDS[i][1] + \
                        " " + SETTINGS_FILENAME_SEPARATOR + " " + \
                        format_settings_value(SETTINGS_FILENAME_FIELDS[i][0]) + \
                        " " + SETTINGS_FILENAME_SEPARATOR + " " + \
                        SETTINGS_FILENAME_FIELDS[i][2]+ "\n"
        write_file(settings_file, settings_str, True)                
            
    settings_file.close()        

    # end file operations, enable Ctrl-C
    signal.signal(signal.SIGINT, handle_ctrl_c)

    print(); print()
    #print(Fn.FormatStrg(CH2 * (COLPRINTWIDTH-20), CLAIMPRINTWIDTH, Fn.CENTER))
    print(Fn.FormatString("Storing Policy #".upper() + Fn.FormatInteger(policy_id,7,Fn.LEFT, True, 0) + " Information...".upper(), CLAIMPRINTWIDTH, Fn.CENTER))
    message_status = f"Saving files '{POLICY_FILENAME}' and '{CLAIMS_FILENAME}...'"    
    print(Fn.FormatString(CH1 * (len(message_status)+10), CLAIMPRINTWIDTH, Fn.CENTER))
    progress_rotating(100, message_status, "SUCCESS!", len(message_status)+10, CLAIMPRINTWIDTH, 0.1, 2, 4)
    print(Fn.FormatString("Data Was Saved Successfully!".upper(), CLAIMPRINTWIDTH, Fn.CENTER))
    print(Fn.FormatString(CH1 * (len(message_status)+10), CLAIMPRINTWIDTH, Fn.CENTER))
    print(Fn.FormatString("Invoice was saved in file "+invoice_filename, CLAIMPRINTWIDTH, Fn.CENTER))
    print(); print()
    print(Fn.FormatString("The System is Ready To Process Next Policy.".upper(), CLAIMPRINTWIDTH, Fn.CENTER))
    print(Fn.FormatString("Press Any Key...".rstrip().upper(), CLAIMPRINTWIDTH, Fn.CENTER), end="\r"); input()
    print(); print(); print()
    
    policy_count += 1
          
exit(0)          
