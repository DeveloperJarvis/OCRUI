# Routes
import os
import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from .forms import UploadImageForm
from flask import current_app as app

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'app/static/images/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = UploadImageForm()
    response_json = None
    image_filename = None
    prev_images = os.listdir(UPLOAD_FOLDER)
    prev_images.sort(reverse=True)

    if form.validate_on_submit():
        image = form.uploaded_image.data
        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)
        image_filename = filename

        with open(image_path, 'rb') as img_file:
            files = {'uploaded_image': img_file}
            try:
                res = requests.post(app.config['API_URL'], files=files)
                res.raise_for_status()
                response_json = res.json()
            except Exception as e:
                flash(f"API error: {e}", 'danger')

    return render_template('index.html', form=form, response_json=response_json, 
                           image_filename=image_filename, prev_images=prev_images)
