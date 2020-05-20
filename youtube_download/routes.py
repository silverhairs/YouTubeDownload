from youtube_download import app
from youtube_download.forms import SearchForm
from flask import render_template, redirect, url_for, request, session, send_file, flash
from pytube import YouTube
from pytube.exceptions import RegexMatchError, LiveStreamError, VideoUnavailable
import requests


# Url expander in the case the user serves a shortened url
def expand_url(url):
    return requests.head(url, allow_redirects=True).url


# -> Index
@app.route('/', methods=['GET', 'POST'])
def index():
    title = 'Welcome'
    form = SearchForm()
    if form.validate_on_submit():
        expanded_url = expand_url(form.video_url.data)
        return redirect(url_for('results', yt_url=expanded_url))
    return render_template('index.html', form=form, title=title)


# -> Results
@app.route('/results', methods=['GET', 'POST'])
def results():
    title = 'Result'
    form = SearchForm()
    yt_url = request.args['yt_url']
    video = None
    session['video_url'] = yt_url
    try:
        video = YouTube(yt_url)
    except RegexMatchError:
        flash('Something is wrong with your link', 'is-danger is-light')
        return redirect(url_for('index'))
    except LiveStreamError:
        flash('Sorry, that video is a Live stream', 'is-info is-light')
        return redirect(url_for('index'))
    except VideoUnavailable:
        flash('Video not available', 'is-danger is-light')
        return redirect(url_for('index'))
    resolutions = ([
        stream.resolution
        for stream in video.streams.filter(progressive=True,
                                           file_extension='mp4')
    ])

    # When the user serves a new url
    if request.method == 'POST':
        if form.validate_on_submit():
            expanded_url = expand_url(form.video_url.data)
            return redirect(url_for('results', yt_url=expanded_url))

    # Getting the youtube video after fetching
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
