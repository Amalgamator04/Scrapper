import streamlit as st
from icrawler.builtin import GoogleImageCrawler
import shutil
import os


# Function to clear the directory
def clear_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


# Function to download images
def download_images(query, max_num=10, output_dir='downloads'):
    # Ensure the output directory exists and is clean
    clear_directory(output_dir)

    google_crawler = GoogleImageCrawler(storage={'root_dir': output_dir})
    google_crawler.crawl(keyword=query, max_num=max_num, file_idx_offset='auto')


# Function to zip the directory
def zip_directory(directory, zip_name):
    zip_path = shutil.make_archive(zip_name, 'zip', directory)
    return zip_path


# Set up custom CSS for background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: purple;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app title
st.title('Google Image Scraper')

# Input fields
search_query = st.text_input('Search Query', 'puppies')
max_images = st.number_input('Max Images', min_value=1, value=5)
output_directory = st.text_input('Output Directory', 'images')
zip_file_name = st.text_input('Zip File Name', 'downloaded_images')

# Download button
if st.button('Download Images'):
    with st.spinner('Downloading images...'):
        download_images(search_query, max_images, output_directory)
        zip_path = zip_directory(output_directory, zip_file_name)
        st.success('Download complete!')
        st.write(f"Images are zipped at: {zip_path}")
        with open(zip_path, 'rb') as f:
            st.download_button('Download Zip', f, file_name=f"{zip_file_name}.zip")
