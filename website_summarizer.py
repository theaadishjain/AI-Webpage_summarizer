import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
import google.generativeai as genai

# Load API Key from .env file
load_dotenv(override=True)
api_key = os.getenv("GEMINIAI_API_KEY")

if not api_key:
    print("No API key was found - please check your .env file and set GEMINIAI_API_KEY properly!")
elif not api_key.startswith("AIza"):  gi
    print("An API key was found, but it doesn't look like a valid Gemini API key; please double-check!")
elif api_key.strip() != api_key:
    print("An API key was found, but it has extra spaces or tab characters - please remove them!")
else:
    print("API key found and looks good so far!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Generate response
message = "Hello, Gemini! This is my first ever message to you! Hi!"
response = model.generate_content(message)
print(response.text)

# Define Headers for Web Scraping
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

# Website Class
class Website:
    def __init__(self, url):
        """
        Create this Website object from the given URL using BeautifulSoup
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

# Test the Website Class
ed = Website("https://edwarddonner.com")
print(ed.title)
print(ed.text)

# Define system prompt
system_prompt = "You are an assistant that analyzes the contents of a website and provides a short summary, ignoring navigation text. Respond in markdown."

# Generate user prompt
def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}\n"
    user_prompt += "The contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt

print(user_prompt_for(ed))

# Define message format for Gemini
def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

# Summarize function using Gemini
def summarize(url):
    website = Website(url)
    response = model.generate_content(user_prompt_for(website))
    return response.text

# Function to display the summary using Markdown
def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))

# Display website summaries
display_summary("https://edwarddonner.com")
display_summary("https://cnn.com")
display_summary("https://anthropic.com")

# Step 1: Create prompts
system_prompt = "You are an AI assistant."
user_prompt = "Summarize this website content."

# Step 2: Make messages list
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

# Step 3: Call Gemini API
response = model.generate_content(user_prompt)

# Step 4: Print the result
print(response.text)
