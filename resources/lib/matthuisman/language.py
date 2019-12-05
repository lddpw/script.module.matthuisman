from kodi_six import xbmcaddon

from .log import log
from .constants import ADDON, COMMON_ADDON

def format_string(string, _bold=False, _label=False, _color=None, _strip=False, **kwargs):
    if kwargs:
        string = string.format(**kwargs)

    if _strip:
        string = string.strip()

    if _label:
        _bold = True
        string = u'~ {} ~'.format(string)

    if _bold:
        string = u'[B]{}[/B]'.format(string)

    if _color:
        string = u'[COLOR {}]{}[/COLOR]'.format(_color, string)
        
    return string

def addon_string(id, addon=ADDON):
    string = addon.getLocalizedString(id)
    
    if not string:
        log.warning("LANGUAGE: Addon didn't return a string for id: {}".format(id))
        string = str(id)

    return string

class BaseLanguage(object):
    PLUGIN_LOGIN_REQUIRED       = 30000
    PLUGIN_NO_DEFAULT_ROUTE     = 30001
    PLUGIN_RESET_YES_NO         = 30002
    PLUGIN_RESET_OK             = 30003
    PLUGIN_CACHE_REMOVED        = 30004
    PLUGIN_CONTEXT_CLEAR_CACHE  = 30005
    ROUTER_NO_FUNCTION          = 30006
    ROUTER_NO_URL               = 30007
    IA_NOT_FOUND                = 30008
    IA_UWP_ERROR                = 30009
    IA_KODI18_REQUIRED          = 30010
    IA_AARCH64_ERROR            = 30011
    IA_NOT_SUPPORTED            = 30012
    NO_BRIGHTCOVE_SRC           = 30013
    IA_DOWNLOADING_FILE         = 30014
    IA_WIDEVINE_DRM             = 30015
    IA_ERROR_INSTALLING         = 30016
    USE_CACHE                   = 30017
    INPUTSTREAM_SETTINGS        = 30018
    CLEAR_DATA                  = 30019
    PLUGIN_ERROR                = 30020
    INSTALL_WV_DRM              = 30021
    IA_WV_INSTALL_OK            = 30022
    USE_IA_HLS                  = 30023
    LOGIN                       = 30024
    LOGOUT                      = 30025
    SETTINGS                    = 30026
    LOGOUT_YES_NO               = 30027
    LOGIN_ERROR                 = 30028
    SEARCH                      = 30029
    SEARCH_FOR                  = 30030
    NO_RESULTS                  = 30031
    PLUGIN_EXCEPTION            = 30032
    ERROR_DOWNLOADING_FILE      = 30033
    GENERAL                     = 30034
    PLAYBACK                    = 30035
    ADVANCED                    = 30036
    VERIFY_SSL                  = 30037
    SELECT_IA_VERSION           = 30038
    SERVICE_DELAY               = 30039
    MD5_MISMATCH                = 30040
    NO_ITEMS                    = 30041
    MULTI_PERIOD_WARNING        = 30042
    QUALITY_BEST                = 30043
    HTTP_TIMEOUT                = 30044
    HTTP_RETRIES                = 30045
    CHUNKSIZE                   = 30046
    WV_LATEST                   = 30047
    QUALITY_SKIP                = 30048
    NO_AUTOPLAY_FOUND           = 30049
    CONFIRM_MIGRATE             = 30050
    MIGRATE_OK                  = 30051
    NO_ERROR_MSG                = 30052
    MULTI_BASEURL_WARNING       = 30053
    QUALITY_CUSTOM              = 30054
    QUALITY_ASK                 = 30055
    QUALITY_PARSE_ERROR         = 30056
    QUALITY_BAD_M3U8            = 30057
    WV_INSTALLED                = 30058
    MAX_BANDWIDTH               = 30059
    QUALITY_LOWEST              = 30060
    PLAYBACK_QUALITY            = 30061
    PLAY_DEFAULT_ACTION         = 30062
    PLAY_FROM_START             = 30063
    PLAY_FROM_LIVE              = 30064
    PLAY_FROM_ASK               = 30065
    PLAY_FROM                   = 30066
    QUALITY_BITRATE             = 30067
    QUALITY_FPS                 = 30068
    SELECT_WV_VERSION           = 30069
    WV_UNKNOWN                  = 30070
    WV_NOT_LATEST               = 30071
    DISABLED                    = 30072
    QUALITY_HTTP_ERROR          = 30073
    IA_ANDROID_REINSTALL        = 30074

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if not isinstance(attr, int):
            return attr

        if hasattr(BaseLanguage, name):
            addon = COMMON_ADDON
        else:
            addon = ADDON

        return addon_string(attr, addon)

    def __call__(self, string, **kwargs):
        return format_string(string, **kwargs)

_ = BaseLanguage()