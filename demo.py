def isPrime(num):
    limit=num>>2
    if num<2:
        return False
    else:
        for i in range(2,limit+1):
            if num%i==0:
                return False 
    return True

def sum(a,b):
    return a+b



# Here we are working through api that has following steps.
# To convert that JavaScript fetch code into Python, you need the requests library. Python doesn't have a built-in fetch function.

# Step,Code Line,Programming Concept,Kya ho raha hai (Behind the Scenes)
# 1. Initialization,"url = f""https://...""",Data Preparation,Aapne Python mein ek String taiyar ki. Abhi tak internet par kuch nahi gaya. Yeh bas address likha hai envelope par.
# 2. HTTP Request,requests.get(url),Request Transmission,requests library ne aapke URL ko internet packet mein pack kiya aur CoinGecko ke server ko bhej diya.
# 3. Server Processing,(Hidden Internet Process),Processing,"CoinGecko server ne aapki request padhi, database check kiya, aur Bitcoin ka price nikala."
# 4. HTTP Response,response = ...,Raw Response (JSON String),"Jawab wapas aaya response variable mein.  Important: Is waqt data JSON String format mein hai (e.g., ""{'bitcoin':...}""). Python isse abhi Dictionary ki tarah nahi padh sakta."
# 5. Deserialization,data = response.json(),Decoding (Parsing),Yeh sabse main step hai.  json() function ne us lambi JSON String ko Python Dictionary (dict) mein convert kiya. Ab Python is data ko samajh sakta hai.
# 6. Usage,data[coin]['usd'],Data Access,"Kyunki Step 5 mein data Dictionary ban gaya tha, ab aap ['key'] use karke price nikaal paaye."




import requests

def get_crypto_price(coin):
    # 1. Define the URL (Using f-string to insert the coin name)
    # In JS you used backticks `...${coin}...`, in Python we use f"..."
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin}"

    # 2. Make the GET request (Equivalent to await fetch)
    response = requests.get(url)
    
    # 3. Parse JSON (Equivalent to await response.json())
    data = response.json()
    
    # 4. Extract just the price (Optional, but cleaner)
    # Data looks like: {'bitcoin': {'usd': 98000}}
    price = data[coin]['usd']
    return f"The price of {coin} is ${price}"


user_problem = input("\nAsk me anything --> ")
print(user_problem)