
import streamlit as st
import modal
import json
import os

def main():
    st.title("Podcast Insights Hub")

    available_podcast_info = create_dict_from_json_files('.')

    # Left section - Input fields
    sidebar = st.sidebar
    sidebar.subheader("Available Podcasts Feeds")
    selected_podcast = sidebar.selectbox("Select Podcast", options=available_podcast_info.keys())

    if selected_podcast:

        podcast_info = available_podcast_info[selected_podcast]

        # Display the podcast title
        episode_title = podcast_info['podcast_details']['episode_title']
        st.subheader("Episode Title")
        st.write(episode_title, unsafe_allow_html=True)

        # Display the podcast summary and the cover image
        col1, col2 = st.columns([5, 5])

        with col1:
            # Display the podcast episode summary
            st.subheader("Podcast Episode Summary")
            st.write(podcast_info['podcast_summary'])

        with col2:
            # Display the podcast episode image
            st.image(podcast_info['podcast_details']['episode_image'], width=300, use_column_width=True)

        # Display the podcast guest and their details
        guest_info = podcast_info['podcast_guest']
        if isinstance(guest_info, dict):
            guest_name = guest_info.get('name', 'Guest Name Not Available')
        else:
            guest_name = guest_info

        st.subheader("Podcast Guest")
        st.write(guest_name)

        # Display the podcast top quote
        st.subheader("Podcast Top Quote")
        st.write(podcast_info["get_podcast_topquote"])

        # Display the episode highlights
        st.subheader("Episode Highlights")
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(
                f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

    # User Input box
    sidebar.subheader("Add and Process New Podcast Feed")
    url = sidebar.text_input("Link to RSS Feed")

    process_button = sidebar.button("Process Podcast Feed")
    sidebar.markdown("**Note**: Podcast processing can take up to 5 mins, please be patient.")

    if process_button:

        # Call the function to process the URLs and retrieve podcast guest information
        podcast_info = process_podcast_info(url)

        # Right section - Newsletter content
        st.header("Newsletter Content")

        # Display the podcast title
        episode_title = podcast_info['podcast_details']['episode_title']
        st.subheader("Episode Title")
        st.write(episode_title, unsafe_allow_html=True)

        # Display the podcast summary and the cover image
        col1, col2 = st.columns([5, 5])

        with col1:
            # Display the podcast episode summary
            st.subheader("Podcast Episode Summary")
            st.write(podcast_info['podcast_summary'])

        with col2:
            # Display the podcast episode image
            st.image(podcast_info['podcast_details']['episode_image'], width=300)

        # Display the podcast guest and their details
        guest_info = podcast_info['podcast_guest']
        if isinstance(guest_info, dict):
            guest_name = guest_info.get('name', 'Guest Name Not Available')
        else:
            guest_name = guest_info

        st.subheader("Podcast Guest")
        st.write(guest_name)

        # Display the podcast top quote
        st.subheader("Podcast Top Quote")
        st.write(podcast_info["get_podcast_topquote"])

        # Display the episode highlights
        st.subheader("Episode Highlights")
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(
                f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data_dict = {}

    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            podcast_info = json.load(file)
            podcast_name = podcast_info['podcast_details']['podcast_title']
            # Process the file data as needed
            data_dict[podcast_name] = podcast_info

    return data_dict

def process_podcast_info(url):
    f = modal.Function.lookup("corise-podcast-project", "process_podcast")
    output = f.call(url, '/content/podcast/')
    return output

if __name__ == '__main__':
    main()

