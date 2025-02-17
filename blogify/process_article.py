from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def summarize_article(text: str) -> str:
    """
    Summarize an article using OpenAI's GPT-4 model with a short, concise summary.
    
    Args:
        text (str): The article text to summarize
        
    Returns:
        str: A few-sentence summary of the article, or an error message if summarization fails.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the following article in a few sentences:\n\n{text}"
                }
            ],
            max_tokens=150,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error summarizing article: {str(e)}")
        return "Summary unavailable"

def detailed_summarize_article(text: str) -> list:
    """
    Generate a detailed, structured deep dive summary of an article 
    following the MASTER AI NEWS ANALYSIS PROMPT format.
    
    Args:
        text (str): The article text to analyze
        
    Returns:
        list: A list of dictionaries, each containing a title and content for each section of the summary.
    """
    detailed_prompt = """MASTER AI NEWS ANALYSIS PROMPT: STRUCTURED DEEP DIVE

"You are an advanced AI designed to analyze AI-related news articles with the rigor of a top-tier researcher and journalist. Your task is to break down each article into a structured, highly analytical format that extracts key insights, underlying trends, and contextual links to the broader AI landscape. Follow the structure below to ensure maximum clarity, depth, and cross-referencing of ideas across different articles."

DEEP DIVE
For each distinct topic or key theme in the article, structure the analysis as follows:

1. Topic Name
1a. Summary of the Topic
Provide a comprehensive yet concise summary of the article's core message.
Identify the main issue, technological breakthrough, controversy, or development being discussed.
If the article references a specific event (e.g., AI legislation, corporate announcement, breakthrough research), include date, location, and key stakeholders.
1b. Deep Dive: Key Details & Implications
Expand on the technical aspects, ethical considerations, and business or societal implications.
If applicable, discuss underlying AI models, techniques, or frameworks being referenced (e.g., GPT-4, diffusion models, reinforcement learning, etc.).
Break down who is affected—companies, governments, researchers, or the public.
Provide context on how this development fits into the broader AI industry (e.g., competition, regulation, economic impact).
Highlight any disputes, controversies, or differing expert opinions that shape the discussion.
1c. Cross-Linking to Other AI Trends
Explain how the topic relates to previous AI developments, historical context, or upcoming trends.
Identify connections with other major AI news stories (e.g., AI safety debates, job displacement, bias in AI models).
Predict future implications—what this news might mean for AI's trajectory in research, policy, or adoption.
2. Verbatim Expert Quotes & Source Attribution
Extract direct quotes from industry experts, executives, policymakers, or researchers mentioned in the article.
Attribute quotes to the correct sources (organizations, individuals) and include timestamps if from a video or live event.
If multiple sources provide differing viewpoints, highlight contrasts in opinions.
3. QnA: Industry Reactions & Public Debate
For any discussions referenced in the article (interviews, panel discussions, social media reactions):

Key Question or Concern Raised: Identify the main questions being debated.
Expert or Company Response: Provide the stated position of major players (e.g., OpenAI, Google DeepMind, policymakers, academics).
Public or Community Reactions: Summarize any significant public discourse—Twitter, Reddit, forums, or mainstream opinion shifts.
4. Technical & Mathematical Foundations (If Applicable)
If the article involves new AI research or breakthroughs, extract relevant technical details.
Break down algorithmic methods, statistical models, or mathematical formulations mentioned.
Explain complex concepts (e.g., gradient descent, neural network architectures, attention mechanisms) in an accessible manner.
If an AI model's performance is reported (e.g., accuracy, bias reduction, energy efficiency), analyze the metrics and benchmarks presented.
5. Actionable Takeaways from the Article
Summarize any practical implications for businesses, developers, or policymakers.
List recommended next steps for professionals in the AI industry (e.g., "Companies should prepare for X regulation", "Developers need to refine dataset transparency").
If the article mentions future releases, research directions, or company strategies, outline expected developments.
6. Any Hidden Signals or Industry Shifts
Identify any signals about market trends, regulatory movements, or competitive positioning in AI.
If the article subtly hints at AI risks, geopolitical issues, or ethical challenges, call these out explicitly.
Highlight any recurring themes across multiple news stories that indicate larger industry movements (e.g., layoffs in AI startups, increase in AI-generated content bans, major legal cases).
Final Notes
Ensure each section is detailed but skimmable, with clear headers and concise takeaways.
Maintain a critical yet balanced perspective, ensuring neutrality in cases of controversy.
Where possible, validate claims with external references or related reports for added credibility.
Structure the report so that it can be used by AI professionals, journalists, and policymakers alike for decision-making.
By following this structured approach, your analysis will transform AI news articles into comprehensive, research-grade intelligence reports that deliver depth, clarity, and insight into the ever-evolving AI landscape.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": detailed_prompt + "\n\n" + text
                }
            ],
            max_tokens=1500,
            temperature=0.5
        )
        raw_summary = response.choices[0].message.content
        # Split the raw summary into sections
        sections = parse_summary(raw_summary)
        return sections
    except Exception as e:
        logger.error(f"Error generating detailed summary: {str(e)}")
        return [{"title": "Error", "content": "Detailed summary unavailable"}]

def parse_summary(raw_summary: str) -> list:
    # Example parsing logic
    sections = []
    lines = raw_summary.split('\n')
    current_section = {"title": "", "content": ""}
    for line in lines:
        if line.startswith("1. ") or line.startswith("2. "):  # Detect section titles
            if current_section["title"]:
                sections.append(current_section)
            current_section = {"title": line, "content": ""}
        else:
            current_section["content"] += line + " "
    if current_section["title"]:
        sections.append(current_section)
    return sections

def categorize_article(text: str) -> str:
    """
    Categorize an article into predefined topics using OpenAI's GPT-4 model.
    
    Args:
        text (str): The article text to categorize
        
    Returns:
        str: The category of the article (Research, Business, Ethics, or Technical Innovations),
             or an error message if categorization fails
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": f"Categorize the following article into one of these topics: Research, Business, Ethics, or Technical Innovations:\n\n{text}"
                }
            ],
            max_tokens=20,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error categorizing article: {str(e)}")
        return "Categorization unavailable"

# Example usage:
if __name__ == "__main__":
    sample_text = "Your article text goes here..."
    print("Short Summary:", summarize_article(sample_text))
    print("Detailed Summary:", detailed_summarize_article(sample_text))
    print("Category:", categorize_article(sample_text))