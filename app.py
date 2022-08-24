import os
import tempfile
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import sys
import torch
import PIL
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer

UPLOAD_FOLDER = os.path.join(tempfile.gettempdir())
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = VisionEncoderDecoderModel.from_pretrained('nlpconnect/vit-gpt2-image-captioning')
feature_extractor = ViTFeatureExtractor.from_pretrained('nlpconnect/vit-gpt2-image-captioning')
tokenizer = AutoTokenizer.from_pretrained('nlpconnect/vit-gpt2-image-captioning')

device = torch.device(('cuda' if torch.cuda.is_available() else 'cpu'))
model.to(device)

gen_kwargs = {'max_length': 16, 'num_beams': 4}

def predict_text(image_path):
    images = []
    i_image = PIL.Image.open(image_path)
    if i_image.mode != 'RGB':
        i_image = i_image.convert(mode='RGB')
    images.append(i_image)

    pixel_values = feature_extractor(images=images, return_tensors='pt').pixel_values
    pixel_values = pixel_values.to(device)
    output_ids = model.generate(pixel_values, **gen_kwargs)
    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return ' '.join(preds)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filename)
            return predict_text(filename)
    return app.send_static_file("index.html")
