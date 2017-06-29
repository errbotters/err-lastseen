import re
from datetime import datetime
from errbot import BotPlugin, botcmd, re_botcmd


USAGE_STR = 'Nick not specified. (usage: !last_seen <nick>)'


class LastSeen(BotPlugin):

    def activate(self):
        super(LastSeen, self).activate()
        try:
            if type(self['last_seen']) is not dict:
                self['last_seen'] = {}
        except KeyError:
            self['last_seen'] = {}

    @re_botcmd(pattern=r'^', prefixed=False, flags=re.IGNORECASE)
    def update_last_seen(self, msg, match):
        user = str(msg.frm).split('!')[0]
        time = datetime.now()

        last_seens = self['last_seen']
        last_seens[user] = time
        self['last_seen'] = last_seens

    @botcmd
    def last_seen(self, msg, args):
        """Return last activity and its time of given user.

        Examples:
            !last_seen <user>
        """
        last_seens = self['last_seen']

        if len(args) < 1:
            return USAGE_STR
        user = args.split(' ')[0]

        try:
            when = last_seens[user].strftime("%d-%m-%Y %H:%M")
        except KeyError:
            return 'We have not seen {} yet.'.format(user)

        return '{} was last seen on {}.'.format(user, when)
