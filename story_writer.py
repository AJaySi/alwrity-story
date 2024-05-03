import time
import os
import json
import streamlit as st

from ai_story_writer import ai_story_generator


def main():
    set_page_config()
    custom_css()
    hide_elements()
    input_section()

def set_page_config():
    st.set_page_config(
        page_title="Alwrity",
        layout="wide",
    )

def custom_css():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            [class="st-emotion-cache-7ym5gk ef3psqc12"] {
                display: inline-block;
                padding: 5px 20px;
                background-color: #4681f4;
                color: #FBFFFF;
                width: 300px;
                height: 35px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

def hide_elements():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)



def input_section():
    #st.title("🧕 Alwrity - AI Story Writer")
    with st.expander("**PRO-TIP** - Choose your inputs carefully", expanded=True):
        col1, space, col2 = st.columns([5, 0.1, 5])
        with col1:
            personas = [
            ("Award-Winning Science Fiction Author", "Award-Winning Science Fiction Author"),
            ("Historical Fiction Author", "Historical Fiction Author"),
            ("Fantasy World Builder", "Fantasy World Builder"),
            ("Mystery Novelist", "Mystery Novelist"),
            ("Romantic Poet", "Romantic Poet"),
            ("Thriller Writer", "Thriller Writer"),
            ("Children's Book Author", "Children's Book Author"),
            ("Satirical Humorist", "Satirical Humorist"),
            ("Biographical Writer", "Biographical Writer"),
            ("Dystopian Visionary", "Dystopian Visionary"),
            ("Magical Realism Author", "Magical Realism Author")
            ]

            selected_persona_name = st.selectbox(
                "Select Your Story Writing Persona Or Book Genre",
                options=[persona[0] for persona in personas]
            )

            persona_descriptions = {
        "Award-Winning Science Fiction Author": "You are an award-winning science fiction author with a penchant for expansive, intricately woven stories. Your ultimate goal is to write the next award-winning sci-fi novel.",
        "Historical Fiction Author": "You are a seasoned historical fiction author, meticulously researching past eras to weave captivating narratives. Your goal is to transport readers to different times and places through your vivid storytelling.",
        "Fantasy World Builder": "You are a world-building enthusiast, crafting intricate realms filled with magic, mythical creatures, and epic quests. Your ambition is to create the next immersive fantasy saga that captivates readers' imaginations.",
        "Mystery Novelist": "You are a master of suspense and intrigue, intricately plotting out mysteries with unexpected twists and turns. Your aim is to keep readers on the edge of their seats, eagerly turning pages to unravel the truth.",
        "Romantic Poet": "You are a romantic at heart, composing verses that capture the essence of love, longing, and human connections. Your dream is to write the next timeless love story that leaves readers swooning.",
        "Thriller Writer": "You are a thrill-seeker, crafting adrenaline-pumping tales of danger, suspense, and high-stakes action. Your mission is to keep readers hooked from start to finish with heart-pounding thrills and unexpected twists.",
        "Children's Book Author": "You are a storyteller for the young and young at heart, creating whimsical worlds and lovable characters that inspire imagination and wonder. Your goal is to spark joy and curiosity in young readers with enchanting tales.",
        "Satirical Humorist": "You are a keen observer of society, using humor and wit to satirize the absurdities of everyday life. Your aim is to entertain and provoke thought, delivering biting social commentary through clever and humorous storytelling.",
        "Biographical Writer": "You are a chronicler of lives, delving into the stories of real people and events to illuminate the human experience. Your passion is to bring history to life through richly detailed biographies that resonate with readers.",
        "Dystopian Visionary": "You are a visionary writer, exploring dark and dystopian futures that reflect contemporary fears and anxieties. Your vision is to challenge societal norms and provoke reflection on the path humanity is heading.",
        "Magical Realism Author": "You are a purveyor of magical realism, blending the ordinary with the extraordinary to create enchanting and thought-provoking tales. Your goal is to blur the lines between reality and fantasy, leaving readers enchanted and introspective."
            }
            character_input = st.text_area(
                    label=f"Describe your story, its premise, characters and a little on outline etc"
                )

        with col2:
            character_input = st.text_area(
                    label=f"Persona Details for {selected_persona_name}",
                    value=persona_descriptions[selected_persona_name]
                )

        if st.button('AI, Write A Story..'):
            if character_input.strip():
                with st.spinner("Generating Story...💥💥"):
                    story_content = ai_story_generator(selected_persona_name, selected_persona_name, character_input)
                    if story_content:
                        st.subheader('**👩🧕 Your Awesome Story:**')
                        st.markdown(story_content)
                    else:
                        st.error("💥 **Failed to generate Story. Please try again!**")
            else:
                st.error(" Write a long on the story you have in your mind.. !")


if __name__ == "__main__":
    main()

