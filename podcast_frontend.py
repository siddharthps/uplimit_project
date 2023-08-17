import streamlit as st
import json
import os
import modal

def main():
    # Toggle for dark mode / light mode
    st.sidebar.write("Choose Color Mode:")
    color_mode = st.sidebar.radio("", ("Light", "Dark"))

    if color_mode == "Dark":
        st.markdown(
            """
            <style>
            body {
                background-color: #121212;
                color: #FFFFFF;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
            body {
                background-color: #FFFFFF;
                color: #000000;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    # Main content
    st.title("Newsletter Dashboard")

    available_podcast_info = create_dict_from_json_files('.')

    st.sidebar.header("Podcast RSS Feeds")
    selected_podcast = st.sidebar.selectbox("Select Podcast", options=available_podcast_info.keys())

    if selected_podcast:
        podcast_info = available_podcast_info[selected_podcast]

        st.header("Podcast Episode Summary")
        st.write(podcast_info['podcast_summary'])

        st.image(podcast_info['podcast_details']['episode_image'], caption="Podcast Cover", width=300, use_column_width=True)

        st.subheader("Podcast Guest")
        st.write(podcast_info['podcast_guest'])

        st.subheader("Podcast Guest Details")
        st.write(podcast_info["podcast_guest"]['summary'])

        st.subheader("Key Moments")
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

    # User Input box
    st.sidebar.subheader("Add and Process New Podcast Feed")
    url = st.sidebar.text_input("Link to RSS Feed")

    process_button = st.sidebar.button("Process Podcast Feed")
    st.sidebar.markdown("**Note**: Podcast processing can take up to 5 mins, please be patient.")

    if process_button:
        podcast_info = process_podcast_info(url)

        st.header("Podcast Episode Summary")
        st.write(podcast_info['podcast_summary'])

        st.image(podcast_info['podcast_details']['episode_image'], caption="Podcast Cover", width=300, use_column_width=True)

        st.subheader("Podcast Guest")
        st.write(podcast_info['podcast_guest'])

        st.subheader("Podcast Guest Details")
        st.write(podcast_info["podcast_guest"]['summary'])

        st.subheader("Key Moments")
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data_dict = {}

    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            podcast_info = json.load(file)
            podcast_name = podcast_info['podcast_details']['podcast_title']
            data_dict[podcast_name] = podcast_info

    return data_dict

def process_podcast_info(url):
    f = modal.Function.lookup("corise-podcast-project", "process_podcast")
    output = f.call(url, '/content/podcast/')
    return output

if __name__ == '__main__':
    main()
