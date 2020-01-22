from kodi_six import xbmcgui

from . import signals, gui
from .session import Session
from .settings import Settings
from .userdata import Userdata
from .constants import COMMON_ADDON_ID, ADDON_ID
from .language import _

common_data     = Userdata(COMMON_ADDON_ID)
common_settings = Settings(COMMON_ADDON_ID)
settings        = Settings(ADDON_ID)

_window   = xbmcgui.Window(10000)

@signals.on(signals.BEFORE_DISPATCH)
def check_dns():
    key        = common_data.get('dns4me_key')
    enabled    = settings.getBool('enable_dns4me', False)
    service_id = settings.get('_dns4me_service_id')
    use_hosts  = settings.getBool('dns4me_use_hosts', True)

    if not enabled or not service_id:
        return

    if not key:
        key = login()
        if not key:
            return

    if use_hosts and not common_data.get('_dns_hosts'):
        _window.setProperty('_dns_enabled', '')

    #move this as a skin settings
    if _window.getProperty('_dns_enabled') == ADDON_ID:
        return

    with gui.progress('Enabling service in dns4me') as progress:
        #print(Session().get('https://dns4me.net/user/update_zone_api/{key}'.format(key=key)).text) #zonekeys are slightly different....

        data = Session().get('https://dns4me.net/api/v2/enable_service/{key}/{service_id}/1'.format(key=key, service_id=service_id)).json()
        if data['error']:
            return

        _window.setProperty('_dns_enabled', ADDON_ID)

        hosts = {}
        if settings.getBool('dns4me_use_hosts', True):
            for line in Session().get('https://dns4me.net/api/v2/get_hosts/hosts/{key}'.format(key=key)).text.splitlines():
                ip_addr, host = line.strip().split('\t')
                hosts[host.lower().strip()] = ip_addr.strip()

        common_data.set('_dns_hosts', hosts)

def login():
    username = gui.input('dns4me Username').strip()
    if not username:
        return

    password = gui.input('dns4me Password', hide_input=True).strip()
    if not password:
        return

    data = Session().post('https://dns4me.net/api/v2/get_apikey', data={'username': username, 'password': password}).json()
    if 'apikey' in data:
        common_data.set('dns4me_key', data['apikey'])
        return data['apikey']