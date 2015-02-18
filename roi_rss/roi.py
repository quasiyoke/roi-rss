'''Roi API processing.'''

import json
import logging

from . import utils

LOG = logging.getLogger(__name__)
ROI_API_URL_PETITIONS_PATTERN = 'https://www.roi.ru/api/petitions/%s.json'

__all__ = ['ApiError', 'ConnectionError', 'get_petitions', ]


class ApiError(utils.Error):
    '''Raised when Roi server is failed to respond us.'''

    def __init__(self, code, *args, **kwargs):
        super(ApiError, self).__init__(*args, **kwargs)
        self.code = code


class ConnectionError(utils.Error):
    '''Raised when we fail to take data from server.'''


def fetch_api(url):
    '''
    @throws ConnectionError
    @throws Error
    '''
    try:
        data = utils.fetch_url(url, content_type='application/json')
    except Exception as e:
        raise ConnectionError('API call for petitions {0} failed: {1}', url, e)
    try:
        data = json.loads(data)
    except Exception as e:
        raise utils.Error('Failed to parse Roi API response: {0}', e)
    try:
        data = data['data']
    except KeyError:
        raise utils.Error('API response for {0} doesn\'t have "data" key', url)
    return data


def get_petitions(actuality):
    '''
    @param actuality str "poll", "advisement", "complete" or "archive".

    @throws ConnectionError
    @throws Error
    '''
    return fetch_api(ROI_API_URL_PETITIONS_PATTERN % actuality)
