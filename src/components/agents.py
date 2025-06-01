from typing import Type
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from exa_py import Exa
import requests
import streamlit as st
import os

#--------------------------------#
#         EXA Answer Tool        #
#--------------------------------#
class EXAAnswerToolSchema(BaseModel):
    query: str = Field(..., description="The question you want to ask Exa.")

class EXAAnswerTool(BaseTool):
    name: str = "Ask Exa a question"
    description: str = "A tool that asks Exa a question and returns the answer."
    args_schema: Type[BaseModel] = EXAAnswerToolSchema
    answer_url: str = "https://api.exa.ai/answer"

    def _run(self, query: str):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": st.secrets["EXA_API_KEY"]
        }
        
        try:
            response = requests.post(
                self.answer_url,
                json={"query": query, "text": True},
                headers=headers,
            )
            response.raise_for_status() 
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Log the HTTP error
            print(f"Response content: {response.content}")  # Log the response content for more details
            raise
        except Exception as err:
            print(f"Other error occurred: {err}")  # Log any other errors
            raise

        response_data = response.json()
        answer = response_data["answer"]
        citations = response_data.get("citations", [])
        output = f"Answer: {answer}\n\n"
        if citations:
            output += "Citations:\n"
            for citation in citations:
                output += f"- {citation['title']} ({citation['url']})\n"

        return output


#######################################
#             AGENTS                  #
#######################################
#--------------------------------#
#         market analyst Agent   #
#--------------------------------#
def create_market_analyst(selection):
    """Create a market trend analyst which will search for relevant audience needs for the domain and then also spot the market trends right now.
    
    Args:
        selection (dict): Contains provider and model information
            - provider (str): The LLM provider ("OpenAI", "GROQ", or "Ollama")
            - model (str): The model identifier or name
    
    Returns:
        Agent: A configured CrewAI agent ready for research tasks
    
    Note:
        Ollama models have limited function-calling capabilities. When using Ollama,
        the agent will rely more on its base knowledge and may not effectively use
        external tools like web search.
    """
    provider = selection["provider"]
    model = selection["model"]
    
    if provider == "GROQ":
        llm = LLM(
            api_key=st.secrets["GROQ_API_KEY"],
            model=f"groq/{model}"
        )
    elif provider == "Ollama":
        llm = LLM(
            base_url="http://localhost:11434",
            model=f"ollama/{model}",
        )
    else:
        # Map friendly names to concrete model names for OpenAI
        if model == "GPT-3.5":
            model = "gpt-3.5-turbo"
        elif model == "GPT-4":
            model = "gpt-4"
        elif model == "o1":
            model = "o1"
        elif model == "o1-mini":
            model = "o1-mini"
        elif model == "o1-preview":
            model = "o1-preview"
        # If model is custom but empty, fallback
        if not model:
            model = "o1"
        llm = LLM(
            api_key=st.secrets["OPENAI_API_KEY"],
            model=f"openai/{model}"
        )
    
    
    researcher = Agent(
        role='Research Analyst',
        goal='Conduct thorough research on audience needs and market trends for the current year 2025',
        backstory='Expert at finding the audience needs and mindset shifts and can tell the market is trending and will what be liking to go more popular. Good knowledge of market sentiments with 20+ years of experience.',
        tools=[EXAAnswerTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False,  # Disable delegation to avoid caching
    )
    return researcher

#--------------------------------#
#       brand strategist Agent   #
#--------------------------------#
def create_brand_strategist(selection):
    """Create a brand strategist analyst which will be searching for the brand valuse and telling what the brand is actually.
    
    Args:
        selection (dict): Contains provider and model information
            - provider (str): The LLM provider ("OpenAI", "GROQ", or "Ollama")
            - model (str): The model identifier or name
    
    Returns:
        Agent: A configured CrewAI agent ready for finding keeping in touch with the brand values
    
    Note:
        Ollama models have limited function-calling capabilities. When using Ollama,
        the agent will rely more on its base knowledge and may not effectively use
        external tools like web search.
    """
    provider = selection["provider"]
    model = selection["model"]
    
    if provider == "GROQ":
        llm = LLM(
            api_key=st.secrets["GROQ_API_KEY"],
            model=f"groq/{model}"
        )
    elif provider == "Ollama":
        llm = LLM(
            base_url="http://localhost:11434",
            model=f"ollama/{model}",
        )
    else:
        # Map friendly names to concrete model names for OpenAI
        if model == "GPT-3.5":
            model = "gpt-3.5-turbo"
        elif model == "GPT-4":
            model = "gpt-4"
        elif model == "o1":
            model = "o1"
        elif model == "o1-mini":
            model = "o1-mini"
        elif model == "o1-preview":
            model = "o1-preview"
        # If model is custom but empty, fallback
        if not model:
            model = "o1"
        llm = LLM(
            api_key=st.secrets["OPENAI_API_KEY"],
            model=f"openai/{model}"
        )
    
    
    researcher = Agent(
        role='Brand Strategist',
        goal='Conduct thorough research on the brand value remaining in the current year 2025',
        backstory='Expert at finding the brand value attained/ remained at present time in the market. Good knowledge of market sentiments with 20+ years of experience.',
        tools=[EXAAnswerTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False,  # Disable delegation to avoid caching
    )
    return researcher

#--------------------------------#
#   strategy synthesizer Agent   #
#--------------------------------#
def create_strategy_synthesizer(selection):
    """Create a creative strategy synthesizer that uses both the the market trend research and the brand values research done and then gives a perfect strategy builder.
    
    Args:
        selection (dict): Contains provider and model information
            - provider (str): The LLM provider ("OpenAI", "GROQ", or "Ollama")
            - model (str): The model identifier or name
    
    Returns:
        Agent: A configured CrewAI agent ready for building a creative campaign strategies.
    
    Note:
        Ollama models have limited function-calling capabilities. When using Ollama,
        the agent will rely more on its base knowledge and may not effectively use
        external tools like web search.
    """
    provider = selection["provider"]
    model = selection["model"]
    
    if provider == "GROQ":
        llm = LLM(
            api_key=st.secrets["GROQ_API_KEY"],
            model=f"groq/{model}"
        )
    elif provider == "Ollama":
        llm = LLM(
            base_url="http://localhost:11434",
            model=f"ollama/{model}",
        )
    else:
        # Map friendly names to concrete model names for OpenAI
        if model == "GPT-3.5":
            model = "gpt-3.5-turbo"
        elif model == "GPT-4":
            model = "gpt-4"
        elif model == "o1":
            model = "o1"
        elif model == "o1-mini":
            model = "o1-mini"
        elif model == "o1-preview":
            model = "o1-preview"
        # If model is custom but empty, fallback
        if not model:
            model = "o1"
        llm = LLM(
            api_key=st.secrets["OPENAI_API_KEY"],
            model=f"openai/{model}"
        )
    strategy_synth = Agent(
        role="Creative Strategy Synthesizer",
        goal="Combine brand insights and market trends to deliver a unified creative strategy.",
        backstory="Expert in turning data, research, and brand values into coherent strategic directions that resonate with target audiences and drive results.",
        tools=[EXAAnswerTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
    return strategy_synth

#--------------------------------#
#    campaign ideator Agent      #
#--------------------------------#
def create_campaign_ideator(selection):
    """Create a Creative Campaign Ideator Agent that uses the previous done work on creative campaign report and build a one good campaign.
    
    Args:
        selection (dict): Contains provider and model information
            - provider (str): The LLM provider ("OpenAI", "GROQ", or "Ollama")
            - model (str): The model identifier or name
    
    Returns:
        Agent: A configured CrewAI agent ready for building a single creative campaign .
    
    Note:
        Ollama models have limited function-calling capabilities. When using Ollama,
        the agent will rely more on its base knowledge and may not effectively use
        external tools like web search.
    """
    provider = selection["provider"]
    model = selection["model"]

    if provider == "GROQ":
        llm = LLM(
            api_key=st.secrets["GROQ_API_KEY"],
            model=f"groq/{model}"
        )
    elif provider == "Ollama":
        llm = LLM(
            base_url="http://localhost:11434",
            model=f"ollama/{model}"
        )
    else:
        if model in ["GPT-3.5", "GPT-4", "o1", "o1-mini", "o1-preview"]:
            model = model.lower().replace("-", "_")
        if not model:
            model = "o1"
        llm = LLM(
            api_key=st.secrets["OPENAI_API_KEY"],
            model=f"openai/{model}"
        )

    return Agent(
        role="Creative Campaign Architect",
        goal="Design an original, scalable, and culturally relevant campaign idea that stands out",
        backstory=(
            "An imaginative, strategic campaign thinker who merges creativity with structure. "
            "Skilled in outlining end-to-end campaign plans, visuals, channels, and growth trajectories."
        ),
        tools=[EXAAnswerTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

#######################################
#             TASKS                   #
#######################################
#--------------------------------#
#         analyst Task          #
#--------------------------------#
def create_analyst_task(analyst, task_description):
    """Create a market analysis task for the agent to execute.
    
    Args:
        analyst (Agent): The market analyst agent that will perform the task
        task_description (str): The topic/product which needs to be think of
    
    Returns:
        Task: A configured CrewAI task with expected output format
    """
    return Task(
        description=task_description,
        expected_output = """
        A detailed market trend analysis report for the year 2025, focused on the specified product or company. 
        The report should uncover key market shifts, consumer behavior changes, competitive positioning, 
        and emerging opportunities or risks relevant to the subject.

        Use clean markdown formatting (no backticks or code blocks) and organize the output as follows:

        # Market Overview
        - Brief description of the product or company
        - Market category and segmentation
        - Key players and positioning
        - Total Addressable Market (TAM) if applicable

        # Emerging Trends (2025)
        - Notable shifts in consumer behavior or preferences
        - Regulatory or environmental changes affecting the space
        - Technological advancements or disruptions
        - Socioeconomic and cultural factors influencing the market

        # Competitive Landscape
        - Key competitors and their strategies
        - Product differentiators and positioning
        - SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis of the target product/company
        - Innovation benchmarks

        # Consumer Insight
        - Target audience demographics and psychographics
        - Pain points, aspirations, and buying behavior
        - Current brand perception and user sentiment

        # Opportunities & Threats
        - Market gaps and untapped potential
        - Risks from new entrants, alternatives, or changing demand
        - Strategic white spaces or growth angles

        # Recommendations
        - Short-term and long-term strategic actions
        - Go-to-market suggestions
        - Innovation or differentiation paths
        - Watch areas for ongoing monitoring

        # Citations
        - List all sources with titles and URLs
        - Include publication dates where available
        - Format as: "[Title] (URL) - [Date]"

        Note: The insights should be based on current trends and reliable data. All claims should be well-supported, and findings should be actionable for strategic planning.
        """,
        agent=analyst,
        output_file="output/analysts_report.md"
    )

#--------------------------------#
#      brand strategist Task     #
#--------------------------------#
def create_brand_strategist_task(analyst, task_description):
    """Create a brand strategist task for the agent to execute.
    
    Args:
        brand strategist (Agent): The brand strategist agent that will perform the task
        task_description (str): The topic/product which needs to be think of
    
    Returns:
        Task: A configured CrewAI task with expected output format
    """
    return Task(
        description=task_description,
        expected_output = """
            A brand alignment and positioning report for the year 2025, focused on the specified product or company. 
            This report should evaluate how well the current brand strategy aligns with target audiences, market context, 
            and business goals. It should provide actionable recommendations for improving brand clarity, consistency, 
            and impact.

            Use clean markdown formatting (no code blocks or backticks) and structure the output as follows:

            # Brand Overview
            - Brief summary of the brand's mission, vision, and core values
            - Description of current brand positioning
            - Brand tone of voice and personality traits
            - Visual identity or symbolic elements (if applicable)

            # Audience-Brand Fit
            - Target audience demographics and psychographics
            - Emotional and functional benefits the brand delivers
            - Assessment of brand relevance to audience needs and aspirations
            - Gaps or mismatches in communication or perception

            # Competitive Brand Analysis
            - Key competitor brand personalities and messages
            - Differentiation opportunities
            - Brand sentiment benchmarks
            - Strengths and weaknesses in current positioning

            # Brand Messaging Assessment
            - Review of tagline/slogan, key messages, and value propositions
            - Language style, tone, and consistency across touchpoints
            - Alignment with audience expectations and cultural tone in 2025

            # Strategic Opportunities
            - Emerging positioning strategies in the market
            - Ways to strengthen emotional or cultural connection
            - Opportunities to evolve tone, narrative, or experience
            - Messaging angles that resonate with 2025 mindsets

            # Recommendations
            - Actions to reinforce brand clarity and consistency
            - Suggested tone and messaging adjustments
            - Cross-channel alignment suggestions
            - Long-term brand evolution strategies

            # Citations
            - List all data sources, articles, frameworks, or references
            - Include titles, URLs, and publication dates
            - Format: "[Title] (URL) - [Date]"

            Note: Ensure that recommendations are grounded in current market dynamics and reflect cultural sensitivities of 2025. Use industry best practices where applicable, and support insights with real examples.
            """,
        agent=analyst,
        output_file="output/brand_report.md"
    )

#--------------------------------#
#   stategy synthesizer Task     #
#--------------------------------#
def create_strategy_synthesis_task(agent, trend_report, brand_report):
    """Create a Strategy Synthesizer task for the agent to execute.
    
    Args:
        Strategy Synthesizer(Agent): The Strategy Synthesizer agent that will perform the task
        trend_report: the report of the trend made
        brand_report: made by the brand strategist agent 
    
    Returns:
        Task: A configured CrewAI task with expected output format
    """
    return Task(
        description=f"""
        Use the following two documents to synthesize a compelling and strategically sound creative direction:

        1. Market Trends Report:
        {trend_report}

        2. Brand Strategy Report:
        {brand_report}

        Your job is to unify the insights from both and produce a final strategic creative recommendation 
        for a campaign, product positioning, or content strategy in 2025.

        Focus on integrating audience expectations, market opportunities, and brand voice to make a persuasive 
        and actionable creative strategy.

        Make it decision-ready for stakeholders.
        """,
        expected_output="""
        # Creative Strategy Document (2025)

        ## Executive Summary
        - Core idea of the campaign or strategic recommendation
        - High-level integration of market and brand insights

        ## Strategic Rationale
        - Why this direction fits the audience now
        - What trends it's aligned with
        - How it reflects the brand identity and tone

        ## Campaign/Concept Overview
        - Key message and storytelling arc
        - Channels and platforms
        - Content formats and ideas
        - Visual/tonal direction suggestions

        ## Strategic Advantages
        - Competitive differentiation
        - Brand alignment
        - Timing relevance

        ## Recommendations
        - Execution tips and risk mitigation
        - KPIs to track success
        - Suggestions for testing or scaling

        ## Appendices
        - Reference summaries of input reports
        """,
        agent=agent,
        output_file="output/final_creative_strategy.md"
    )

#--------------------------------#
#     Campaign Ideator Task      # 
#--------------------------------#
def create_campaign_task(agent, brief_or_topic):
    """Create a single creative campaign strategy task.
    Args:
        campaign ideator(Agent): The campaign ideator agent that will perform the task
        trend_report: the report of the trend made
        brand_report: made by the brand strategist agent 
    
    Returns:
        Task: A configured CrewAI task with expected output format
    """
    return Task(
        description=f"Develop a creative marketing campaign for: {brief_or_topic}",
        expected_output="""
        A comprehensive creative campaign proposal for 2025, built around the provided theme or product.

        # Campaign Idea
        - Campaign title and concept
        - One-liner pitch or tagline
        - Big idea explanation
        - Emotional and cultural insight leveraged

        # Campaign Plan
        - Key objectives (awareness, engagement, conversion, etc.)
        - Target audience
        - Phased rollout plan (launch, sustain, scale)
        - Key messages per stage

        # Channel Strategy
        - Platforms to be used (e.g., social, outdoor, PR, influencer, events)
        - Content types and format examples
        - Timing and cadence

        # Growth & Virality
        - How the idea can scale organically
        - Built-in shareability
        - Potential collaborations or stunts
        - Metrics to track success

        # Visual Concept (for image generation)
        - Describe a hero visual representing the campaign (what it would look like)
        - Specify style (e.g., surreal, minimalist, high-contrast)
        - Mood and tone
        - Add environment, people, props, emotion if relevant

        # Image Prompt
        Provide a concise visual prompt ready for an AI image generation tool. Keep it clear, vivid, and under 60 words.

        # Final Notes
        - Any additional creative ideas
        - Brand alignment checks
        - Cultural or ethical considerations

        """,
        agent=agent,
        output_file="output/campaign_strategy_report.md"
    )

#######################################
#              CREW                   #
#######################################
#--------------------------------#
#         analyst Crew           #
#--------------------------------#
def run_analyst(analyst, task):
    """Execute the market trend analyst task using the configured agent.
    
    Args:
        market analyst (Agent): The analyst agent to perform the task
        task (Task): The analyst task to execute
    
    Returns:
        str: The research results in markdown format
    """
    crew = Crew(
        agents=[analyst],
        tasks=[task],
        verbose=True,
        process=Process.sequential
    )
    
    return crew.kickoff()

#--------------------------------#
#    brand strategist Crew       #
#--------------------------------#

def run_brand_strategist(analyst, task):
    """Execute the brand strategist task using the configured agent.
    
    Args:
        brand strategist (Agent): The analyst agent to perform the task
        task (Task): The analyst task to execute
    
    Returns:
        str: The research results in markdown format
    """
    crew = Crew(
        agents=[analyst],
        tasks=[task],
        verbose=True,
        process=Process.sequential
    )
    
    return crew.kickoff()

#--------------------------------#
#  strategy synthesizer Crew     #
#--------------------------------#
def run_creative_strategy_synthesis(synthesizer,task):
    """Execute the Strategy synthesizer task using the configured agent.
    
    Args:
        Strategy synthesizer (Agent): The analyst agent to perform the task
        task (Task): The analyst task to execute
    
    Returns:
        str: The research results in markdown format
    """
    
    crew = Crew(
        agents=[synthesizer],
        tasks=[task],
        verbose=True,
        process=Process.sequential
    )
    return crew.kickoff()
#--------------------------------#
#    Campaign ideator Crew       #
#--------------------------------#
def run_campaign_agent(agent, task):
    """Execute the campaign ideator task using the configured agent.
    
    Args:
        campaign ideator (Agent): The analyst agent to perform the task
        task (Task): The analyst task to execute
    
    Returns:
        str: The research results in markdown format
    """
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True,
        process=Process.sequential
    )
    return crew.kickoff()
