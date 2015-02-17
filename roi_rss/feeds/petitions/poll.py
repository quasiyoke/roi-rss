# -*- coding: utf-8 -*-

from roi_rss import feeds


class Poll(feeds.Feed):
    '''RSS feed with petitions which are on poll now.'''
    
    title = u'Инициативы РОИ на голосовании'
    link = 'https://www.roi.ru/poll/'
    description = u'Инициативы сайта Российской общественной инициативы, находящиеся в данный момент на голосовании.'
    image = '/static/img/roi.png'
    
    def get_items(self):
        return []
