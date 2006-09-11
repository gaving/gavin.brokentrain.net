import os.path
import feedparser
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
	""" Entry point for the root of the site """

	index = {
			'SVN' : {
					'name' : 'svn',
					'url' : 'http://svn.brokentrain.net/',
					'items' : 5
				},
			'PROJECTS' : {
					'name' : 'projects',
					'url' : 'projects/',
					'items' : 5
				},
			'LAST_FM' : {
					'name' : 'music',
					'url' : 'http://www.last.fm/user/gaving',
					'items' : 8,
					'feed' : 'http://ws.audioscrobbler.com/1.0/user/gaving/recenttracks.rss'
				},
			'UPLOAD' : {
					'name' : 'upload',
					'url' : 'upload/',
					'items' : 10
				}
			}

	projects = []
	for file in os.listdir(index['PROJECTS']['url']):
		fullpath = os.path.join(index['PROJECTS']['url'], file)
		if os.path.isdir(fullpath):
			projects.append((os.path.getatime(fullpath), file, fullpath))

	projects.sort()
	projects.reverse()

	uploads = []
	for file in os.listdir(index['UPLOAD']['url']):
		fullpath = os.path.join(index['UPLOAD']['url'], file)
		uploads.append((os.path.getatime(fullpath), file, fullpath))

	uploads.sort()
	uploads.reverse()

	d = feedparser.parse(index['LAST_FM']['feed'])

	return render_to_response('main/index.html', {
		'index': index,
		'projects' : projects[:index['PROJECTS']['items']],
		'tracks' : d.entries[:index['LAST_FM']['items']],
		'uploads' : uploads[:index['UPLOAD']['items']]
	})

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
