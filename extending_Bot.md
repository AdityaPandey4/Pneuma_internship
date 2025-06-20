
### **Hand-off Document: `EXTENDING_THE_BOT.md`**


# How to Add a New FAQ to the Pneuma Bot

This guide explains how to add a new question-and-answer capability to the Pneuma WhatsApp bot. The process is designed to be quick and should take less than 10 minutes.

**Prerequisite:** You have the project code on your machine and a code editor like VS Code.

### **Step 1: Open the Main Application File**

All the core logic for the bot is located in one place.

*   Open the file: `main.py`

### **Step 2: Find the Intent Routing Function**

Scroll down until you find the function named `route_intent`. This is where the bot decides how to answer a message. It looks like this:

```python
def route_intent(user_message: str) -> str:
    """
    A simple keyword-based router to handle different user intents.
    This is where new FAQs can be added.
    """
    normalized_message = user_message.lower()

    # --- INTENT 1: SWEET-SPOT DEALS ---
    if any(keyword in normalized_message for keyword in ["deal", "sweet spot"]):
        # ... logic for deals ...

    # ... other elif blocks ...
```

### **Step 3: Add a New `elif` Block for Your FAQ**

We will add a new "else if" (`elif`) block to handle the new question. For this example, let's add an FAQ about **Pneuma's pricing**.

1.  **Choose your keywords:** Think of the words a user might type to ask this question. For pricing, good keywords would be `pricing`, `cost`, `how much`, `free`.

2.  **Write the factual context:** This is the "source of truth" that the AI will use to form its answer. Keep it simple and factual.

Copy and paste the following code block *before* the final `else:` block in the function.

```python
    # --- NEW INTENT: PRICING ---
    elif any(keyword in normalized_message for keyword in ["pricing", "cost", "how much", "free"]):
        context = """
        Pneuma has two tiers:
        1. Free Tier: You get access to our weekly newsletter with one "sweet-spot" deal highlight.
        2. Premium Tier ($10/month): You get full access to the WhatsApp bot for real-time deal alerts and on-demand searches.
        """
        return get_llm_response(user_message, context)
```

### **Step 4: Verify the Placement**

Your `route_intent` function should now look something like this (new block is highlighted):

```python
    # ... other intent blocks ...

    # --- NEW INTENT: PRICING ---
    elif any(keyword in normalized_message for keyword in ["pricing", "cost", "how much", "free"]):
        context = """
        Pneuma has two tiers:
        1. Free Tier: You get access to our weekly newsletter with one "sweet-spot" deal highlight.
        2. Premium Tier ($10/month): You get full access to the WhatsApp bot for real-time deal alerts and on-demand searches.
        """
        return get_llm_response(user_message, context)

    # --- FALLBACK RESPONSE ---
    else:
        # ... fallback logic ...
```

### **Step 5: Save and Test**

1.  **Save** the `main.py` file. If your `uvicorn` server is running with `--reload`, it will automatically restart. If not, stop it (`CTRL+C`) and start it again (`uvicorn main:app --reload`).
2.  **Test** your new FAQ using a `curl` command in a separate terminal.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"Body": "how much does it cost?", "From": "whatsapp:+1234567890"}' http://127.0.0.1:8000/whatsapp
```

You should receive a neatly formatted answer about Pneuma's pricing tiers. You're done!

