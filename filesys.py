import streamlit as st
import json
import os

DATA_FOLDER='.data/filesys'

@st.cache_resource
def init():
  if not os.path.exists(DATA_FOLDER):
    os.makedirs(folder_path, exist_ok=True)

init()

view_tab, create_tab, upload_tab = st.tabs(['Edit/View', 'Create', 'Upload'])
  
with view_tab:
  # Simple file selection from server
  file_list = os.listdir(DATA_FOLDER) 
  selected_file = st.selectbox('Or select a file to edit', file_list)
  
  if selected_file:
    file_path = os.path.join(DATA_FOLDER, selected_file)
    with open(file_path, 'r') as file:
      if selected_file.endswith('.json'):
        content = json.load(file)  # Load JSON file
        edited_content = st.text_area("Edit JSON", value=json.dumps(content, indent=2), key='1')
      else:
        content = file.read()  # Read text file
        edited_content = st.text_area("Edit Text", value=content, key='2')
    
    # Save button for server file
    if st.button('Save Server File'):
      with open(file_path, 'w') as file:
        if selected_file.endswith('.json'):
          json.dump(json.loads(edited_content), file, indent=2)  # Save edited JSON
        else:
          file.write(edited_content)  # Save edited text
      st.success('File saved successfully!')

# Create or upload a file:
with create_tab:
  new_file_name = st.text_input("Enter the name of the new file (with extension)", "", key='3')
  new_file_content = st.text_area("Enter the content for the new file", "", key='4')

  # Save button for the new file
  if st.button("Create File"):
      if new_file_name:  # Check if the filename is not empty
          # Specify the directory to save the file, here it's the current directory
          save_path = os.path.join(DATA_FOLDER, new_file_name)
          # Create and save the new file
          with open(save_path, 'w') as new_file:
              new_file.write(new_file_content)
          st.success(f"File '{new_file_name}' created successfully!")
      else:
          st.error("Please enter a valid filename.")

with upload_tab:
  uploaded_file = st.file_uploader("Upload a file", type=['txt', 'json'])

  # Process the uploaded file
  if uploaded_file is not None:
    # To read file as string:
    content = uploaded_file.getvalue().decode("utf-8")
  
    if uploaded_file.name.endswith('.json'):
      content = json.loads(content)  # Parse string to JSON
      edited_content = st.text_area("Edit JSON", value=json.dumps(content, indent=2), key='5')
    else:
      edited_content = st.text_area("Edit Text", value=content, key='6')
  
    # Save button for uploaded file
    if st.button('Save Uploaded File'):
      # Choose a path to save the file
      save_path = os.path.join(DATA_FOLDER, uploaded_file.name)
      
      with open(save_path, 'w') as file:
        if uploaded_file.name.endswith('.json'):
          json.dump(json.loads(edited_content), file, indent=2)  # Save edited JSON
        else:
          file.write(edited_content)  # Save edited text
      st.success(f'File saved successfully as {save_path}!')

