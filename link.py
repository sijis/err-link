import logging
from datetime import datetime

from errbot import botcmd, BotPlugin

log = logging.getLogger(name='errbot.plugins.Link')

class Link(BotPlugin):

    @botcmd(split_args_with=' ')
    def link(self, msg, args):
        """ Return link """

        key = str(args.pop(0))

        if key is '':
            self.send(msg.frm, 'link for what?', message_type=msg.type)
            return

        log.debug('{0} requested link for {1}'.format(msg.frm, key))

        try:
            link_key = self.shelf[key]
            self.send(msg.frm, link_key['url'], message_type=msg.type)
        except KeyError:
            self.send(msg.frm, 'I have no link for {0}'.format(key), message_type=msg.type)

        return

    @botcmd(split_args_with=' ')
    def link_add(self, msg, args):
        """ Add or updates a link """

        if len(args) != 2:
            self.send(msg.frm, 'Wrong number of arguments. You need 2.', message_type=msg.type)

        key = str(args.pop(0))
        link = args.pop(0)

        self.shelf[key] = {
            'updated': datetime.now(),
            'url': link,
        }
        self.shelf.sync()

    @botcmd(split_args_with=' ')
    def link_delete(self, msg, args):
        """ Delete link """
        try:
            link_key = str(args.pop(0))
            del self.shelf[link_key]
            self.shelf.sync()
            self.send(msg.frm, 'Successfully deleted "{0}"'.format(link_key), message_type=msg.type)
        except KeyError:
            self.send(msg.frm, 'I have no record of {0}'.format(link_key), message_type=msg.type)

        return

    @botcmd
    def link_list(self, msg, args):
        key_list = []
        for key in self.shelf.keys():
            key_list.append(key)
        self.send(msg.frm, 'Available keys: {0}'.format(','.join(key_list)), message_type=msg.type)
