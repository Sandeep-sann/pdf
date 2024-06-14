from flask import Flask, request, render_template, send_file
import pdfplumber
from gtts import gTTS
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    # Extract text from PDF
    text = ''
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    if not text.strip():
        return 'No text found in PDF', 400

    return text

@app.route('/synthesize', methods=['POST'])
def synthesize():
    text = request.form.get('text')
    if not text:
        return 'No text provided', 400

    # Convert text to speech
    tts = gTTS(text, lang='en', slow=True)
    audio = io.BytesIO()
    tts.write_to_fp(audio)
    audio.seek(0)

    return send_file(audio, mimetype='audio/mp3', as_attachment=True, download_name='speech.mp3')

if __name__ == '__main__':
    app.run(debug=True)
