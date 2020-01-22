import sys

from matthuisman import plugin, userdata, inputstream, gui
from matthuisman.session import Session
from matthuisman.language import _

@plugin.route('')
def home(**kwargs):
    folder = plugin.Folder(cacheToDisc=False)

    if not userdata.get('dns4me_key'):
        folder.add_item(
            label = 'dns4me Login',
            path  = plugin.url_for(dns4me_login),
        )
    else:
        folder.add_item(
            label = 'dns4me Logout',
            path  = plugin.url_for(dns4me_logout),
        )

    folder.add_item(
        label = 'Install Widevine CDM',
        path  = plugin.url_for(ia_install),
    )

    #folder.add_item(label=_.SETTINGS, path=plugin.url_for(plugin.ROUTE_SETTINGS))

    return folder

@plugin.route()
def dns4me_login(**kwargs):
    username = gui.input('dns4me Username').strip()
    if not username:
        return

    password = gui.input('dns4me Password', hide_input=True).strip()
    if not password:
        return

    data = Session().post('https://dns4me.net/api/v2/get_apikey', data={'username': username, 'password': password}).json()
    if 'apikey' in data:
        userdata.set('dns4me_key', data['apikey'])
    else:
        plugin.exception('Failed to login')

    gui.refresh()

@plugin.route()
def dns4me_logout(**kwargs):
    if not gui.yes_no('Are you sure logout?'):
        return

    userdata.delete('dns4me_key')
    gui.refresh()

@plugin.route()
def ia_install(**kwargs):
    inputstream.install_widevine(reinstall=True)
    gui.refresh()

plugin.dispatch(sys.argv[2])