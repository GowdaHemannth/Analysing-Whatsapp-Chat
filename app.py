from pydoc import Helper
import seaborn as sns
import streamlit as st
import Preprocessor,helper
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp-Chat- Analysis ")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    Data= bytes_data.decode("utf-8")
    Df=Preprocessor.preprocess(Data)
    st.dataframe(Df)
    ## Fetch the Unique Users
    user_List=Df['users'].unique().tolist()

    user_List.remove('group')
    user_List.sort()
    user_List.insert(0,"Overall")
    Selected_user=st.sidebar.selectbox("Show Analysis with respect to user list", user_List)
    if st.sidebar.button("Show Analysis"):
        num_messges,words,Media,Links= helper.fetch_stats(Selected_user,Df)
        col1,col2,col3,col4=st.columns(4)
        st.title("Top-Statics-Analysis")
        with col1:
            st.header("Total-No-Messsges")
            st.title(num_messges)

        with col2:
            st.header("Total-No-Words ")
            st.title(words)

        with col3:
            st.header("Total-No-Media Files")
            st.title(Media)
        with col4:
            st.header("Total-No-Links")
            st.title(Links)

        ## Here we will see the  MOnthlyTime line
        Time_Line=helper.Monthly_Users(Selected_user,Df)
        st.title("Timeline of Messges")
        fig,ax=plt.subplots()
        ax.plot(Time_Line['time'],Time_Line['Message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        ## Here you will see the Daily Timelinne'
        DDDTime_Line = helper.Daily_Tiemline(Selected_user, Df)
        st.title("Daily-Timeline of Messges")
        fig, ax = plt.subplots()
        ax.plot(DDDTime_Line['only_Date'], DDDTime_Line['Message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        ## Here we will be seeing the buiest Day
        st.title("Activity-Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Busy-Day")
            busy_day=helper.Day_Timeline(Selected_user, Df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Busy_Month")
            busy_month=helper.Month_Active(Selected_user, Df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values, color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        ## Here we will be Listing the Busiest Persons
        if Selected_user=="Overall":
            st.title("Most Active Person ")
            x,Database=helper.Most_Busy(Df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(Database)
    ## Here we will be Doing the HeatMap thing
            st.title("Heat-Map-Showing-Distribution")
            user_Activity=helper.Activity_HeatMap(Selected_user,Df)
            fig,ax=plt.subplots()
            ax=sns.heatmap(user_Activity)
            st.pyplot(fig)
    ## Here we will be Creating a World Cloud
        st.title("Word-Cloud-Analysis ")
        df_wc=  helper.WorldCloud(Selected_user,Df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

    ## Here we will be Getting top 20 Common Words
        Most_Common_Words= helper.MostCommon_Words(Selected_user, Df)
        fig,ax=plt.subplots()
        ## Here Based on the x ,y Axis Will be Seated
        ax.bar(Most_Common_Words[0],Most_Common_Words[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

    ## Here we will get the Emoji Analyser
        emoji_Df=helper.Emojis_Analyser(Selected_user,Df)
        st.title("Emoji-Analysis")
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_Df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_Df[1],labels=emoji_Df[0])
            st.pyplot(fig)









