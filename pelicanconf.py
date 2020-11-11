#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from pathlib import Path
import re

# Base setting
AUTHOR = 'Jason'
SITENAME = "Jason's Blog"
SITEURL = 'https://blog.chairco.me'

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
# Theme Path
#THEME = "./pelican-clean-blog/"
THEME = "./nest/"
# Theme setting
SITETITLE = u"廢廢的宅生物，歡迎餵食，禁止拍打"
SITESUBTITLE = SITETITLE #"Code / Travel / Other"
SITEDESCRIPTION = SITETITLE
SITELOGO = "/pics/20161206.png"
MAIN_MENU = True
MENUITEMS = [
    ('About', '/pages/about-me/'),
    ('Resume', '/cv'),
    ('Archives', '/archives.html'),
    ('Categories', '/categories.html'),
    ('Tags', '/tags.html'),
    ('RSS', '/feeds/all.atom.xml')
]
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
COLOR_SCHEME_CSS = 'tomorrow.css'
FAVICON = 'myfavicon.ico'
COPYRIGHT_YEAR = 2019
CC_LICENSE = {
    'name': 'Creative Commons Attribution',
    'version': '4.0',
    'slug': 'by'
}
#OG_LOCALE = 'zh_TW'
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
# Social widget
SOCIAL = (
    ('Github', 'https://github.com/chairco'),
    ('Twitter', 'https://twitter.com/ChaircoChen'),
    ('Email', 'mailto:chairco@gmail.com'),
    #('Google', '#'),
    #('Facebook', 'https://www.facebook.com/chairco'),
    #('RSS', 'http://chairco.me/feeds/all.atom.xml'),
    #('Linkedin', '#'),
)
SUMMARY_MAX_LENGTH = 24
DEFAULT_PAGINATION = 12
# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True


# NEST Template
THEME = 'nest'
SITESUBTITLE = u"Jason's Blog"
# Minified CSS
NEST_CSS_MINIFY = True
# Add items to top menu before pages
MENUITEMS = [
    ('About', '/pages/about-me/'),
    ('Resume', '/cv'),
    ('Categories', '/categories.html'),
    #('Archives', '/archives.html'),
    #('Tags', '/tags.html'),
    #('RSS', '/feeds/all.atom.xml')
]
# Add header background image from content/images : 'background.jpg'
NEST_HEADER_IMAGES = 'home-bg.jpg'
NEST_HEADER_LOGO = '/images/logo.png'
# Footer
NEST_SITEMAP_COLUMN_TITLE = u'Sitemap'
NEST_SITEMAP_MENU = [
    ('Archives', '/archives.html'),
    ('Tags','/tags.html'),
    #('Authors','/authors.html')
]
NEST_SITEMAP_ATOM_LINK = u'Atom Feed'
NEST_SITEMAP_RSS_LINK = u'RSS Feed'
NEST_SOCIAL_COLUMN_TITLE = u'Social'
NEST_LINKS_COLUMN_TITLE = u'Links'
NEST_COPYRIGHT = u"&copy; Jason's Blog 2018"
# Footer optional
NEST_FOOTER_HTML = ''
# index.html
NEST_INDEX_HEAD_TITLE = u'真是迷人的 Asyncio'
NEST_INDEX_HEADER_TITLE = SITETITLE
NEST_INDEX_HEADER_SUBTITLE = u'TAIWAN No.1'
NEST_INDEX_CONTENT_TITLE = u'Latest Posts'
# archives.html
NEST_ARCHIVES_HEAD_TITLE = u'Archives'
NEST_ARCHIVES_HEAD_DESCRIPTION = u'Posts Archives'
NEST_ARCHIVES_HEADER_TITLE = u'Archives'
NEST_ARCHIVES_HEADER_SUBTITLE = u'Archives for all posts'
NEST_ARCHIVES_CONTENT_TITLE = u'Archives'
# article.html
NEST_ARTICLE_HEADER_BY = u'By'
NEST_ARTICLE_HEADER_MODIFIED = u'modified'
NEST_ARTICLE_HEADER_IN = u'in category'
# author.html
NEST_AUTHOR_HEAD_TITLE = u'Posts by'
NEST_AUTHOR_HEAD_DESCRIPTION = u'Posts by'
NEST_AUTHOR_HEADER_SUBTITLE = u'Posts archives'
NEST_AUTHOR_CONTENT_TITLE = u'Posts'
# authors.html
#NEST_AUTHORS_HEAD_TITLE = u'Author list'
#NEST_AUTHORS_HEAD_DESCRIPTION = u'Author list'
#NEST_AUTHORS_HEADER_TITLE = u'Author list'
#NEST_AUTHORS_HEADER_SUBTITLE = u'Archives listed by author'
# categories.html
NEST_CATEGORIES_HEAD_TITLE = u'Categories'
NEST_CATEGORIES_HEAD_DESCRIPTION = u'Archives listed by category'
NEST_CATEGORIES_HEADER_TITLE = u'Categories'
NEST_CATEGORIES_HEADER_SUBTITLE = u'Archives listed by category'
# category.html
NEST_CATEGORY_HEAD_TITLE = u'Category Archive'
NEST_CATEGORY_HEAD_DESCRIPTION = u'Category Archive'
NEST_CATEGORY_HEADER_TITLE = u'Category'
NEST_CATEGORY_HEADER_SUBTITLE = u'Category Archive'
# pagination.html
NEST_PAGINATION_PREVIOUS = u'Previous'
NEST_PAGINATION_NEXT = u'Next'
# period_archives.html
NEST_PERIOD_ARCHIVES_HEAD_TITLE = u'Archives for'
NEST_PERIOD_ARCHIVES_HEAD_DESCRIPTION = u'Archives for'
NEST_PERIOD_ARCHIVES_HEADER_TITLE = u'Archives'
NEST_PERIOD_ARCHIVES_HEADER_SUBTITLE = u'Archives for'
NEST_PERIOD_ARCHIVES_CONTENT_TITLE = u'Archives for'
# tag.html
NEST_TAG_HEAD_TITLE = u'Tag archives'
NEST_TAG_HEAD_DESCRIPTION = u'Tag archives'
NEST_TAG_HEADER_TITLE = u'Tag'
NEST_TAG_HEADER_SUBTITLE = u'Tag archives'
# tags.html
NEST_TAGS_HEAD_TITLE = u'Tags'
NEST_TAGS_HEAD_DESCRIPTION = u'Tags List'
NEST_TAGS_HEADER_TITLE = u'Tags'
NEST_TAGS_HEADER_SUBTITLE = u'Tags List'
NEST_TAGS_CONTENT_TITLE = u'Tags List'
NEST_TAGS_CONTENT_LIST = u'tagged'
# Static files
STATIC_PATHS = ['images', 'pics', 'extra/robots.txt', 'extra/favicon.ico', 'extra/logo.svg']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'myfavicon.ico'},
    'extra/logo.svg': {'path': 'logo.svg'}
}
# Disqus
DISQUS_SITENAME = "chairco"
# Google analytics
GOOGLE_ANALYTICS = "UA-79798833-1"
# Analytics
GAUGES = False
PIWIK_URL = False
