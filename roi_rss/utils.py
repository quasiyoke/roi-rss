import cgi
import httplib
import logging
import os
import google.appengine.api.urlfetch as urlfetch
from google.appengine.ext.webapp import template


APP_DIR = os.path.dirname(__file__)
LOG = logging.getLogger(__name__)


class Error(Exception):
    def __init__(self, message='', *args, **kwargs):
        super(Error, self).__init__(**kwargs)
        self.message = message.format(*args)


class HTTPNotFoundError(Error):
    '''Raised on HTTP Page Not Found error.'''


def fetch_url(url, content_type = 'text/html'):
    '''Fetches the specified URL.'''

    LOG.info('Fetching "%s"...', url)

    try:
        page = _fetch_url(url, headers = { 'Accept-Language': 'ru,en' })
    except urlfetch.Error as e:
        raise Error('Failed to fetch the page: {0}.', e)
    else:
        if page.status_code == httplib.OK:
            LOG.info('"%s" has been successfully fetched.', url)
        else:
            error_class = HTTPNotFoundError if page.status_code == httplib.NOT_FOUND else Error
            raise error_class('The server returned error: {0} ({1}).',
                httplib.responses.get(page.status_code, 'Unknown error'), page.status_code)

    content = page.content

    for key in page.headers:
        if key.lower() == 'content-type':
            value, params = cgi.parse_header(page.headers[key])

            if value != content_type:
                LOG.warning('The server returned a page with invalid content type: {0}.', value)

            if content_type.startswith('text/'):
                for param in params:
                    if param.lower() == 'charset':
                        content_encoding = params[param]
                        break
                else:
                    content_encoding = 'UTF-8'

                try:
                    content = content.decode(content_encoding)
                except UnicodeDecodeError:
                    raise Error('The server returned a page in invalid encoding.')

            break
    else:
        LOG.warning('The server returned a page with missing content type.')

    return content


def _fetch_url(*args, **kwargs):
    '''
    Sometimes urlfetch.fetch() raises weird error 'ApplicationError: 5' when it
    shouldn't. So this wrapper ignores errors and tries to fetch the URL again.

    @throws urlfetch.Error
    '''

    tries = 3

    while True:
        try:
            return urlfetch.fetch(*args, **kwargs)
        except urlfetch.Error as e:
            if tries <= 1:
                raise e
            tries -= 1


def render_template(name, context={}):
    return template.render(os.path.join(APP_DIR, 'templates', name), context)
