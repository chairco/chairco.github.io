#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from pathlib import Path
import re

AUTHOR = 'chairco(Jason)'
SITENAME = "Jason's Blog"
SITEURL = 'https://chairco.com.tw'

PATH = 'content'
STATIC_PATHS = ['blogs', 'pages', 'pics', 'files']
ARTICLE_PATHS = ['blogs']

ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_LANG_URL = 'posts/{date:%Y}/{date:%m}/{slug}-{lang}.html'
ARTICLE_LANG_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}-{lang}.html'

PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'
PAGE_LANG_URL = 'pages/{slug}/{lang}.html'
PAGE_LANG_SAVE_AS = 'pages/{slug}/{lang}.html'

TIMEZONE = 'Asia/Taipei'

DEFAULT_LANG = 'zh-Hant'
DEFAULT_DATE = 'fs'
DEFAULT_DATE_FORMAT = '%b %d, %Y'
USE_FOLDER_AS_CATEGORY = False
TYPOGRIFY = True
MD_EXTENSIONS = [
    'fenced_code',
    'extra',
    'codehilite(linenums=False)'
]


# Theme
THEME = "./pelican-clean-blog/"

# Flex theme setting
SITETITLE = "廢廢的阿宅，來看一下嘛，反正不用錢 >///<"
SITESUBTITLE = "Code / Travel / Other"
SITEDESCRIPTION = SITETITLE
SITELOGO = "/pics/20161206.png"
MAIN_MENU = True
MENUITEMS = [
    ('Archives', '/archives.html'),
    ('Categories', '/categories.html'),
    ('Tags', '/tags.html'),
    ('RSS', '/feeds/all.atom.xml')
]

COPYRIGHT_YEAR = 2017

CC_LICENSE = {
    'name': 'Creative Commons Attribution',
    'version': '4.0',
    'slug': 'by'
}
OG_LOCALE = 'zh_TW'


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


# Social widget
SOCIAL = (
    ('google', '#'),
    ('twitter', 'https://twitter.com/ChaircoChen'),
    ('facebook', 'https://www.facebook.com/chairco'),
    ('github', 'https://github.com/chairco'),
    ('RSS', 'http://chairco.com.tw/feeds/all.atom.xml'),
    ('envelope-o', 'mailto:chairco@gmail.com'),
    ('linkedin', '#'),
)

SUMMARY_MAX_LENGTH = 24
DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

DISQUS_SITENAME = "chairco"

GOOGLE_ANALYTICS = "UA-79798833-1"

