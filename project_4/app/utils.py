import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/uploads'

def allowed_file(filename):
    allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_media_file(file, upload_folder=UPLOAD_FOLDER):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)  # Create the folder if it doesn't exist
    
    filename = secure_filename(file.filename)  # Ensure the filename is safe
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)  # Save the file

    # Return the URL to access the file
    return f'/uploads/{filename}'
