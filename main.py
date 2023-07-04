from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("client_id")
SECRET_KEY = os.getenv("SECRET_KEY")

print("client_id: ", client_id)
print("API_SECRET: ", SECRET_KEY)