from openai import OpenAI
from environs import Env

env = Env()
env.read_env()

OPENAI_API_KEY = env("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)