from urlextract import URLExtract
import matplotlib.pyplot as plt
import emoji
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
extract=URLExtract()

def fetch_stats(Selected_user,Df):
    ## Here we will be feching the Number of Words and Messeges
    ## Here we will be feching total Number of Urls
    links=[]
    for messge in Df['Message']:
        links.extend(extract.find_urls(messge))
    if Selected_user=="Overall":

        num_Messeges=Df.shape[0]
        words = []
        Media_Files = Df[Df['Message'] == '<Media omitted>\n'].shape[0]
        for message in Df["Message"]:
            words.extend(message.split())
            ## Here we will be extracting the Number of Media files tranfersed between them

        return num_Messeges,len(words), Media_Files,len(links)


    else:
        ## Here these is called masking means here we are analysis that in the Column Named User
        ## How many people like of selected user can be anything like Meghna or Shwetha mam it will show their NUMber of Messges
        new_Df=  Df[Df['users']==Selected_user]
        new_messeges=new_Df.shape[0]
        words = []
        for message in new_Df["Message"]:
            words.extend(message.split())
            Media_Files = Df[Df['Message'] == '<Media omitted>\n'].shape[0]
        return new_messeges,len(words),Media_Files,len(links)
def Most_Busy(Df):
    x = Df["users"].value_counts().head()
    ## Here we willget How much has each Person Has Percentages in Chats  Here we can aslo convert it inro the Datframe
    ## Dont be Confused The column Names will be Taken when we enter the reset.index

    DATABASE= round((Df["users"].value_counts() / Df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percent'})
    return x,DATABASE
def WorldCloud (Selected_user,Df):
    if Selected_user!='Overall':
        Df=Df[Df['users']==Selected_user]
    wc=WordCloud(width=500,height=500,background_color='white')
    df_wc=wc.generate(Df['Message'].str.cat(sep=''))
    return df_wc
def MostCommon_Words(Selected_user,Df):
    if Selected_user!='Overall':
        Df=Df[Df['users']==Selected_user]
    ## Here we will removing soem words like Stop Words Group Notificationa
    ## And then we need to remove Media Ommitedd Word
    temp = Df[Df['users'] != "group"]
    ## !!Here one more thing is you can also use temp as df now
    ## Now will be removing the Media omitted part
    temp = temp[temp['Message'] != "<Media omitted>\n"]
    ## Now here you will get the temp dataframe where there will be no messegs like media ommited and no users like gruop
    words = []
    for messege in temp['Message']:
        words.extend(messege.split())
    D=pd.DataFrame(Counter(words).most_common(20))
    return  D

def Emojis_Analyser(Selected_user,Df):
    if Selected_user != 'Overall':
        Df = Df[Df['users'] == Selected_user]
    emojis = []

    for message in Df['Message']:
        emojis.extend([ch for ch in message if emoji.is_emoji(ch)])

    ## Here we will be converting thise emojis and getting top 20 one
    Emoji_Df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return Emoji_Df

def Monthly_Users(Selected_user,Df):
    if Selected_user != 'Overall':
        Df = Df[Df['users'] == Selected_user]
    timeline = Df.groupby(['Year', 'month_num', 'Month']).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        ## Here we will be using the str in year beacuse since moth is a string to add them we need to use these
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))
    timeline['time'] = time
    return timeline

def Daily_Tiemline(Selected_user,Df):
    if Selected_user != 'Overall':
        Df = Df[Df['users'] == Selected_user]
    daily_timeline = Df.groupby('only_Date').count()['Message'].reset_index()
    return daily_timeline

def Day_Timeline(Selected_user,Df):
    if Selected_user != 'Overall':
        Df = Df[Df['users'] == Selected_user]
    Day_Time=Df["Day_Name"].value_counts()
    return Day_Time

def Month_Active(Selected_user,Df):
    if Selected_user != 'Overall':
        Df = Df[Df['users'] == Selected_user]
    return Df["Month"].value_counts()

def Activity_HeatMap(Selected_user,Df):
    if Selected_user != 'Overall':
        Df = Df[Df['users'] == Selected_user]
    Activity=Df.pivot_table(index="Day_Name", columns="Period", values="Message", aggfunc='count').fillna(0)
    return Activity

