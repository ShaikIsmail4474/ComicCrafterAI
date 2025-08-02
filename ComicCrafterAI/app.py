from flask import Flask, render_template, request, send_file
from utils import generate_story_parts, generate_image, create_comic_pdf
import json

app = Flask(__name__)

# Homepage - input prompt and get comic
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        story_parts = generate_story_parts(prompt)

        images = []
        for part in story_parts:
            images.append(generate_image(part))

        return render_template('result.html', story=story_parts, images=images)

    return render_template('index.html')

# Comic PDF download route
@app.route('/download', methods=['POST'])
def download():
    story = json.loads(request.form['story'])
    images = json.loads(request.form['images'])

    create_comic_pdf(story, images)
    return send_file("comic_output.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
