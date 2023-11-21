from django.shortcuts import render
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


def generate(request):
        if request.method == "POST":
            input=request.POST.get('input')
            result=scriptgenerate(input)
            return render(request,'script_studio/index.html',{'result':result})
        else:
            return render(request,'script_studio/index.html')

def scriptgenerate(input):
    client = OpenAI(
        api_key=os.getenv('api_key')
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input,
            }
        ],
        model="gpt-3.5-turbo",
    )
    Result=chat_completion.choices[0].message.content
    return Result
    




