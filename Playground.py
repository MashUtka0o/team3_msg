import streamlit as st

# Define options with the same displayed values but different internal values
options = [
    {'displayed': 'Option A', 'value': 'value1'},
    {'displayed': 'Option A', 'value': 'value2'},
    {'displayed': 'Option A', 'value': 'value3'}
]

# Display a selectbox with the options
selected_option_index = st.selectbox('Choose an option', range(len(options)),
                                     format_func=lambda i: options[i]['displayed'])

# Get the corresponding value from options based on the selected index
selected_value = options[selected_option_index]['value']

# Display the selected value (different from displayed option)
st.write('You selected:', selected_value)
