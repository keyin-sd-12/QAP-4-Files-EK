"""  
QAP-4, EK, SD-12 Group17
"""

import datetime, math

LEFT="left"
RIGHT="right"
CENTER="center"
ENDSTR="-END"
NEGONE=-1
DOLLAR = "$"
PERCENT = "%"
DATESPLIT = "-"

# function to validate string input
def ValidStringInput(Prompt, MinLength, MaxLength, AllowedSet, WhitespaceAllowed = False, RemoveSpaces = False, AllowEmpty = False, IgnoreCase = False):
    # print("Allowed characters are:", AllowedSet)
    while True:
        StringInput = input(Prompt).strip()
        if IgnoreCase: StringInput = StringInput.upper()
        if AllowEmpty and StringInput == "": return ""
        if StringInput.upper() == ENDSTR:
            return ENDSTR
        #if len(StringInput) == 0:
            #print("Invalid input: cannot be blank.")
        elif (len(StringInput) < MinLength) or (len(StringInput) > MaxLength):
            if MinLength == MaxLength:
                print(f"Invalid input: must be exactly {MinLength} characters.")
            else:
                print(f"Invalid input: must be {MinLength}-{MaxLength} characters.")
        elif (not WhitespaceAllowed) and (" " in StringInput):
            print("Invalid input: whitespace not permitted.")
        elif (isinstance(AllowedSet, set) and (not set(StringInput).issubset(AllowedSet))) or \
             (isinstance(AllowedSet, list) and (StringInput not in AllowedSet)):
            print("Invalid input: not permitted character(s).")
        else:
            if RemoveSpaces:
                StringInput = StringInput.replace(" ", "")
            return StringInput

def ValidPostalCode(InputPrompt, MinLength, MaxLength, AllowedSet):
    while True:
        StringInput = ValidStringInput(InputPrompt, MinLength, MaxLength, AllowedSet, True, True, True, True)
        if (len(StringInput) == 6 and StringInput[0].isalpha() and StringInput[1].isdigit() and \
            StringInput[2].isalpha() and StringInput[3].isdigit() and StringInput[4].isalpha() and \
            StringInput[5].isdigit()) or (StringInput == ""): 
            return StringInput
        else:
            print("Invalid input. Please enter a valid postal code.")
            
def ValidPhoneNumber(InputPrompt, MinLength, MaxLength, AllowedSet, AllowedSeparatorSet):            
    while True:
        StringInput = ValidStringInput(InputPrompt, MinLength, MaxLength, AllowedSet, True, True, True)
        StringInput = ''.join([char for char in StringInput if char not in AllowedSeparatorSet])
        if (len(StringInput) == 10 and StringInput.isdigit()) or (StringInput == ""):
            return StringInput
        else:
            print("Invalid input. Please enter a valid phone number.")

# function to check if Integer1 is divisible by Integer2
def Divisible(Integer1, Integer2):
    if Integer1 % Integer2 == 0:
        return True
    else:
        return False

# function to validate integer input (within specified bounds)
def ValidIntegerInput(InputPrompt, LowerBound, UpperBound, EnterAllowed = False, DefaultValue = 0, NegOneAllowed = False):
    while True:
        UserInput = input(InputPrompt)
        if EnterAllowed and UserInput == "":
            return DefaultValue
        try:
            Value = int(UserInput)
            if (NegOneAllowed and (Value == NEGONE)) or ((Value >= LowerBound) and (Value <= UpperBound)):
                return Value
            else: 
                print(f"Invalid input: value must be between {LowerBound} and {UpperBound}.")
        except ValueError:
            print("Invalid input: must be integer.")    

# function to validate float input (within specified bounds)
def ValidFloatInput(InputPrompt, LowerBound, UpperBound, EnterAllowed = False, DefaultValue = 0.00):
    while True:
        UserInput = input(InputPrompt)
        if EnterAllowed and UserInput == "":
            return DefaultValue
        try:
            Value = float(UserInput)
            if Value < LowerBound or Value > UpperBound:
                print(f"Invalid input: value must be between {LowerBound:.2f} and {UpperBound:.2f}.")
            else:
                return Value
        except ValueError:
            print("Invalid input: must be a valid real number.")    
            
# function to validate date input in the format YYYY-MM-DD            
def ValidDateInput(InputPrompt, AllowedSet = set("ABCDEFGHIJKLMONPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-/ "), DefaultAllowed = False, DefaultDate = datetime.datetime.now(), AllowFuture=False):
    current_date = datetime.datetime.now()
    while True:
        UserInput = ValidStringInput(InputPrompt, 1, 20, AllowedSet, True, False, True, False)
        if UserInput == "": return DefaultDate
        UserInput = UserInput.replace(" ", DATESPLIT)
        UserInput = UserInput.replace("/", DATESPLIT)
        try:
            # try validate "YYYY-MM-DD" format
            validated_date = datetime.datetime.strptime(UserInput, "%Y-%m-%d")
            if not AllowFuture and validated_date > current_date:
                print("Invalid input: Date cannot be in the future.")
            else:   
                return validated_date
        except ValueError:
            # print("Invalid date format Step 1. Please, try again.")
            # if not validated try to validate "YYYY-MON-DD" format
            # split user input into 3 parts
            UserInputSplitted = UserInput.split(DATESPLIT)
            if len(UserInputSplitted) == 3:
                # Convert month to title case FEB or feb to "Feb"
                UserInputSplitted[1] = UserInputSplitted[1].title()  # Convert month to title case (e.g., JAN -> Jan)
                UserInput = '-'.join(UserInputSplitted)
                # print(UserInput)
                try: 
                    validated_date = datetime.datetime.strptime(UserInput, "%Y-%b-%d")
                    if not AllowFuture and validated_date > current_date:
                        print("Invalid input: Date cannot be in the future.")
                    else:   
                        return validated_date
                except ValueError:
                    print("Invalid date format. Please, try again.")
            else:
               print("Invalid date format. Please, try again.")
              
# function to format String to specified specified Width
# alignment is either "left", "right", or "center"
# if input string is longer than Width, it is truncated
# returns formatted string
def FormatString(String, Width, Alignment, Filler=" "):
    if len(String) > Width:
        String = String[:Width]
    if Alignment == "left":
        return f"{String:<{Width}}"
    elif Alignment == "right":
        return f"{String:>{Width}}"
    elif Alignment == "center":
        return f"{String:^{Width}}"
    else:
        return String
    
# function to format Float to specified Width and Precision
# adds Symbol to the left side of the number
def FormatFloat(Symbol, Float, Width, Precision, Alignment, SymbolOnRight = False):
    if SymbolOnRight:
        FormattedNumber = f"{Float:,.{Precision}f}"+Symbol
    else:
        if Float < 0:
            FormattedNumber = f"-{Symbol}{abs(Float):,.{Precision}f}"
        else:
            FormattedNumber = f"{Symbol}{Float:,.{Precision}f}"    
        # FormattedNumber = Symbol+f"{Float:,.{Precision}f}"    
    if Alignment == "left":
        return f"{FormattedNumber:<{Width}s}"
    elif Alignment == "right":
        return f"{FormattedNumber:>{Width}s}"
    elif Alignment == "center":
        return f"{FormattedNumber:^{Width}s}"
    else:
        return FormattedNumber

# function to format Integer to specified Width    
def FormatInteger(Integer, Width, Alignment, ZeroPadding=False, PadToWidth=0):
    if (PadToWidth == 0) or (PadToWidth >= Width): PadToWidth = Width
    if ZeroPadding:
        Integer_str = f"{Integer:0{PadToWidth}d}"
    else:
        Integer_str = str(Integer)
    
    if Alignment == "left":
        return f"{Integer_str:<{Width}}"
    elif Alignment == "right":
        return f"{Integer_str:>{Width}}"
    elif Alignment == "center":
        return f"{Integer_str:^{Width}}"
    else:
        return Integer_str

# - old version of the function
# function to format Integer to specified Width    
# def FormatInteger(Integer, Width, Alignment, ZeroPadding = False):
#     if Alignment == "left":
#         return f"{Integer:<{Width}}"
#     elif Alignment == "right":
#         return f"{Integer:>{Width}}"
#     elif Alignment == "center":
#         return f"{Integer:^{Width}}"
#     else:
#         return f"{Integer}"
# - end of old version

# function takes two strings and a Width as input. 
# returns a new string of the specified width. 
# in the new string, the first input string is left-justified, 
# and the second input string is right-justified. 
# the space between the two strings is filled with spaces. 
# if the combined length of the two strings is greater 
# than the specified width, the second string is truncated from the left.
def JustifyText (LeftString, RightString, Width):
    RemainingSpace = Width - len(LeftString)
    Padding = ""
    if RemainingSpace <= 0:
        return LeftString[:Width]
    elif RemainingSpace < len(RightString):
        RightString = RightString[len(RightString) - RemainingSpace:]
    elif RemainingSpace > len(RightString):
        Padding = " " * (RemainingSpace - len(RightString))
    
    # Return the justified string
    return (LeftString + Padding + RightString)[:Width]

# function to add NMonths to a date object
def AddMonths(DateObject, NMonths):
    # extract all attributes
    Year = DateObject.year
    Month = DateObject.month
    Day = DateObject.day
    Hour = DateObject.hour
    Minute = DateObject.minute
    Second = DateObject.second
    Microsecond = DateObject.microsecond

    # add NMonths
    NewMonth = Month + NMonths
    
    # check if the new month is greater than 12
    NewYear = Year + ((NewMonth - 1) // 12)
    # adjust the month
    NewMonth = ((NewMonth - 1) % 12) + 1
    
    # figure out the last day of the new month
    if NewMonth == 12:
        NewMonthLastDay = 31
    else:
        NewMonthLastDay = (datetime.datetime(NewYear, NewMonth + 1, 1) - datetime.timedelta(days=1)).day

    # adjust if new month doesn't have the same day (e.g., Feb 28th to Feb 29th)
    NewDay = min(Day, NewMonthLastDay)

    return datetime.datetime(NewYear, NewMonth, NewDay, Hour, Minute, Second, Microsecond)

# function to add NYears to a date object
def AddYears(DateObject, NYears):
    # extract all attributes
    Year = DateObject.year
    Month = DateObject.month
    Day = DateObject.day
    Hour = DateObject.hour
    Minute = DateObject.minute
    Second = DateObject.second
    Microsecond = DateObject.microsecond

    # add NYears
    NewYear = Year + NYears
    
    # figure out the last day of the current month in the new year
    if Month == 12:
        NewMonthLastDay = 31
    else:
        NewMonthLastDay = (datetime.datetime(NewYear, Month + 1, 1) - datetime.timedelta(days=1)).day

    # adjust if new year doesn't have the same day (e.g., Feb 28th to Feb 29th)
    NewDay = min(Day, NewMonthLastDay)

    return datetime.datetime(NewYear, Month, NewDay, Hour, Minute, Second, Microsecond)




