from flask import Flask, render_template, request, send_file
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        # YouTube video URL ko form se lekar
        video_url = request.form['url']
        
        # yt-dlp options set karein
        ydl_opts = {
            'format': 'best',  # Best quality mein download karein
            'outtmpl': '%(title)s.%(ext)s',  # Output file ka naam
        }
        
        # Video download karein
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', 'video')
            video_filename = f"{video_title}.mp4"
        
        # Download kiye gaye video ko user ko send karein
        return send_file(video_filename, as_attachment=True, download_name=video_filename)
    
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)