from flask import Flask, render_template, request, flash, redirect
import os
from werkzeug.utils import secure_filename
import speech_recognition as sr
import cv2
import moviepy.editor as mp

app = Flask(__name__)

# Set the secret key for the session
app.secret_key = 'your_secret_key'

# Set up environment variables
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3', 'ogg', 'webm', 'mp4'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_audio(audio_file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        flash('Could not recognize audio')
    except sr.RequestError:
        flash('Could not connect to the speech recognition service')
    except Exception as e:
        flash(f'Error: {str(e)}')
    return None

def extract_text_from_video(video_file):
    video = mp.VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile("temp_audio.wav")

    # Extract text from the temporary audio file
    text = extract_text_from_audio("temp_audio.wav")
    
    # Remove the temporary audio file
    os.remove("temp_audio.wav")

    return text

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'audio' in request.files:
            audio_file = request.files['audio']
            if audio_file.filename == '':
                flash('No audio file selected')
                return redirect(request.url)
            if audio_file and allowed_file(audio_file.filename):
                filename = secure_filename(audio_file.filename)
                upload_folder = app.config['UPLOAD_FOLDER']
                os.makedirs(upload_folder, exist_ok=True)
                filepath = os.path.join(upload_folder, filename)
                audio_file.save(filepath)
                text = extract_text_from_audio(filepath)
                os.remove(filepath)
                if text:
                    return render_template('result.html', text=text)
            else:
                flash('Invalid audio file format')
                return redirect(request.url)
        
        if 'video' in request.files:
            video_file = request.files['video']
            if video_file.filename == '':
                flash('No video file selected')
                return redirect(request.url)
            if video_file and allowed_file(video_file.filename):
                filename = secure_filename(video_file.filename)
                upload_folder = app.config['UPLOAD_FOLDER']
                os.makedirs(upload_folder, exist_ok=True)
                filepath = os.path.join(upload_folder, filename)
                video_file.save(filepath)
                text = extract_text_from_video(filepath)
                os.remove(filepath)
                if text:
                    return render_template('result.html', text=text)
            else:
                flash('Invalid video file format')
                return redirect(request.url)

    return render_template('upload.html')


@app.route('/upload_video', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'video' not in request.files:
            flash('No video file selected')  # Corrected flash message
            return redirect(request.url)

        video_file = request.files['video']

        # Check if the file is allowed
        if video_file and allowed_file(video_file.filename):
            # Save the file to the upload folder
            filename = secure_filename(video_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video_file.save(filepath)

            # Process the video file and extract text
            text_from_video = extract_text_from_video(filepath)

            # Delete the uploaded video file
            os.remove(filepath)

            return render_template('result.html', text=text_from_video)

    return render_template('upload.html')


if __name__ == '__main__':
    app.run()
