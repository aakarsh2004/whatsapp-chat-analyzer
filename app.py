import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.markdown("<h1 style='text-align: center; color: #FFA500;'>📊 Top Statistics</h1>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("<h2 style='text-align: center; color: #FF5733;'>💬 Total Messages</h2>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: #3498DB;'>{num_messages}</h1>", unsafe_allow_html=True)

        with col2:
            st.markdown("<h2 style='text-align: center; color: #FF5733;'>📝 Total Words</h2>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: #3498DB;'>{words}</h1>", unsafe_allow_html=True)

        with col3:
            st.markdown("<h2 style='text-align: center; color: #FF5733;'>📷 Media Shared</h2>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: #3498DB;'>{num_media_messages}</h1>", unsafe_allow_html=True)

        with col4:
            st.markdown("<h2 style='text-align: center; color: #FF5733;'>🔗 Links Shared</h2>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: #3498DB;'>{num_links}</h1>", unsafe_allow_html=True)
                # monthly timeline    
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(timeline['time'], timeline['message'], color='green', linewidth=2, marker='o', markersize=6)
        # Set the background color of the plot
        ax.set_facecolor("#F8F9F9")  # Light gray for a modern, clean look

        # Set X-axis label with background color and arrow
        ax.set_xlabel(
            "Time →",
            fontsize=16,
            color="#34495E",  # Charcoal gray
            labelpad=12,
            weight='semibold',
            bbox=dict(facecolor="#EAF2F8", edgecolor="none", boxstyle="round,pad=0.3")  # Light blue background
        )

        # Set Y-axis label with background color and arrow
        ax.set_ylabel(
            "Number of Messages →",
            fontsize=16,
            color="#34495E",  # Gold
            labelpad=12,
            weight='semibold',
            bbox=dict(facecolor="#EAF2F8", edgecolor="none", boxstyle="round,pad=0.3")  # Light yellow background
        )

        ax.set_title("Messages Over Time", fontsize=16, color="black", weight='bold', pad=15)
        ax.tick_params(axis='x', labelsize=12, rotation=45, colors="black")
        ax.tick_params(axis='y', labelsize=12, colors="black")
        ax.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.7)

        st.pyplot(fig)
        
       

        # daily timeline
        st.title("📅 Daily Timeline")

        # Fetch daily timeline data
        daily_timeline = helper.daily_timeline(selected_user, df)

        # Create a figure
        fig, ax = plt.subplots(figsize=(10, 5))

        # Plot with improved styling
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#2E86C1', linewidth=2, marker='o', markersize=6, markerfacecolor='red')

        # Set background color
        ax.set_facecolor("#F8F9F9")  # Light gray for a modern, clean look

        # Set X-axis label
        ax.set_xlabel(
            "Date →",
            fontsize=14,
            color="#1C2833",  # Dark gray
            labelpad=10,
            weight='semibold'
        )

        # Set Y-axis label
        ax.set_ylabel(
            "Number of Messages →",
            fontsize=14,
            color="#1C2833",  
            labelpad=10,
            weight='semibold'
        )

        # Set title with styling
        ax.set_title("Daily Message Trend ", fontsize=16, color="black", weight='bold', pad=15)

        # Rotate x-axis labels for readability
        ax.tick_params(axis='x', labelsize=12, rotation=45, colors="black")
        ax.tick_params(axis='y', labelsize=12, colors="black")

        # Add grid for better readability
        ax.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.7)

        # Display the plot in Streamlit
        st.pyplot(fig)


                # activity map
        st.title("📍 Activity Map")

        col1, col2 = st.columns(2)

        # --- Most Busy Day ---
        with col1:
            st.markdown("<h3 style='text-align: center; color: #8E44AD;'>📆 Most Busy Day</h3>", unsafe_allow_html=True)
            
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 4))
            
            ax.bar(busy_day.index, busy_day.values, color='#8E44AD', alpha=0.85, edgecolor='black', linewidth=1.2)
            
            ax.set_facecolor("#F8F9F9")
            ax.set_xlabel("Day of the Week", fontsize=12, weight='bold', color="#2C3E50")
            ax.set_ylabel("Message Count", fontsize=12, weight='bold', color="#2C3E50")
            ax.set_title("Messages per Day", fontsize=14, weight='bold', color="black")
            
            ax.tick_params(axis='x', labelsize=11, rotation=45, colors="black")
            ax.tick_params(axis='y', labelsize=11, colors="black")
            
            ax.grid(axis='y', linestyle="--", linewidth=0.6, alpha=0.7)
            
            st.pyplot(fig)

        # --- Most Busy Month ---
        with col2:
            st.markdown("<h3 style='text-align: center; color: #E67E22;'>📅 Most Busy Month</h3>", unsafe_allow_html=True)
            
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 4))
            
            ax.bar(busy_month.index, busy_month.values, color='#E67E22', alpha=0.85, edgecolor='black', linewidth=1.2)
            
            ax.set_facecolor("#F8F9F9")
            ax.set_xlabel("Month", fontsize=12, weight='bold', color="#2C3E50")
            ax.set_ylabel("Message Count", fontsize=12, weight='bold', color="#2C3E50")
            ax.set_title("Messages per Month", fontsize=14, weight='bold', color="black")
            
            ax.tick_params(axis='x', labelsize=11, rotation=45, colors="black")
            ax.tick_params(axis='y', labelsize=11, colors="black")
            
            ax.grid(axis='y', linestyle="--", linewidth=0.6, alpha=0.7)
            
            st.pyplot(fig)


        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_font = fm.FontProperties(fname="fonts/SegoeUIEmoji.ttf", size=14)

        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(emoji_df["Count"].head(), 
                labels=emoji_df["Emoji"].head(), 
                autopct="%0.2f%%", 
                startangle=90,
                textprops={'fontproperties': emoji_font})
            ax.axis("equal")
            fig.tight_layout()
            st.pyplot(fig)
            