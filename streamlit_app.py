# Handle SQLite for ChromaDB
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except (ImportError, KeyError):
    pass

import streamlit as st
import os
from src.components.sidebar import render_sidebar
from src.components.agents import create_analyst_task,create_market_analyst,run_analyst,create_brand_strategist,create_brand_strategist_task,run_brand_strategist,create_strategy_synthesizer,create_strategy_synthesis_task,run_creative_strategy_synthesis,run_campaign_agent,create_campaign_ideator,create_campaign_task
from src.utils.output_handler import capture_output

#--------------------------------#
#         Streamlit App          #
#--------------------------------#
# Configure the page
st.set_page_config(
    page_title="CrewAI AGENTS BOX",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)
import markdown

def read_markdown_file(filepath):
   """Reads a markdown file and converts it to HTML."""
   try:
       with open(filepath, 'r', encoding='utf-8') as file:
           markdown_text = file.read()
           html_text = markdown.markdown(markdown_text)
           return html_text
   except FileNotFoundError:
       return "Error: File not found."
   except Exception as e:
       return f"Error: {e}"
# Logo
st.logo(
    "https://cdn.prod.website-files.com/66cf2bfc3ed15b02da0ca770/66d07240057721394308addd_Logo%20(1).svg",
    link="https://www.crewai.com/",
    size="large"
)

# Main layout
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🔍 :red[CrewAI] :blue[AGENTS BOX]", anchor=False)
st.info('This is a purely informational message, first press the research button and wait till it gets executed. After this wait for some time before doing the start creative button as it is taking groq key now it can\'t do regular consistent task so give time so rate limit of groq does not exceed', icon="ℹ️")
# Render sidebar and get selection (provider and model)
selection = render_sidebar()

# Check if API keys are set based on provider
if selection["provider"] == "OpenAI":
    if not os.environ.get("OPENAI_API_KEY"):
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar to get started")
        st.stop()
elif selection["provider"] == "GROQ":
    if not os.environ.get("GROQ_API_KEY"):
        st.warning("⚠️ Please enter your GROQ API key in the sidebar to get started")
        st.stop()

# Check EXA key for non-Ollama providers
if selection["provider"] != "Ollama":
    if not os.environ.get("EXA_API_KEY"):
        st.warning("⚠️ Please enter your EXA API key in the sidebar to get started")
        st.stop()

# Add Ollama check
if selection["provider"] == "Ollama" and not selection["model"]:
    st.warning("⚠️ No Ollama models found. Please make sure Ollama is running and you have models loaded.")
    st.stop()

# Create two columns for the input section
input_col1, input_col2, input_col3 = st.columns([1, 3, 1])
with input_col2:
    task_description = st.text_area(
        "What would you like to research?",
        value="m2 chip of apple laptops",
        height=68
    )

col1, col2, col3 = st.columns([1, 0.5, 1])
with col2:
    start_research = st.button("🚀 Start Research", use_container_width=False, type="primary")

if start_research:
    with st.status("🤖 Researching the market trend...", expanded=True) as status:
        try:
            # Create persistent container for process output with fixed height.
            process_container = st.container(height=300, border=True)
            output_container = process_container.container()
            
            # Single output capture context.
            with capture_output(output_container):
                researcher = create_market_analyst(selection)
                task = create_analyst_task(researcher, task_description)
                result = run_analyst(researcher, task)
                status.update(label="✅ Market Trend Research completed!", state="complete", expanded=False)
        except Exception as e:
            status.update(label="❌ Error occurred", state="error")
            st.error(f"An error occurred: {str(e)}")
            st.stop()
    
        # Convert CrewOutput to string for display and download
        analyst_report = str(result)
        
        # Display the final result
        st.markdown(analyst_report)

    
    with st.status("🤖 Researching the brand values...", expanded=True) as status:
        try:
            # Create persistent container for process output with fixed height.
            process_container = st.container(height=300, border=True)
            output_container = process_container.container()
            
            # Single output capture context.
            with capture_output(output_container):
                researcher = create_brand_strategist(selection)
                task = create_brand_strategist_task(researcher, task_description)
                result = run_brand_strategist(researcher, task)
                status.update(label="✅ Brand Research completed!", state="complete", expanded=False)
        except Exception as e:
            status.update(label="❌ Error occurred", state="error")
            st.error(f"An error occurred: {str(e)}")
            st.stop()
        # Convert CrewOutput to string for display and download
        brand_report = str(result)
        
        # Display the final result
        st.markdown(brand_report)
# creativity starts here
with col2:
    start_creativity = st.button("🚀 Start Creative", use_container_width=False, type="primary")

if start_creativity:
    with st.status("🤖 Making a Creative Strategy...", expanded=True) as status:
        try:
            # Create persistent container for process output with fixed height.
            process_container = st.container(height=300, border=True)
            output_container = process_container.container()
            analyst_report=read_markdown_file("output/analysts_report.md")
            brand_report=read_markdown_file("output/brand_report.md")
            # Single output capture context.
            with capture_output(output_container):
                researcher = create_strategy_synthesizer(selection)
                task = create_strategy_synthesis_task(researcher,trend_report=analyst_report,brand_report=brand_report)
                result = run_creative_strategy_synthesis(researcher, task)
                status.update(label="✅ Creative Strategy compiled!", state="complete", expanded=False)
        except Exception as e:
            status.update(label="❌ Error occurred", state="error")
            st.error(f"An error occurred: {str(e)}")
            st.stop()
        # Convert CrewOutput to string for display and download
        strategy = str(result)
        
        # Display the final result
        st.markdown(strategy)
### single campaign idea
with col2:
    make_a_campaign= st.button("🚀 Make a creative campaign idea", use_container_width=False, type="primary")

if make_a_campaign:
    with st.status("🤖 Making a Creative Idea/Program...", expanded=True) as status:
        try:
            # Create persistent container for process output with fixed height.
            process_container = st.container(height=300, border=True)
            output_container = process_container.container()
            creative_shit=read_markdown_file("output/final_creative_strategy.md")
            # Single output capture context.
            with capture_output(output_container):
                researcher = create_campaign_ideator(selection)
                task = create_campaign_task(researcher,task_description)
                result = run_campaign_agent(researcher, task)
                status.update(label="✅ Creative Strategy compiled!", state="complete", expanded=False)
        except Exception as e:
            status.update(label="❌ Error occurred", state="error")
            st.error(f"An error occurred: {str(e)}")
            st.stop()
        # Convert CrewOutput to string for display and download
        strategy = str(result)
        
        # Display the final result
        st.markdown(strategy)
    
# Create download buttons
st.divider()
download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
with download_col2:
    st.markdown("### 📥 Download  Reports")
        
    # Download as Markdown
    st.download_button(
        label="Download final creative strategy Report",
        data=read_markdown_file("output/final_creative_strategy.md"),
        file_name="final_creative_strategy.md",
        mime="text/markdown",
        help="Download the research report in Markdown format"
    )
    st.download_button(
        label="Download Brand Report",
        data=read_markdown_file("output/brand_report.md"),
        file_name="brand_report.md",
        mime="text/markdown",
        help="Download the research report in Markdown format"
    )
    st.download_button(
        label="Download Campaign Strategy Report",
        data=read_markdown_file("output/campaign_strategy_report.md"),
        file_name="campaign_strategy_report.md",
        mime="text/markdown",
        help="Download the research report in Markdown format"
    )

# Add footer
st.divider()
footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])
with footer_col2:
    st.caption("Made with ❤️❤️❤️ and luck....")