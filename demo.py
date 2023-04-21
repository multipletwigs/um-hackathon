import streamlit as st 
import torch

def introduction():
    st.title("House Price Prediction!")
    st.write("This is a demo of a simple house price prediction model built with PyTorch and Streamlit.")

def input_forms():

    # Streamlit input fields 
    st.sidebar.header("User Input Features")
    st.sidebar.markdown("Please fill in the following fields to get a prediction of the house price.")

    # Input fields based on ["total_rooms", "population", "households", "median_income"]

    with st.form(key='housing_form'):
        total_rooms = st.number_input(label="Total Rooms", value=1)
        population = st.number_input(label="Population", value=1)
        households = st.number_input(label="Households", value=1)
        median_income = st.number_input(label="Median Income", value=1)

        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            # Create a list of inputs
            inputs = [total_rooms, population, households, median_income]

            # Convert inputs to tensor
            inputs = torch.tensor(inputs, dtype=torch.float32)

            # Return input tensors
            return inputs


def display_predictions(inputs):
    # Make predictions
    predictions = predict(inputs)

    # Display predictions
    st.subheader("Predicted house price!")
    st.write(f"USD ${predictions:.2f}")

def predict(inputs):
    # Import local module 
    from learning_resources.model import RegressionModel

    # Because we only trained for 4 inputs
    model = RegressionModel(input_dim=4, output_dim=1)
    state = torch.load("learning_resources/models/housing_price.pt") 
    model.load_state_dict(state_dict=state)

    # Make predictions 
    predictions = model(inputs)

    # Get value from tensor
    predictions = predictions.item() 

    return predictions * 1000


if __name__ == "__main__":
    introduction() 
    inputs = input_forms()

    if inputs is not None:
        display_predictions(inputs)