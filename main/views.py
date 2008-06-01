import os.path
import re
from feedparser import feedparser
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    """ Entry point for the root of the site """

    def get_image(filename):
        images = re.compile(r'[\w\W]*.(jpg|png|gif)$')
        audio = re.compile(r'[\w\W]*.(mp3|wav|ogg|flac)$')
        text = re.compile(r'[\w\W]*.(txt|doc|pdf|dat)$')
        video = re.compile(r'[\w\W]*.(mpg|avi|ogm|mpeg|mkv)$')
        archive = re.compile(r'[\w\W]*.(tar|tar.gz|bz2|tar.bz2|tgz|rar|zip)$')

        if images.match(filename):
            return 'mime-image.png'
        elif audio.match(filename):
            return 'mime-audio.png'
        elif text.match(filename):
            return 'mime-text.png'
        elif video.match(filename):
            return 'mime-video.png'
        elif archive.match(filename):
            return 'mime-archive.png'
        else:
            return 'mime-unknown.png'

    index = {
            'SVN' : {
                    'name' : 'svn',
                    'url' : 'http://svn.brokentrain.net/',
                    'repodir' : '../svn',
                    'items' : 5,
                },
            'PROJECTS' : {
                    'name' : 'projects',
                    'url' : 'projects/',
                    'items' : 5,
                },
            'LAST_FM' : {
                    'name' : 'music',
                    'url' : 'http://www.last.fm/user/gaving',
                    'items' : 8,
                    'feed' : 'http://ws.audioscrobbler.com/1.0/user/gaving/recenttracks.rss',
                },
            'UPLOAD' : {
                    'name' : 'upload',
                    'url' : 'upload/',
                    'items' : 5
                },
            'BLOG' : {
                    'name' : 'blog',
                    'url' : 'blog/',
                    'items' : 5
                }
            }

    repos = []
    for file in os.listdir(index['SVN']['repodir']):
        fullpath = os.path.join(index['SVN']['repodir'], file)
        if os.path.isdir(fullpath):
            repos.append(file)
    repos.sort()

    projects = []
    for file in os.listdir(index['PROJECTS']['url']):
        fullpath = os.path.join(index['PROJECTS']['url'], file)
        if os.path.isdir(fullpath):
            projects.append((os.path.getmtime(fullpath), file, fullpath))

    projects.sort()
    projects.reverse()

    uploads = []
    for file in os.listdir(index['UPLOAD']['url']):
        fullpath = os.path.join(index['UPLOAD']['url'], file)
        uploads.append((os.path.getatime(fullpath), file, fullpath, get_image(file)))

    uploads.sort()
    uploads.reverse()

    d = feedparser.parse(index['LAST_FM']['feed'])

    return render_to_response('main/index.html', {
            'index': index,
            'svn' : repos,
            'projects' : projects[:index['PROJECTS']['items']],
            'tracks' : d.entries[:index['LAST_FM']['items']],
            'uploads' : uploads[:index['UPLOAD']['items']]
            })

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
