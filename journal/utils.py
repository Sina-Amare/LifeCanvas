from openai import OpenAI
from django.conf import settings
import logging
from .models import Journal

logger = logging.getLogger(__name__)


def analyze_sentiment(content):
    """
    Analyze the sentiment of the given content using DeepSeek V3 via OpenRouter.
    Returns a mood string from the predefined MOOD_CHOICES.
    """
    # Initialize OpenAI client for OpenRouter
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.OPENROUTER_API_KEY,
    )

    # Define the prompt for sentiment analysis
    prompt = (
        "Analyze the sentiment of the following text and classify it as one of these moods: "
        "sometimes the text might be in another language rather than english , if so , first try changing it to persian and then analyze , e.g : boos = بوس = kiss , talkh = تلخ = bitter , ..."
        "happy, sad, angry, or neutral. Return only the mood word, nothing else.\n\n"
        f"Text: {content}"
    )

    try:
        # Call the DeepSeek V3 API
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost:8000",  # For OpenRouter rankings
                "X-Title": "LifeCanvas",  # For OpenRouter rankings
            },
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract the mood from the response
        mood = completion.choices[0].message.content.strip().lower()

        # Validate the mood against MOOD_CHOICES
        valid_moods = [choice[0] for choice in Journal.MOOD_CHOICES]
        if mood not in valid_moods:
            logger.warning(
                f"Invalid mood '{mood}' returned from DeepSeek. Defaulting to 'neutral'.")
            mood = "neutral"

        return mood

    except Exception as e:
        # Log the error and return a default mood
        logger.error(f"Error analyzing sentiment: {str(e)}")
        return "neutral"
