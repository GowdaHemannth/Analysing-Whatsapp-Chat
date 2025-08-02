import re
import pandas as pd


def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\u202f|\s)?(?:AM|PM|am|pm)?\s*-\s'

    # Fix: Correctly indented this line
    messeges = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create dataframe
    df = pd.DataFrame({'User_Messages': messeges, 'Date': dates})

    # Step 0: Ensure 'Date' is string type
    df['Date'] = df['Date'].astype(str)

    # Step 1: Clean Unicode narrow space (WhatsApp uses \u202f before AM/PM)
    df['Date'] = df['Date'].str.replace('\u202f', ' ', regex=True)

    # Step 2: Remove trailing ' -' from each string
    df['Date'] = df['Date'].str.replace(r'\s*-\s*$', '', regex=True)

    # Step 3: Convert to proper datetime
    df['Date'] = pd.to_datetime(df['Date'], format="%m/%d/%y, %I:%M %p", errors='coerce')

    users = []
    Message = []
    for messages in df['User_Messages']:
        entry = re.split(r'([\w\W]+?):\s', messages)
        if entry[1:]:
            users.append(entry[1])
            Message.append(entry[2])
        else:
            users.append('group')
            Message.append(entry[0])

    df['users'] = users
    df['Message'] = Message
    df.drop(columns=['User_Messages'], inplace=True)
    df['Month'] = df['Date'].dt.month_name()
    df['Year'] = df['Date'].dt.year
    df['month_num'] = df['Date'].dt.month
    df['only_Date'] = df['Date'].dt.date
    df['Day'] = df['Date'].dt.day
    df["Day_Name"] = df["Date"].dt.day_name()

    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute
    period = []
    for hour in df[["Day_Name", "Hour"]]["Hour"]:
        if hour == 23:
            period.append(str(hour) + "-" + str(00))
        elif hour == 0:
            period.append(str(00) + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df["Period"] = period
    return df
