#####################################################
#
# google-gemini-cookbook - Story_Writing_with_Prompt_Chaining
#
#####################################################

import os
from pathlib import Path
from google.api_core import retry
import google.generativeai as genai
import streamlit as st


def generate_with_retry(model, prompt):
    """
    Generates content from the model with retry handling for errors.

    Parameters:
        model (GenerativeModel): The generative model to use for content generation.
        prompt (str): The prompt to generate content from.

    Returns:
        str: The generated content.
    """
    try:
        # FIXME: Need a progress bar here.
        return model.generate_content(prompt, request_options={'retry':retry.Retry()})
    except Exception as e:
        print(f"Error generating content: {e}")
        return ""


def ai_story_generator(persona, story_setting, character_input, 
                       plot_elements, writing_style, story_tone, narrative_pov,
                       audience_age_group, content_rating, ending_preference, api_key=None, page_length=3, output_language="English"):
    """
    Write a story using prompt chaining and iterative generation.

    Parameters:
        persona (str): The persona statement for the author.
        story_genre (str): The genre of the story.
        characters (str): The characters in the story.
        page_length (int): The target length of the story in pages.
    """
    st.info(f"""
        You have chosen to create a story set in **{story_setting}**. 
        The main characters are: **{character_input}**.
        The plot will revolve around the theme of **{plot_elements}**.
        The story will be written in a **{writing_style}** style with a **{story_tone}** tone, from a **{narrative_pov}** perspective. 
        It is intended for a **{audience_age_group}** audience with a **{content_rating}** rating. 
        You prefer the story to have a **{ending_preference}** ending.
        """)
    try:
        persona = f"""{persona}
            Write a story with the following details:

        **The stroy Setting is:**
        {story_setting}
        
        **The Characters of the story are:**
        {character_input}
        
        **Plot Elements of the story:**
        {plot_elements}
        
        **Story Writing Style:**
        {writing_style}
        
        **The story Tone is:**
        {story_tone}
        
        **Write story from the Point of View of:**
        {narrative_pov}
        
        **Target Audience of the story:**
        {audience_age_group}, **Content Rating:** {content_rating}
        
        **Story Ending:**
        {ending_preference}
        
        Make sure the story is engaging and tailored to the specified audience and content rating. 
        Ensure the ending aligns with the preference indicated.
        
        IMPORTANT: Write the story in {output_language} language.
        """
        # Define persona and writing guidelines
        # Calculate target word count (1 page ≈ 300 words)
        target_words = page_length * 300
        # Initial draft always targets at least 2000 words for a rich start
        initial_words = 2000
        # Update guidelines to reflect target length
        guidelines = f'''
        Writing Guidelines:
        Delve deeper. Lose yourself in the world you're building. Unleash vivid
        descriptions to paint the scenes in your reader's mind.
        Develop your characters — let their motivations, fears, and complexities unfold naturally.
        Weave in the threads of your outline, but don't feel constrained by it.
        Allow your story to surprise you as you write. Use rich imagery, sensory details, and
        evocative language to bring the setting, characters, and events to life.
        Introduce elements subtly that can blossom into complex subplots, relationships,
        or worldbuilding details later in the story.
        Keep things intriguing but not fully resolved.
        Avoid boxing the story into a corner too early.
        Plant the seeds of subplots or potential character arc shifts that can be expanded later.
        Remember, your main goal is to write as much as you can. If you get through
        the story too fast, that is bad. Expand, never summarize.
        Aim for a story of at least {target_words} words (about {page_length} pages).'''

        # Generate prompts
        premise_prompt = f'''\

        {persona}

        Write a single sentence premise for a {story_setting} story featuring {character_input}.
        '''

        outline_prompt = f'''\

        {persona}

        You have a gripping premise in mind:

        {{premise}}

        Write an outline for the plot of your story.
        '''

        starting_prompt = f'''

        {persona}

        You have a gripping premise in mind:

        {{premise}}

        Your imagination has crafted a rich narrative outline:

        {{outline}}

        First, silently review the outline and the premise. Consider how to start the
        story.

        Start to write the very beginning of the story. You are not expected to finish
        the whole story now. Your writing should be detailed enough that you are only
        scratching the surface of the first bullet of your outline. Try to write AT MINIMUM {initial_words} WORDS.

        {guidelines}
        '''

        continuation_prompt = f'''\

        {persona}

        You have a gripping premise in mind:

        {{premise}}

        Your imagination has crafted a rich narrative outline:

        {{outline}}

        You've begun to immerse yourself in this world, and the words are flowing.
        Here's what you've written so far:

        {{story_text}}

        =====

        First, silently review the outline and story so far. Identify what the single
        next part of your outline you should write.

        Your task is to continue where you left off and write the next part of the story.
        You are not expected to finish the whole story now. Your writing should be
        detailed enough that you are only scratching the surface of the next part of
        your outline. Try to write AT MINIMUM 1000 WORDS. However, only once the story
        is COMPLETELY finished, write IAMDONE. Remember, do NOT write a whole chapter
        right now.

        {guidelines}
        '''
        
        # Use user-provided API key if available
        if api_key:
            genai.configure(api_key=api_key)
        else:
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        # Initialize the generative model with Gemini 2.0 Flash
        model = genai.GenerativeModel('gemini-2.0-flash')

        # Generate prompts
        try:
            premise_result = generate_with_retry(model, premise_prompt)
            premise = premise_result.text if hasattr(premise_result, 'text') else str(premise_result)
            st.info(f"The premise of the story is: {premise}")
        except Exception as err:
            st.error(f"Premise Generation Error: {err}")
            return

        outline_result = generate_with_retry(model, outline_prompt.format(premise=premise))
        outline = outline_result.text if hasattr(outline_result, 'text') else str(outline_result)
        with st.expander("🧙‍♂️ Click to Checkout the outline, writing still in progress..", expanded=True):
            st.markdown(f"The Outline of the story is: {outline}\n\n")
        
        if not outline:
            st.error("Failed to generate outline. Exiting...")
            return

        # Generate starting draft
        with st.status("🦸Story Writing in Progress..", expanded=True) as status:
            try:
                starting_draft_result = generate_with_retry(model, 
                    starting_prompt.format(premise=premise, outline=outline))
                starting_draft = starting_draft_result.text if hasattr(starting_draft_result, 'text') else str(starting_draft_result)
                status.update(label=f"🪂 Current draft length: {len(starting_draft)} characters")
            except Exception as err:
                st.error(f"Failed to Generate Story draft: {err}")
                return False

            try:
                draft = starting_draft
                continuation_result = generate_with_retry(model, 
                    continuation_prompt.format(premise=premise, outline=outline, story_text=draft))
                continuation = continuation_result.text if hasattr(continuation_result, 'text') else str(continuation_result)
                status.update(label=f"🏄 Current draft length: {len(continuation)} characters")
            except Exception as err:
                st.error(f"Failed to write the initial draft: {err}")

            # Add the continuation to the initial draft, keep building the story until we see 'IAMDONE'
            import re
            def word_count(text):
                return len(re.findall(r'\w+', text))
            try:
                draft += '\n\n' + continuation
                status.update(label=f"Current draft length: {len(draft)} characters")
            except Exception as err:
                st.error(f"Failed as: {err} and {continuation}")
            
            # Strict chunked generation: one page at a time
            while 'IAMDONE' not in continuation and word_count(draft) < target_words:
                # Calculate remaining words needed
                remaining_words = target_words - word_count(draft)
                # If less than 300 words left, instruct LLM to write only the remaining words
                chunk_words = min(300, remaining_words)
                # Modify the continuation prompt to request exactly chunk_words
                chunked_prompt = continuation_prompt + f"\nWrite no more than {chunk_words} words in this section. Stop if you reach the target length."
                try:
                    status.update(label=f"⏳ Writing in progress... Current draft length: {len(draft)} characters")
                    continuation_result = generate_with_retry(model, 
                        chunked_prompt.format(premise=premise, outline=outline, story_text=draft))
                    continuation = continuation_result.text if hasattr(continuation_result, 'text') else str(continuation_result)
                    draft += '\n\n' + continuation
                except Exception as err:
                    st.error(f"Failed to continually write the story: {err}")
                    return
            status.update(label=f"✔️  Story Completed ✔️ ... Scroll Down for the story.")

        # Remove 'IAMDONE' and print the final story
        final = draft.replace('IAMDONE', '').strip()
        # Trim to exact word count
        words = final.split()
        if len(words) > target_words:
            final = ' '.join(words[:target_words])
        return(final)

    except Exception as e:
        st.error(f"Main Story writing: An error occurred: {e}")
