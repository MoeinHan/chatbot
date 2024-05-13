# import streamlit as st
# import numpy as np
# import pandas as pd
# import time
import streamlit as st
import datetime
import sqlite3

import g4f
from g4f.client import Client

conn = sqlite3.connect("data.db")
c = conn.cursor()


def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS chatstable(role TEXT,content TEXT, post_date DATE)")


def add_data(role, content, post_date):
    c.execute('INSERT INTO chatstable(role,content,post_date) VALUES (?,?,?)', (role, content, post_date))
    conn.commit()


def view_all_chats_as_dict():
    c.row_factory = sqlite3.Row
    c.execute("SELECT * FROM chatstable")
    data = c.fetchall()
    unpacked = [{k: item[k] for k in item.keys()} for item in data]
    return unpacked


client = Client()
provider = g4f.Provider.Gemini
model = "stream"

side_bar = st.sidebar
side_bar.header('search for patent')
radio_button = side_bar.radio("what do you want?", ("chatbot", "patent", "research"))
side_bar.write('your choose is: ', radio_button)
st.title("Welcome to AI Chatbot App😎!")
input_user = side_bar.text_input("Enter subject")
button = side_bar.button("ask")
if radio_button == "chatbot":
    st.header("Chatbot App🤖!")
    st.caption("welcome. this chatbot has no limited. ask everything you want😉")

    create_table()
    if "messages" not in st.session_state:
        st.session_state.messages = view_all_chats_as_dict()

    for message in st.session_state.messages:

        with st.chat_message(message.get("role")):
            if str(message.get("role")) == 'user':
                st.markdown(message.get("content"))
                # print(message.get("content"))
            else:
                # print(message.get("content"))
                st.markdown(message.get("content"))

    # sender = st.sidebar.selectbox("User", ["user", "assistant"])

    # prompt = st.chat_input("send a massage")

    prompt = st.chat_input("Send A Message")

    if (button and input_user) or prompt:
        st.session_state.messages.append({"role": 'user', "content": prompt, "post_date": datetime.datetime.now()})

        # Add to persistant storage
        add_data(**{"role": "user", "content": prompt, "post_date": datetime.datetime.now()})

        st.chat_message("user").write(prompt)
        with st.spinner("writing ..."):
            # time.sleep(1)

            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                # ...
                provider=provider
            )
            st.session_state.messages.append({"role": 'assistant', "content": response.choices[0].message.content,
                                              "post_date": datetime.datetime.now()})

            # Add to persistant storage
            add_data(**{"role": 'assistant', "content": response.choices[0].message.content,
                        "post_date": datetime.datetime.now()})

            st.chat_message("assistant").write(response.choices[0].message.content)
            # st.info(response.choices[0].message.content)
            button = False
            prompt = None
        # continue

if radio_button == "patent":
    # prompt = st.chat_input("Enter patent field")

    st.header("finding patent🔬")
    st.caption("here you can find 5 patent about your entered field")

    # subject_patent=st.text_input("enter subject that you want find patents:")
    # st.button("display 5 patent")
    if (button and input_user):
        # if not prompt:
        #     prompt = input_user
        patent = 'recommend 5 patents about ' + str(input_user)
        # st.success(input_user)
        with st.spinner("finding ..."):
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": patent}],
                # ...
                provider=provider
            )
            st.info(response.choices[0].message.content.rjust(100))
            button = False
            input_user = None

if radio_button == "research":
    # prompt = st.chat_input("Enter patent field")

    st.header("finding researches📖")
    st.caption("here you can find 5 research about your entered field")

    # subject_patent = st.text_input("enter subject that you want find researches:")
    # st.button("display 5 research")
    if (button and input_user):
        # st.success(input_user)
        # if not prompt:
        #     prompt = input_user
        researchs = 'recommend 5 articles about ' + str(input_user)

        with st.spinner("finding ..."):
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": researchs}],
                # ...
                provider=provider
            )
            st.info(response.choices[0].message.content.rjust(100))
            button = False
            input_user = None
