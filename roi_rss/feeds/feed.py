from PyRSS2Gen import PyRSS2Gen
import webapp2

class Feed(webapp2.RequestHandler):
    '''RSS feed.'''
    
    def get(self):
        rss = PyRSS2Gen.RSS2(
            title=self.title,
            link=self.link,
            description=self.description,
            image=PyRSS2Gen.Image(
                url=self.image,
                title=self.title,
                link=self.link,
                description=self.description,
            ),
            items=self.get_items(),
        )
        self.response.headers['Content-Type'] = 'application/rss+xml; charset=utf-8'
        self.response.write(rss.to_xml('utf-8'))

    def get_items(self):
        raise NotImplementedError()
