''' This package is for user managing in wechat mp
 1. What can we do?
    - set tags and everything around them
    - get all your users (of course not at a time) or get detailed information of one
    - set blacklist and everything around it

 3. I alse listed API list for you:
   - TAGS
     create_tag
     get_tags
     update_tag
     delete_tag
     get_users_of_tag
     add_users_into_tag
     delete_users_of_tag
     get_tags_of_user
   - USER INFO
     get_users
     get_user_info
     set_alias
   - BLACKLIST
     get_blacklist
     add_users_into_blacklist
     delete_users_of_blacklist
'''
import logging

from .requests import requests
from .common import access_token
from itchatmp.utils import retry, encode_send_dict
from itchatmp.content import (SERVER_URL,
    IMAGE, VOICE, VIDEO, MUSIC, TEXT, NEWS, CARD)
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')

def create_tag(name):
    @retry(n=3, waitTime=3)
    @access_token
    def _create_tag(name, accessToken=None):
        data = encode_send_dict({'tag': {'name': name}})
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/cgi-bin/tags/create?access_token=%s'
            % (SERVER_URL, accessToken), data=data).json()
        if 'tag' in r: r['errcode'] = 0
        return ReturnValue(r)
    return _create_tag(name)

def get_tags():
    @retry(n=3, waitTime=3)
    @access_token
    def _get_tags(accessToken=None):
        r = requests.get('%s/cgi-bin/tags/get?access_token=%s'
            % (SERVER_URL, accessToken)).json()
        if 'tags' in r: r['errcode'] = 0
        return ReturnValue(r)
    return _get_tags()

def update_tag(id, name):
    @retry(n=3, waitTime=3)
    @access_token
    def _update_tag(id, name, accessToken=None):
        data = encode_send_dict({'tag': {'name': name, 'id': id}})
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/cgi-bin/tags/update?access_token=%s'
            % (SERVER_URL, accessToken), data=data).json()
        return ReturnValue(r)
    return _update_tag(id, name)

def delete_tag(id):
    @retry(n=3, waitTime=3)
    @access_token
    def _delete_tag(id, accessToken=None):
        data = encode_send_dict({'tag': {'id': id}})
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/cgi-bin/tags/delete?access_token=%s'
            % (SERVER_URL, accessToken), data=data).json()
        return ReturnValue(r)
    return _delete_tag(id)

def get_users_of_tag(id, nextOpenId=''):
    @retry(n=3, waitTime=3)
    @access_token
    def _get_users_of_tag(id, nextOpenId, accessToken=None):
        data = encode_send_dict({'tagid': id, 'next_openid': nextOpenId})
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/cgi-bin/tag/get?access_token=%s'
            % (SERVER_URL, accessToken), data=data).json()
        if 'count' in r: r['errcode'] = 0
        return ReturnValue(r)
    return _get_users_of_tag(id, nextOpenId)

def add_users_into_tag(id, userIdList):
    @retry(n=3, waitTime=3)
    @access_token
    def _add_users_into_tag(id, userIdList, accessToken=None):
        data = encode_send_dict({'openid_list': userIdList, 'tagid': id})
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/cgi-bin/tags/members/batchtagging?access_token=%s'
            % (SERVER_URL, accessToken), data=data).json()
        return ReturnValue(r)
    return _add_users_into_tag(id, userIdList)

def delete_users_of_tag(id, userIdList):
    @retry(n=3, waitTime=3)
    @access_token
    def _delete_users_of_tag(id, userIdList, accessToken=None):
        data = encode_send_dict({'tagid': id, 'openid_list': userIdList})
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/cgi-bin/tags/members/batchuntagging?access_token=%s'
            % (SERVER_URL, accessToken), data=data).json()
        return ReturnValue(r)
    return _delete_users_of_tag(id, userIdList)

def get_tags_of_user(userId):
    @retry(n=3, waitTime=3)
    @access_token
    def _get_tags_of_user(userId, accessToken=None):
        data = encode_send_dict({'openid': userId})
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/cgi-bin/tags/getidlist?access_token=%s'
            % (SERVER_URL, accessToken), data=data).json()
        if 'tagid_list' in r: r['errcode'] = 0
        return ReturnValue(r)
    return _get_tags_of_user(userId)

def set_alias(userId, alias):
    ''' this method is for verified service mp only '''
    @retry(n=3, waitTime=3)
    @access_token
    def _set_alias(userId, alias, accessToken=None):
        data = encode_send_dict({'openid': userId, 'remark': alias})
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/cgi-bin/user/info/updateremark?access_token=%s'
            % (SERVER_URL, accessToken), data=data).json()
        return ReturnValue(r)
    return _set_alias(userId, alias)

def get_user_info(userId):
    @retry(n=3, waitTime=3)
    @access_token
    def _batch_get_user_info(userId, accessToken=None):
        data = {'user_list': [{'openid': id, 'lang': 'zh-CN'} for id in userId]}
        data = encode_send_dict(data)
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/cgi-bin/user/info/batchget?access_token=%s'
            % (SERVER_URL, accessToken), data=data).json()
        if 'user_info_list' in r: r['errcode'] = 0
        return ReturnValue(r)
    @retry(n=3, waitTime=3)
    @access_token
    def _get_user_info(userId, accessToken=None):
        params = {
            'access_token': accessToken,
            'openid': userId,
            'lang': 'zh_CN', }
        r = requests.get('%s/cgi-bin/user/info' % SERVER_URL, params=params).json()
        if 'openid' in r: r['errcode'] = 0
        return ReturnValue(r)
    if isinstance(userId, list):
        return _batch_get_user_info(userId)
    else:
        return _get_user_info(userId)

def get_users(nextOpenId=''):
    @retry(n=3, waitTime=3)
    @access_token
    def _get_users(nextOpenId, accessToken=None):
        params = {
            'access_token': accessToken,
            'next_openid': nextOpenId, }
        r = requests.get('%s/cgi-bin/user/get' % SERVER_URL, params=params).json()
        if 'data' in r: r['errcode'] = 0
        return ReturnValue(r)
    return _get_users(nextOpenId)

def get_blacklist(beginOpenId=''):
    @retry(n=3, waitTime=3)
    @access_token
    def _get_blacklist(beginOpenId, accessToken=None):
        data = {'begin_openid': beginOpenId}
        data = encode_send_dict(data)
        r = requests.post('%s/cgi-bin/tags/members/getblacklist?access_token=%s' % 
            (SERVER_URL, accessToken), data=data).json()
        if 'data' in r: r['errcode'] = 0
        return ReturnValue(r)
    return _get_blacklist(beginOpenId)

def add_users_into_blacklist(userId):
    ''' userId can be a userId or a list of userId '''
    if not isinstance(userId, list): userId = [userId]
    @retry(n=3, waitTime=3)
    @access_token
    def _add_users_into_blacklist(userId, accessToken=None):
        data = {'openid_list': userId}
        data = encode_send_dict(data)
        r = requests.post('%s/cgi-bin/tags/members/batchblacklist?access_token=%s' % 
            (SERVER_URL, accessToken), data=data).json()
        return ReturnValue(r)
    return _add_users_into_blacklist(userId)

def delete_users_of_blacklist(userId):
    ''' userId can be a userId or a list of userId '''
    if not isinstance(userId, list): userId = [userId]
    @retry(n=3, waitTime=3)
    @access_token
    def _delete_users_of_blacklist(userId, accessToken=None):
        data = {'openid_list': userId}
        data = encode_send_dict(data)
        r = requests.post('%s/cgi-bin/tags/members/batchunblacklist?access_token=%s' % 
            (SERVER_URL, accessToken), data=data).json()
        return ReturnValue(r)
    return _delete_users_of_blacklist(userId)
