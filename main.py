import os
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

# --- 1. SETUP AND CONFIGURATION ---

# Load environment variables from .env file (for the OpenAI API key)
load_dotenv()

# Initialize the FastAPI app
app = FastAPI()

# Get the OpenAI API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Initialize the Gemini client
client = genai.Client(api_key=api_key)


# Pydantic model to validate the incoming webhook data (mocked from WhatsApp/Twilio)
class WhatsAppMessage(BaseModel):
    Body: str
    From: str # Example: "whatsapp:+14155238886"

# --- 2. PROMPT RECIPES AND LLM LOGIC ---

# The global system prompt that defines the bot's personality and rules
SYSTEM_PROMPT = """
You are a helpful WhatsApp assistant for Pneuma, a service that finds the best ways to use travel points and miles.

Your voice is:
- Plain-English and direct.
- Data-backed and factual.
- Quietly witty, but never snarky or unprofessional.

Your rules are:
- Be concise. WhatsApp is not the place for essays.
- Avoid marketing buzzwords like "revolutionize," "unlock," or "supercharge."
- Your answer must be based *only* on the factual context provided in the user's message.
- If the user's question cannot be answered from the provided context, politely state that you don't have that specific information.
"""

def get_llm_response(user_message: str, context: str) -> str:
    """
    Calls the OpenAI API to get a response based on the provided context and user message.
    """
    try:
        response = client.models.generate_content(
        model="gemini-1.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT),
            contents={f"Context:\n{context}\n\nUser Question:\n{user_message}\n\nTask: Answer the user's question."},
            # temperature=0.1
        )

        # print(response.text)
        return response.text

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Sorry, I'm having a little trouble connecting right now. Please try again in a moment."


def route_intent(user_message: str) -> str:
    """
    A simple keyword-based router to handle different user intents.
    This is where new FAQs can be added.
    """
    normalized_message = user_message.lower()

    # --- INTENT 1: SWEET-SPOT DEALS ---
    if any(keyword in normalized_message for keyword in ["deal", "sweet spot", "sweet-spot"]):
        context = """
        Today's Sweet-Spot Deals:
        - Deal 1: Fly Business Class from New York (JFK) to Lisbon (LIS) on TAP Air Portugal for 35,000 Amex points. It's the best way to cross the Atlantic without a trust fund.
        - Deal 2: Fly Economy from Los Angeles (LAX) to Tokyo (HND) on ANA for 55,000 Chase points round-trip. Yes, round-trip.
        - Deal 3: Fly from Chicago (ORD) to a surprise Caribbean destination (e.g., AUA, PUJ) on United for 12,500 MileagePlus miles. We call this one "The Escape Hatch."
        """
        return get_llm_response(user_message, context)

    # --- INTENT 2: MILEAGE TRANSFER BASICS ---
    elif any(keyword in normalized_message for keyword in ["transfer", "move points"]):
        context = """
        Mileage Transfer Basics: Transferring points means sending them from a flexible rewards program (like Amex, Chase, or Capital One) to a specific airline or hotel partner (like United, British Airways, or Hyatt).

        Why it's useful: It gives you flexibility. You don't have to commit your points to one airline until you find a flight you're ready to book.

        One key rule: Transfers are almost always a one-way street. Once you move your points from the bank to the airline, you can't move them back. So, it's best to confirm your flight is available before you transfer.
        """
        return get_llm_response(user_message, context)

    # --- INTENT 3: GENERAL FAQ ("WHAT IS PNEUMA?") ---
    elif any(keyword in normalized_message for keyword in ["what is pneuma", "what do you do", "about this service"]):
        context = """
        Pneuma is a service that helps you find great flights you can book with your existing credit card points and airline miles. Instead of you spending hours searching, we find the "sweet spot" deals—high-value redemptions where your points go furthest—and show you how to book them. We focus on the data, not the hype.
        """
        return get_llm_response(user_message, context)

    # --- FALLBACK RESPONSE ---
    else:
        # Fallback context provides a general "I don't know" capability
        context = "The user is asking a question that does not match any of the known intents (deals, transfers, about Pneuma)."
        return get_llm_response(user_message, context)


# --- 3. API ENDPOINT ---

@app.post("/whatsapp")
async def whatsapp_webhook(message: WhatsAppMessage):
    """
    This endpoint simulates receiving a message from WhatsApp via Twilio.
    It takes the incoming message, routes it to the correct logic,
    and returns the bot's response.
    """
    print(f"Received message from {message.From}: '{message.Body}'")
    
    # Route the message to the appropriate handler based on its content
    response_text = route_intent(message.Body)
    
    print(f"Generated response: '{response_text}'")
    
    # In a real Twilio app, you'd return TwiML XML.
    # For this prototype, we'll return a simple JSON response.
    return {"reply": response_text}


@app.get("/")
def read_root():
    """A simple root endpoint to confirm the server is running."""
    return {"status": "Pneuma FAQ Bot is running"}