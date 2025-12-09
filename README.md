File: 07_ai_agent_with_tools.py

Description This script represents a major upgrade from a standard Chatbot to an "AI Agent." While a chatbot just talks, an Agent has the power to "do" things. This specific agent is equipped with three tools: a calculator (Sum), a logic checker (Prime Number), and a real-time market tracker (Crypto Price).

Key Concept

Function Calling (Tool Use): The LLM is taught not just to generate text, but to generate "code calls." If you ask "What is the price of Bitcoin?", the model doesn't guess. It recognizes it needs the 'get_crypto_price' tool and pauses to ask Python to run that function for it.

The Agent Loop: You will notice a 'while True' loop inside the run_agent function. This is the Agent's brain cycle:

Think: Does the user's question require a tool?

Act: If yes, call the tool.

Observe: Get the result from the Python function.

Respond: Use that result to answer the user.

Real-Time Data Access: Unlike the previous bots which relied only on training data (which is old), this agent connects to the live internet (CoinGecko API) to get up-to-the-second data
