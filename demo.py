import streamlit as st 
import torch as torch
from st_aggrid import AgGrid
import pandas as pd


def introduction():
    st.title("Please input a PDF Folder")
    #st.write("Keep calm and wait for you pdf to be generate")

def input_forms():

    # Streamlit input fields 
    st.sidebar.header("User Input Features")
    #st.sidebar.markdown("Please fill in the following fields to get a prediction of the house price.")
    uploaded_files = st.file_uploader('Upload your files',
    accept_multiple_files=True,type="pdf")

        # Add a submit button
    if st.button("Submit"):
        # Perform some action when the user clicks the submit button
        st.write("You clicked the Submit button!")

    st.write("SUMMARY")
    df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')
    # AgGrid(df)
    container = st.container()
    all = st.checkbox("Select all")

    if all:
        selected_options = container.multiselect("Select one or more options:",
            [value for value in df["airline"]],[value for value in df["airline"]])
    else:
        selected_options =  container.multiselect("Select one or more options:",
        [value for value in df["airline"]])

    # Use boolean indexing to filter the DataFrame based on the selected options
    filtered_df = df[df["airline"].isin(selected_options)]
    AgGrid(filtered_df)
 

        # if submit_button:
        #     # Create a list of inputs
        #     inputs = [total_rooms, population, households, median_income]

        #     # Convert inputs to tensor
        #     inputs = torch.tensor(inputs, dtype=torch.float32)

        #     # Return input tensors
        #     return inputs


# def display_predictions(inputs):
#     # Make predictions
#     predictions = predict(inputs)

#     # Display predictions
#     st.subheader("Predicted house price!")
#     st.write(f"USD ${predictions:.2f}")

# def predict(inputs):
#     # Import local module 
#     from learning_resources.model import RegressionModel

#     # Because we only trained for 4 inputs
#     model = RegressionModel(input_dim=4, output_dim=1)
#     state = torch.load("learning_resources/models/housing_price.pt") 
#     model.load_state_dict(state_dict=state)

#     # Make predictions 
#     predictions = model(inputs)

#     # Get value from tensor
#     predictions = predictions.item() 

#     return predictions * 1000




if __name__ == "__main__":
    introduction() 
    inputs = input_forms()
    

    # if inputs is not None:
    #     display_predictions(inputs)