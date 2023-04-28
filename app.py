import streamlit as st
from streamlit_chat import message
from memory import get_memory

print('this is app.py')
st.title('How My ZSH')

def get_text():
    input_text = st.text_input("", key="input")
    return input_text

# Initialize the session state for generated responses and past inputs
if 'generated' not in st.session_state:
    st.session_state['generated'] = ['i am ready to help you ser']

if 'past' not in st.session_state:
    st.session_state['past'] = ['hello']


# Get the user's input from the text input field
user_input = get_text()

# add reset or clear button to clear the chat
if st.button('Clear', key='clear'):
    st.session_state['generated'] = []
    st.session_state['past'] = []
    user_input = get_text()

# If there is user input, search for a response using the search_chroma function
if user_input:
    output = get_memory().query(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

# If there are generated responses, display the conversation using Streamlit messages
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])):
        message(st.session_state['past'][i],
                avatar_style="personas",
                is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))
        
