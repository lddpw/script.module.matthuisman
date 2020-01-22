from urllib3.util import connection

import requests

from kodi_six import xbmc, xbmcgui

from . import userdata, settings, mem_cache
from .log import log
from .constants import ADDON_ID, COMMON_ADDON_ID

DEFAULT_HEADERS = {
    'User-Agent': xbmc.getUserAgent(),
}

_orig_create_connection = connection.create_connection

common_data = userdata.Userdata(COMMON_ADDON_ID)

class Session(requests.Session):
    def __init__(self, headers=None, cookies_key=None, base_url='{}', timeout=None, attempts=None, verify=None, hosts=None, use_hosts=True):
        super(Session, self).__init__()

        self._headers     = headers or {}
        self._cookies_key = cookies_key
        self._base_url    = base_url
        self._timeout     = timeout or settings.getInt('http_timeout', 30)
        self._attempts    = attempts or settings.getInt('http_retries', 2)
        self._verify      = verify if verify is not None else settings.getBool('verify_ssl', True)
        self._hosts       = hosts or {}
        self._use_hosts   = use_hosts

        self.headers.update(DEFAULT_HEADERS)
        self.headers.update(self._headers)

        if self._cookies_key:
            self.cookies.update(userdata.get(self._cookies_key, {}))

    def _patched_create_connection(self, address, *args, **kwargs):
        if settings.getBool('enable_dns4me', False) and xbmcgui.Window(10000).getProperty('_dns_enabled') == ADDON_ID:
            hosts = common_data.get('_dns_hosts', {})
        else:
            hosts = {}
    
        hosts.update(self._hosts)

        host, port = address
        _host = hosts.get(host.lower())
        if _host:
            log.debug('Rewrite DNS: {} > {}'.format(host, _host))
            host = _host

        return _orig_create_connection((host, port), *args, **kwargs)

    def request(self, method, url, timeout=None, attempts=None, verify=None, **kwargs):
        if not url.startswith('http'):
            url = self._base_url.format(url)

        timeout = timeout or self._timeout
        if timeout:
            kwargs['timeout'] = timeout

        kwargs['verify']  = verify or self._verify
        attempts          = attempts or self._attempts

        try:
            if self._use_hosts:
                connection.create_connection = self._patched_create_connection

            for i in range(1, attempts+1):
                log('Attempt {}/{}: {} {} {}'.format(i, attempts, method, url, kwargs if method.lower() != 'post' else ""))

                try:
                    return super(Session, self).request(method, url, **kwargs)
                except:
                    if i == attempts:
                        raise
        except:
            raise
        finally:
            connection.create_connection = _orig_create_connection

    def save_cookies(self):
        if not self._cookies_key:
            raise Exception('A cookies key needs to be set to save cookies')

        userdata.set(self._cookies_key, self.cookies.get_dict())

    def clear_cookies(self):
        if self._cookies_key:
            userdata.delete(self._cookies_key)
        self.cookies.clear()

    def chunked_dl(self, url, dst_path, method='GET', chunksize=None, **kwargs):
        kwargs['stream'] = True
        resp = self.request(method, url, **kwargs)
        resp.raise_for_status()

        with open(dst_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=chunksize or settings.getInt('chunksize', 4096)):
                f.write(chunk)