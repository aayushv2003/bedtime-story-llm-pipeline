import streamlit as st

from main import (
    create_story_plan,
    generate_story,
    judge_story,
    extract_overall_score,
    revise_story,
    final_safety_check,
    save_output,
)

st.set_page_config(
    page_title="Bedtime Story Generator",
    page_icon="🌙",
    layout="wide"
)

st.title("🌙 Bedtime Story Generator")

st.write(
    "A multi-stage LLM storytelling pipeline for children ages 5–10, "
    "with story planning, LLM judging, revision, and safety validation."
)

default_prompt = """Write a bedtime story for ages 5 to 10 about honesty.
The main character should be a girl named Emma who sees the last cookie that her mom baked for her class party.
Emma secretly eats it, feels guilty, and learns that telling the truth is better than hiding a mistake.
The story should feel warm, calming, emotionally reassuring, and end with a peaceful bedtime moment."""

user_prompt = st.text_area(
    "Enter your bedtime story request:",
    value=default_prompt,
    height=180
)

generate_button = st.button("Generate Story")

if generate_button:

    if not user_prompt.strip():
        st.warning("Please enter a story request.")

    else:
        try:

            with st.spinner("Creating story plan..."):
                story_plan = create_story_plan(user_prompt)

            with st.spinner("Generating story..."):
                initial_story = generate_story(user_prompt, story_plan)

            with st.spinner("Judging story quality..."):
                feedback = judge_story(initial_story)

            score = extract_overall_score(feedback)

            if score < 8:
                with st.spinner(f"Overall score was {score}/10. Improving story..."):
                    final_story = revise_story(initial_story, feedback)
            else:
                final_story = initial_story

            with st.spinner("Running final safety check..."):
                safety_result = final_safety_check(final_story)

            save_output(
                story_plan,
                feedback,
                safety_result,
                final_story
            )

            st.success("Story generated successfully!")

            tab1, tab2, tab3, tab4 = st.tabs(
                [
                    "Final Story",
                    "Story Plan",
                    "Judge Feedback",
                    "Safety Check"
                ]
            )

            with tab1:
                st.subheader("Final Bedtime Story")
                st.write(final_story)

            with tab2:
                st.subheader("Story Plan")
                st.text(story_plan)

            with tab3:
                st.subheader("LLM Judge Feedback")
                st.text(feedback)

            with tab4:
                st.subheader("Final Safety Check")
                st.text(safety_result)

            with open("sample_output.txt", "r", encoding="utf-8") as file:
                output_data = file.read()

            st.download_button(
                label="Download Story Output",
                data=output_data,
                file_name="sample_output.txt",
                mime="text/plain"
            )

        except Exception as error:
            st.error(f"Something went wrong: {error}")