import streamlit as st
import csv
import pandas as pd

# Function to save user signup data to a CSV file
def save_signup_data(name, email, slot):
    with open('signup_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, email, slot])

# Function to display the signup form and handle user input
def signup_form(available_slots):
    st.write("# Event Signup Form")
    slot_options = [slot for slot, available_spots in available_slots.items() if available_spots > 0]
    selected_slot = st.selectbox("Select a slot", slot_options)
    name = st.text_input("Name")
    email = st.text_input("Email")

    # Add validation for required fields
    if st.button("Sign Up"):
        if not name or not email:  # Check if name or email is empty
            st.error("Name and email are required fields.")
        else:
            if available_slots[selected_slot] > 0:
                save_signup_data(name, email, selected_slot)
                st.success(f"Thank you, {name}! You have successfully signed up for slot {selected_slot}.")
                available_slots = get_available_slots()  # Update available slots after sign-up
            else:
                st.error(f"Sorry, slot {selected_slot} is full. Please choose another slot.")

# Function to display the number of available spots for each slot
def display_available_spots(available_slots):
    st.write("## Available Spots")
    for slot, available_spots in available_slots.items():
        if available_spots > 0:
            st.write(f"- Slot {slot}: {available_spots} spots available")

def get_available_slots():
    # Read initial available slots from CSV
    df_available_slots = pd.read_csv('available_slots.csv')
    #print(df_available_slots)

    # Read sign-up data from CSV
    df_taken_slots = pd.read_csv('signup_data.csv')
    df_taken_slots = df_taken_slots['slots'].value_counts().to_frame().reset_index()
    df_taken_slots = df_taken_slots.rename(columns={'count': 'count_taken_slots'})

    # Merge taken slots with initial available slots
    #df_available_slots = pd.merge(df_available_slots, df_taken_slots, on='index', how='left').fillna(0)
    new_values_take_slots = df_taken_slots['count_taken_slots'].to_list()
    df_available_slots['count_taken_slots'] = new_values_take_slots

    # Calculate available spots
    df_available_slots['count_available_slots'] = df_available_slots['count_initial_available_slots'] - df_available_slots['count_taken_slots']
    available_slots = df_available_slots.set_index('slots')['count_available_slots'].to_dict()

    return available_slots

# Main function to run the Streamlit app
def main():
    available_slots = get_available_slots()
    display_available_spots(available_slots)
    signup_form(available_slots)

if __name__ == "__main__":
    main()
