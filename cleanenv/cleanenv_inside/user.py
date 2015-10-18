# FIXME 'id -Gn' lists somewhat more when special network groups are used.
import grp
import os
import pwd
import re


_pattern = r'(system:)?(?:(\d+)?:)?([^:]+)?$'


def _groups(username):
    result = []

    try:
        group = grp.getgrnam(username)
        result.append({'gid': group.gr_gid, 'name': group.gr_name})
    except KeyError:
        pass

    for group in grp.getgrall():
        for member in group.gr_mem:
            if member == username or member.endswith('+' + username):
                result.append({'gid': group.gr_gid, 'name': group.gr_name})

    return result


def username_from_config(config):
    value = config['global'].get('user')
    if not value:
        return None
    match = re.match(_pattern, value)
    if not match:
        return None
    return match.group(3)


def expand_user(config):
    """Detect username, userid and its associated groups (including group ids)
    from the user in config['global']['user']. If none is set, the current
    logged in user is used.

    Returns a dictionary with 'uid', 'name', 'system' flag and its 'groups'.
    """
    user = config['global'].get('user')

    match   = re.match(_pattern, user)
    if not match:
        raise ValueError('Invalid user: %s' % user)

    sudo     = config['global'].get('sudo', False)
    system   = bool(match.group(1))
    gid      = match.group(2)
    username = match.group(3)

    if not username:
        username = getlogin()

    if gid:
        userid = int(gid)
    else:
        try:
            userid = pwd.getpwnam(username).pw_uid
        except KeyError:
            # no such user
            userid = None

    groups = _groups(username)

    return {'name': username,
            'uid': userid,
            'system': system,
            'sudo': sudo,
            'groups': groups}


def getlogin():
    # os.getlogin() is not always working properly on all systems
    return pwd.getpwuid(getuid()).pw_name

def getuid():
    return os.geteuid()
