from datetime import datetime
from errbot import BotPlugin, botcmd

USAGE_STR = 'Nick not specified. (usage: !last_seen <nick>)'
CONFIG_TEMPLATE = {
    # locale-preffered format is default
    'TIME_FORMAT': '%c'
}


class LastSeen(BotPlugin):
    def configure(self, configuration):
        if configuration is not None and configuration != {}:
            config = dict(chain(CONFIG_TEMPLATE.items(),
                                configuration.items()))
        else:
            config = CONFIG_TEMPLATE
        super(LastSeen, self).configure(config)

    def get_configuration_template(self):
        return CONFIG_TEMPLATE

    def activate(self):
        super(LastSeen, self).activate()
        try:
            if type(self['last_seen']) is not dict:
                self['last_seen'] = {}
        except KeyError:
            self['last_seen'] = {}

    def callback_message(self, msg):
        user = msg.nick
        last_seens = self['last_seen']

        last_seens[user] = {}
        last_seens[user]['time'] = datetime.now()
        last_seens[user]['msg'] = msg.body

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
            time = last_seens[user]['time']
            text = last_seens[user]['msg']

            timedelta = datetime.now() - time
            if timedelta.days == 0:
                hours = timedelta.seconds // 3600
                minutes = (timedelta.seconds - (hours * 3600)) // 60

                min_format = 'minute' if minutes == 1 else 'minutes'
                if hours > 0:
                    hour_format = 'hour' if hours == 1 else 'hours'

                    params = [user, hours, hour_format, minutes, min_format,
                              text]
                    msg = '{} was last seen {} {} and {} {} ago, saying "{}".'
                    return msg.format(*params)

                params = [user, minutes, min_format, text]
                msg = '{} was last seen {} {} ago, saying "{}".'
                return msg.format(*params)

        except KeyError:
            return 'We have not seen {} yet.'.format(user)

        form = self.config['TIME_FORMAT']
        time = time.strftime(form)
        return '{} was last seen on {}, saying "{}".'.format(user, time, text)
