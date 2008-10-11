import os.path
import re
import feedparser
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
import datetime
import time

def index(request):
    """ Entry point for the root of the site """


    def get_nice_feed(url):
        parsed_feed = feedparser.parse(url)
        feed = [
                  {
                      'title': truncchar(re.sub('^vesech: ', '', entry.title), 45),
                      'link': entry.link,
                      'updated': datetime.datetime.fromtimestamp(time.mktime(entry.updated_parsed))
                  }

                  for entry in parsed_feed.entries
              ]

        return feed

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

    def truncchar(value, arg):
        if len(value) < arg:
            return value
        else:
            return value[:arg] + '...'

    index = {
            'SVN' : {
                    'name' : 'svn',
                    'url' : 'http://svn.brokentrain.net/',
                    'repodir' : 'svn',
                    'items' : 5,
                },
            'PROJECTS' : {
                    'name' : 'projects',
                    'url' : 'projects/',
                    'items' : 5,
                },
            'UPLOAD' : {
                    'name' : 'upload',
                    'url' : 'upload/',
                    'items' : 5
                }
            }

    feeds = {
            'LAST_FM' : {
                    'name' : 'scrobs',
                    'url' : 'http://www.last.fm/user/gaving',
                    'items' : 5,
                    'feed' : 'http://ws.audioscrobbler.com/1.0/user/gaving/recenttracks.rss',
                },
            'BLOG' : {
                    'name' : 'blog',
                    'url' : 'blog/',
                    'items' : 5,
                    'feed' : 'http://gavin.brokentrain.net/blog/feed/',
                },
            'TWITTER' : {
                    'name' : 'tweets',
                    'url' : 'http://twitter.com/vesech',
                    'items' : 5,
                    'feed' : 'http://twitter.com/statuses/user_timeline/16518060.rss',
                },
            'DELICIOUS' : {
                    'name' : 'bookmarks',
                    'url' : 'http://delicious.com/vesech',
                    'items' : 5,
                    'feed' : 'http://feeds.delicious.com/v2/rss/vesech?count=15',
                },
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

    entries = get_nice_feed(feeds['BLOG']['feed'])
    tracks = get_nice_feed(feeds['LAST_FM']['feed'])
    tweets = get_nice_feed(feeds['TWITTER']['feed'])
    bookmarks = get_nice_feed(feeds['DELICIOUS']['feed'])

    return render_to_response('main/index.html', {
                'index': index,
                'feeds': feeds,
                'svn' : repos,
                'projects' : projects[:index['PROJECTS']['items']],
                'uploads' : uploads[:index['UPLOAD']['items']],
                'entries' : entries[:feeds['BLOG']['items']],
                'tracks' : tracks[:feeds['LAST_FM']['items']],
                'tweets' : tweets[:feeds['TWITTER']['items']],
                'bookmarks' : bookmarks[:feeds['DELICIOUS']['items']]
            })

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
