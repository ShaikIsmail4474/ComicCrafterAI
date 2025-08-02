import openai
import replicate
import requests
from fpdf import FPDF
from PIL import Image
from io import BytesIO
from openai import OpenAI

# ✅ Set your API keys here
client = OpenAI(api_key="OPENAI_API_KEY")
replicate_client_token = 'r8_fIp1kfUVJ1FSeu92XqkCVG8CepfKggt3EgZgb'

# ✅ Generates a 4-part story using OpenAI
def generate_story_parts(prompt):
    format_prompt = f"""
    Write a short children's comic story in 4 parts:
    1. Introduction
    2. Storyline
    3. Climax
    4. Moral of the story

    Prompt: {prompt}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": format_prompt}],
        temperature=0.7,
        max_tokens=700,
    )

    story = response.choices[0].message.content
    parts = story.split('\n\n')
    return [p for p in parts if p.strip()][:4]
# ✅ Generates comic-style image using Replicate's Stable Diffusion
def generate_image(text):
    output = replicate.run(
        "stability-ai/stable-diffusion:db21e45e8e5a9d58e19cb29d1bc1c9945f38cfb2e2df9e4d36f7f4fdb40b5bda",
        input={
            "prompt": f"Comic book style illustration of: {text}",
            "width": 512,
            "height": 512,
            "num_inference_steps": 30,
            "guidance_scale": 7.5
        },
        api_token=replicate_client_token
    )
    return output[0]  # First image URL

# ✅ Creates a downloadable PDF comic with story + images
def create_comic_pdf(story_parts, image_urls, filename="comic_output.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for i in range(len(story_parts)):
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, story_parts[i])

        response = requests.get(image_urls[i])
        img = Image.open(BytesIO(response.content))
        img_path = f"temp_image_{i}.jpg"
        img.save(img_path)

        pdf.image(img_path, x=10, y=70, w=180)

    pdf.output(filename)
