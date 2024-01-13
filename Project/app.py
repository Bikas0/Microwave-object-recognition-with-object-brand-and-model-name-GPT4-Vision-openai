from flask import Flask, render_template, request, redirect, url_for
import os
from main import process_image

app = Flask(__name__)

uploads_dir = 'uploads'
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)


@app.route('/')
def index():
    return render_template('input.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']

    if uploaded_file.filename != '':
        # Save the uploaded file
        file_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(file_path)

        # Process the image and get the output
        brand_output, model_output, output_image_path = process_image(file_path)

        # Render the output
        return render_template('result.html', file_name=uploaded_file.filename,
                               output=[brand_output, model_output])
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
