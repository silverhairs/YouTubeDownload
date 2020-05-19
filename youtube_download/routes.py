from youtube_download import app
from flask import render_template, redirect, url_for, request, session, send_file
from pytube import YouTube
from youtube_download.forms import SearchForm


# -> Index
@app.route('/', methods=['GET', 'POST'])
def index():
    title = 'Welcome'
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('results', yt_url=form.video_url.data))
    return render_template('index.html', form=form, title=title)


# -> Results
@app.route('/results', methods=['GET', 'POST'])
def results():
    title = 'Result'
    form = SearchForm()
    yt_url = request.args['yt_url']
    session['video_url'] = yt_url
    video = YouTube(yt_url)
    resolutions = [
        stream.resolution
        for stream in video.streams.filter(progressive=True,
                                           file_extension='mp4')
    ]
    if request.method == 'POST':
        if form.validate_on_submit():
            video = YouTube(form.video_url.data)
            session['video_url'] = form.video_url.data
            return render_template(
                'results.html',
                video=video,
                resolutions=resolutions,
                form=form,
            )

    elif request.method == 'GET':
        return render_template(
            'results.html',
            video=video,
            title=title,
            resolutions=resolutions,
            form=form,
        )


# -> Return video
@app.route('/download')
def download_video():
    resolution = request.args['resolution']
    video = session.get('video_url', None)
    video = YouTube(video)
    return send_file(
        video.streams.filter(progressive=True,
                             file_extension='mp4',
                             resolution=resolution).first().download(),
        as_attachment=True,
    )
