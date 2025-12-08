import requests
from google import genai
from google.genai import types

# --- 1. YOUR PROVIDED FUNCTIONS ---

def isPrime(num):
    limit=num>>2
    if num<2:
        return False
    else:
        for i in range(2,limit+1):
            if num%i==0:
                return False 
    return True

def sum(num1, num2): 
    return num1 + num2

def get_crypto_price(coin):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin}"

    # 2. Make the GET request (Equivalent to await fetch)
    response = requests.get(url)
    
    # 3. Parse JSON (Equivalent to await response.json())
    data = response.json()
    
    # 4. Extract just the price (Optional, but cleaner)
    # Data looks like: {'bitcoin': {'usd': 98000}}
    # API returns a list, so we access [0]
    try:
        price = data[0]['current_price']
        return price
    except:
        return "Price not found"

# --- 2. SETUP CLIENT & HISTORY ---

client = genai.Client(api_key="your valid api")

# 2. Initialize an empty list to maintain chat history manually
chat_history = []

print("--- Manual Chat History (Type 'quit' to exit) ---")

# --- 3. TOOL DECLARATIONS ---
# here the name should match with exact function name this part is similar as LLM is giving the structured input 
sumDeclaration = {
    'name':'sum',
    'description':'Get the sum of two numbers',
    'parameters':{ # Fixed typo: 'parameter' -> 'parameters' for API compatibility
        'type':'OBJECT',  
        'properties':{
            'num1':{
                'type':'NUMBER',
                'description': 'It will be first number for addition ex: 10'
                },
            'num2':{
                'type':'NUMBER',
                'description':'It will be Second number for addition ex: 10'
            }},
        'required':['num1','num2']
    }
}

primeDeclaration = {
    'name':'isPrime',
    'description':"Get if number if prime or not",
    'parameters':{
        'type':'OBJECT',
        'properties':{
            'num':{
                'type':'NUMBER',
                'description': 'It will be the number to find it is prime or not ex: 13'
            },
        },
        'required': ['num']   
    }
}

cryptoDeclaration = {
    'name':'get_crypto_price',
    'description':"Get the current price of any crypto Currency like bitcoin",
    'parameters':{
        'type':'OBJECT',
        'properties':{
            'coin':{
                'type':'STRING',
                'description': 'It will be the crypto currency name, like bitcoin'
            },
        },
        'required': ['coin']   
    }
}

# --- 4. MAP TOOLS TO FUNCTIONS ---
available_tools = {
    "sum": sum,
    "isPrime": isPrime,
    "get_crypto_price": get_crypto_price
}

# --- 5. THE AGENT LOGIC (Converted from JS runAgent) ---
def run_agent(user_problem):
    
    # Push User Query to History
    chat_history.append({
        "role": "user",
        "parts": [{"text": user_problem}]
    })

    while True:
        # Call Gemini with Tools
        response = client.models.generate_content(
            model="gemini-2.0-flash", # Using 2.0 as it is more stable for tools
            contents=chat_history,
            config=types.GenerateContentConfig(
                system_instruction="""You are an AI Agent, You have access of 3 available tools like to to find sum or add of 2 number, get crypto price of any currency and find a number is prime or not. Use these tools whenever required to confirm user query. If user ask general question you will still answer it even if you don't need of these three tools only add these lines first then answer "mujhe dusre bhai tools se puchhna parega" initially then in nxt line you will answer""",
                tools=[{
                    "function_declarations": [sumDeclaration, primeDeclaration, cryptoDeclaration]
                }]
            )
        )

        # Check if the model wants to call a function
        # In Python SDK, we check for function_calls in the response
        if response.function_calls and len(response.function_calls):
            # Get the first function call
            print(response.function_calls[0] ," is called ")
            call = response.function_calls[0]
            fn_name = call.name
            fn_args = call.args


# to check whether my own functions are being used or not
            # print(f"🤖 Tool Call: {fn_name}({fn_args})")

            # Execute the actual Python function
            if fn_name in available_tools:
                tool_result = available_tools[fn_name](**fn_args)
            else:
                tool_result = "Error: Function not found"

            # 1. Add Model's "Call" to history
            chat_history.append(response.candidates[0].content)

            # 2. Add the "Result" to history
            # result Ko history daalna
            chat_history.append({
                "role": "user", # Function responses come from the 'tool' (user side)
                "parts": [{
                    "function_response": {
                        "name": fn_name,
                        "response": {"result": tool_result}
                    }
                }]
            })
            
            # Loop continues to let the model see the result and generate text
        
        else:
            # No function call? Then it's a text response.
            model_text = response.text
            
            chat_history.append({
                "role": "model",
                "parts": [{"text": model_text}]
            })
            
            print(f"agent: {model_text}")
            break

# --- 6. MAIN LOOP ---
if __name__ == "__main__":
    while True:
        user_input = input("\nAsk me anything--> ")
        if user_input.lower() in ["quit", "exit"]:
            break
        
        run_agent(user_input)