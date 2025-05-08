import time
import os
import json
import streamlit as st

from ai_story_writer import ai_story_generator


def main():
    set_page_config()
    custom_css()
    hide_elements()
    title_and_description()
    how_to_use_section()
    advanced_settings()
    input_section()
    help_faq_section()
    st.markdown('<div class="footer">Made with ❤️ by ALwrity | <a href="https://github.com/AJaySi/AI-Writer" style="color:#1976D2;">Support</a></div>', unsafe_allow_html=True)

def set_page_config():
    st.set_page_config(
        page_title="Alwrity",
        layout="wide",
    )

def custom_css():
    st.markdown(f"""
        <style>
        html, body, [class*="css"]  {{
            font-size: 16px;
            background: #fff !important;
            color: #111 !important;
        }}
        @media (max-width: 600px) {{
            html, body, [class*="css"]  {{
                font-size: 14px !important;
            }}
            .stButton > button, .stTextInput > div > input {{
                font-size: 13px !important;
            }}
        }}
        .streamlit-expanderHeader {{color: #fff !important; background: #111 !important; border-radius: 8px;}}
        .streamlit-expanderContent {{background: #111 !important;}}
        div.stButton > button:first-child {{
            background: #1565C0 !important;
            color: white !important;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 2px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }}
        .stAlert, .stError, .stWarning {{ color: #fff !important; background: #b71c1c !important; }}
        .footer {{text-align:center; margin-top:2rem; color:#1976D2; font-size:15px;}}
        </style>
    """, unsafe_allow_html=True)

def hide_elements():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

def title_and_description():
    st.title("🧕 Alwrity - AI Story Writer")
    st.markdown("This app helps you create creative stories with AI. Just fill in your ideas and let Alwrity do the magic! 🧠✨")

def how_to_use_section():
    with st.expander('How to Use', expanded=False):
        st.markdown('''<div style="background:#111;padding:1rem;border-radius:10px;margin-bottom:1.5rem;">
        <ol style="color:#fff;margin-left:1.2em;">
          <li>Select your story persona or genre.</li>
          <li>Describe your story setting, characters, and plot details.</li>
          <li>Choose tone, style, audience, and story length.</li>
          <li>Click <b>AI, Write a Story..</b> to generate your story.</li>
          <li>Read, enjoy, and copy your story!</li>
        </ol>
        </div>''', unsafe_allow_html=True)

def advanced_settings():
    with st.expander("Advanced Settings ⚙️", expanded=False):
        st.markdown('''If you have your own Gemini AI Key, you can enter it below. <a href="https://aistudio.google.com/app/apikey" target="_blank">Get Gemini API Key</a>''', unsafe_allow_html=True)
        user_api_key = st.text_input("Gemini AI Key (optional)", type="password", help="Paste your Gemini API Key here if you have one. Otherwise, the tool will use the default key if available.")
        if user_api_key:
            st.session_state["user_api_key"] = user_api_key

def help_faq_section():
    with st.expander('❓ Need Help?', expanded=False):
        st.markdown('''
        - <b>What does this tool do?</b> It helps you write creative stories with AI, based on your ideas and preferences.<br>
        - <b>Do I need an AI Key?</b> No, you can use the tool without one. Only add your key if you have issues or want to use your own quota.<br>
        - <b>Why do I see errors?</b> Make sure you filled all required fields. If you see API errors, try adding your own Gemini AI Key.<br>
        - <b>Still stuck?</b> <a href="https://github.com/AJaySi/AI-Writer" target="_blank">See our support & documentation</a>
        ''', unsafe_allow_html=True)

def input_section():
    personas = [
        ("Award-Winning Science Fiction Author", "👽 Award-Winning Science Fiction Author"),
        ("Historical Fiction Author", "🏺 Historical Fiction Author"),
        ("Fantasy World Builder", "🧙 Fantasy World Builder"),
        ("Mystery Novelist", "🕵️ Mystery Novelist"),
        ("Romantic Poet", "💌 Romantic Poet"),
        ("Thriller Writer", "🔪 Thriller Writer"),
        ("Children's Book Author", "📚 Children's Book Author"),
        ("Satirical Humorist", "😂 Satirical Humorist"),
        ("Biographical Writer", "📜 Biographical Writer"),
        ("Dystopian Visionary", "🌆 Dystopian Visionary"),
        ("Magical Realism Author", "🪄 Magical Realism Author")
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

    # Story Setting
    st.subheader("🌍 Story Setting")
    story_setting = st.text_area(
        label="**Story Setting** (e.g., medieval kingdom in the past, futuristic city in the future, haunted house in the present):",
        placeholder="""Enter settings for your story, like Location (e.g., medieval kingdom, futuristic city, haunted house),
        Time period in which your story is set (e.g: Past, Present, Future)
        Example: 'A bustling futuristic city with towering skyscrapers and flying cars, set in the year 2150. 
        The city is known for its technological advancements but has a dark underbelly of crime and corruption.'""",
        help="Describe the main location and time period where the story will unfold in a detailed manner."
    )
    
    # Main Characters
    st.subheader("👥 Main Characters")
    character_input = st.text_area(
        label="**Character Information** (Names, Descriptions, Roles)",
        placeholder="""Example:
        Character Names: John, Xishan, Amol
        Character Descriptions: John is a tall, muscular man with a kind heart. Xishan is a clever and resourceful woman. Amol is a mischievous and energetic young boy.
        Character Roles: John - Hero, Xishan - Sidekick, Amol - Supporting Character""",
        help="Enter character information as specified in the placeholder."
    )
    
    # Plot Elements
    st.subheader("🗺️ Plot Elements")
    plot_elements = st.text_area(
        "**Plot Elements** - (Theme, Key Events & Main Conflict)",
        placeholder="""Example:
        Story Theme: Love conquers all, The hero's journey, Good vs. evil.
        Key Events: The hero meets the villain, The hero faces a challenge, The hero overcomes the conflict.
        Main Conflict: The hero must save the world from a powerful enemy, The hero must overcome a personal obstacle to achieve their goal.""",
        help="Enter plot elements as specified in the placeholder."
    )
    
    # Tone and Style
    st.subheader("🎨 Tone and Style")
    col1, col2, col3 = st.columns(3)
    with col1:
        writing_style = st.selectbox(
            "**Writing Style:**",
            ["🧐 Formal", "😎 Casual", "🎼 Poetic", "😂 Humorous"],
            help="Choose the writing style that fits your story."
        )
    with col2:
        story_tone = st.selectbox(
            "**Story Tone:**",
            ["🌑 Dark", "☀️ Uplifting", "⏳ Suspenseful", "🎈 Whimsical"],
            help="Select the overall tone or mood of the story."
        )
    with col3:
        narrative_pov = st.selectbox(
            "**Narrative Point of View:**",
            ["👤 First Person", "👥 Third Person Limited", "👁️ Third Person Omniscient"],
            help="Choose the point of view from which the story is told."
        )
    
    # Target Audience
    st.subheader("👨‍👩‍👧‍👦 Target Audience")
    col1, col2, col3 = st.columns(3)
    with col1:
        audience_age_group = st.selectbox(
            "**Audience Age Group:**",
            ["🧒 Children", "👨‍🎓 Young Adults", "🧑‍🦳 Adults"],
            help="Choose the intended audience age group."
        )
    with col2:
        content_rating = st.selectbox(
            "**Content Rating:**",
            ["🟢 G", "🟡 PG", "🔵 PG-13", "🔴 R"],
            help="Select a content rating for appropriateness."
        )
    with col3:
        ending_preference = st.selectbox(
            "Story Conclusion:",
            ["😊 Happy", "😢 Tragic", "❓ Cliffhanger", "🔀 Twist"],
            help="Choose the type of ending you prefer for the story."
        )

    # Page Length Option
    st.subheader("📄 Story Length")
    page_length = st.slider(
        "Select the number of pages for your story:",
        min_value=1, max_value=100, value=3, help="1 page ≈ 300 words. For very large stories, consider using your own API key."
    )
    # Restrict default API key to 10 pages
    api_key = st.session_state.get("user_api_key", None)
    if not api_key and page_length > 10:
        st.warning("To generate more than 10 pages, you must provide your own Gemini API key in Advanced Settings.")
    if page_length > 20:
        st.warning("You have selected a very large story. This may use a lot of API quota and take a long time. For best results, use your own Gemini API key in Advanced Settings.")

    # Language selection in main UI
    st.subheader("🌐 Output Language")
    language_options = ["English", "Hindi", "Spanish", "French", "German", "Chinese", "Japanese", "Other"]
    output_language = st.selectbox(
        "Select Output Language:",
        language_options,
        help="Choose the language in which you want your story to be generated."
    )
    if output_language == "Other":
        custom_language = st.text_input(
            "Enter your desired language:",
            placeholder="Type your language (e.g., Italian, Russian, Arabic, etc.)",
            help="Type the language you want if it's not in the list."
        )
        if custom_language.strip():
            output_language = custom_language.strip()
    st.session_state["output_language"] = output_language

    if st.button('AI, Write a Story..'):
        if character_input.strip():
            if not api_key and page_length > 10:
                st.error("You must provide your own Gemini API key in Advanced Settings to generate more than 10 pages.")
                return
            with st.spinner("Generating Story...💥💥"):
                story_content = ai_story_generator(persona_descriptions[selected_persona_name],
                        story_setting, character_input, plot_elements, writing_style,
                        story_tone, narrative_pov, audience_age_group, content_rating,
                        ending_preference, api_key=api_key, page_length=page_length, output_language=output_language)
                if story_content:
                    st.subheader('**🧕 Your Awesome Story:**')
                    st.markdown(story_content)
                else:
                    st.error("💥 **Failed to generate Story. Please try again!**")
        else:
            st.error("Describe the story you have in your mind.. !")


if __name__ == "__main__":
    main()
