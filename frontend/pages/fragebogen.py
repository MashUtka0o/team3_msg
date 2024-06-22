import streamlit as st


# Add Personal Information
#
def submit_form():
    answers = {"location": location, "time": time, "desc_of_pain": [desc_of_pain, desc_extra], "event": event}
    output = {"Personal Information": {},
              "Answers": answers}

    print(output)


st.write("Fragebogen Knie")

location = st.radio("Wo sind ihre Schmerzen lokalisiert?",
                    ["Innenseite", "Außenseite", "Weiß ich nicht"])

time = st.radio("Wann haben die Schmerzen begonnen?", [
    "1-3 Tagen", "4-7 Tagen", "bis 2 Wochen", "länger als 2 Wochen"])

desc_of_pain = st.radio("Können Sie die Schmerzen beschreiben?", ["Stechen", "Brennen", "Weiß ich nicht"])

if desc_of_pain == "Stechen":
    desc_extra = st.radio("Haben Sie Symptome wie Taubheit, Schwäche?", ["Ja", "Nein"])
else:
    desc_extra = None

event = st.text_area("Können Sie ein Ereignis beschreiben, nachdem die Schmerzen aufgetreten sind")

st.button(label="Submit", on_click=submit_form)

back = st.button("Back")
if back:
    st.switch_page("./pages/termin.py")

# Every form must have a submit button.
