# Audio and Video to Text Conversion using Flask

This project is a Flask-based web application that allows users to upload audio and video files and converts them into text using speech recognition techniques. The application provides a user-friendly interface to upload the files and displays the extracted text as the result.

## Prerequisites

- Python 3.x
- virtualenv

## Installation

1. Clone the repository:

   ```shell
   git clone git@github.com:kheersagarpatel/audio-video-to-text.git
   or
   git clone https://github.com/kheersagarpatel/audio-video-to-text.git
   or
   Download as Zip
   ```

2. Change Directory:

   ```shell
   cd audio-video-to-text
   ```

3. Create a virtual environment (ref: [Create Python Virtual Environments with venv for linux](https://developers.knowivate.com/@kheersagar/creating-python-virtual-environments-on-ubuntu-with-venv)):

   ```shell
   python3 -m venv myenvname
   For Windows
   python -m venv myenvname
   ```

3. Activate the virtual environment:

   ```shell
   For Linux
   source myenvname/bin/activate
   For Windows
   myenvname\Scripts\activate
   ```

4. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

## Usage

1. Run the application in debug mode:

   ```shell
   flask --app vtext run --debug
   ```

   OR

   Run the application in production mode:

   ```shell
   flask --app vtext run
   ```

2. Access the application in your web browser at `http://127.0.0.1:5000/`.

3. Upload an audio or video file using the provided forms on the page.

4. The application will process the file and display the extracted text in the result.

## License

This project is licensed under the [MIT License](LICENSE).

Please make sure to update the `myenvname` placeholder in the README with your desired virtual environment name.

Let me know if you need any further assistance!