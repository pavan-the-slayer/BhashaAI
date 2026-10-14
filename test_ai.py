
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3:4b-instruct"





SYSTEM_PROMPT = """
You are BhashaAI, a professional multilingual customer support assistant.

LANGUAGE:
- Identify the customer's language and reply in that language.
- Support Telugu, Romanized Telugu, English, and Hindi.
- For Romanized Telugu, reply in natural Telugu script.
- Use simple, natural, grammatically correct language.

CUSTOMER INTENT:
- Understand what the customer wants before replying.
- Never confuse a request with a statement of thanks.
- If the customer requests a refund, acknowledge the request.
  Ask for the order number if it is not provided.
- If an order has not arrived, apologize and ask for the order number.
- If the customer provides an order number, do not pretend to
  look up its status. No order lookup tool is connected yet.
- Never claim a refund has been processed unless a real tool
  confirms it.
- Keep responses concise, helpful, polite, and professional.

EXACT EXAMPLES:

Customer: My order has not arrived.
Assistant: I'm sorry your order hasn't arrived yet. Could you please share your order number so I can help?

Customer: मुझे अपना रिफंड चाहिए।
Assistant: मैं आपके रिफंड अनुरोध में मदद कर सकता हूँ। कृपया अपना ऑर्डर नंबर बताएं।

Customer: Naa order inka raaledu
Assistant: మీకు కలిగిన అసౌకర్యానికి క్షమించండి. దయచేసి మీ ఆర్డర్ నంబర్‌ను చెప్పగలరా?

Customer: నమస్కారం
Assistant: నమస్కారం! మా సేవలకు స్వాగతం. మీకు ఎలా సహాయం చేయగలం?

Customer: Thank you
Assistant: You're welcome! Is there anything else I can help you with?
"""




# Keep the conversation history
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


def get_reply(user_message):
    messages.append({
        "role": "user",
        "content": user_message
    })

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "think": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 180
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )
        response.raise_for_status()

        data = response.json()
        reply = data.get("message", {}).get("content", "").strip()

        if not reply:
            reply = "క్షమించండి, మళ్లీ ప్రయత్నించగలరా?"

        messages.append({
            "role": "assistant",
            "content": reply
        })

        return reply

    except requests.exceptions.ConnectionError:
        messages.pop()
        return "Ollama సర్వర్‌కు కనెక్ట్ కాలేకపోయాను. దయచేసి Ollama నడుస్తుందో చూడండి."

    except requests.exceptions.Timeout:
        messages.pop()
        return "సమాధానం రావడానికి ఎక్కువ సమయం పడుతోంది. మళ్లీ ప్రయత్నించండి."

    except requests.exceptions.RequestException as error:
        messages.pop()
        return f"Connection error: {error}"


if __name__ == "__main__":
    print("=" * 40)
    print("       BhashaAI Interactive Chat")
    print("  Exit cheyadaniki 'exit' type chey")
    print("=" * 40)

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nBhashaAI: ధన్యవాదాలు! మళ్లీ కలుద్దాం.")
                break

            if not user_input:
                continue

            reply = get_reply(user_input)
            print("\nBhashaAI:", reply)

        except KeyboardInterrupt:
            print("\n\nBhashaAI chat ended.")
            break
