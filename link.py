import logging
from datetime import datetime

from errbot import botcmd, BotPlugin

log = logging.getLogger(name='errbot.plugins.Link')


class Link(BotPlugin):

    @botcmd(split_args_with=' ')
    def link(self, msg, args):
        ''' Return link
            example:
            !link google
        '''

        key = str(args.pop(0))

        if key is '':
            return 'link for what?'

        log.debug('{0} requested link for {1}'.format(msg.frm, key))

        try:
            link_key = self[key]
            msg = link_key['url']
        except KeyError:
            msg = 'I have no link for {0}'.format(key)
        return msg

    @botcmd(split_args_with=' ')
    def link_add(self, msg, args):
        ''' Add or updates a link
            example:
            !link add google http://google.com
        '''

        if len(args) != 2:
            return 'Wrong number of arguments. You need 2.'

        key = str(args.pop(0))
        link = str(args.pop(0))

        self[key] = {
            'updated': datetime.now(),
            'url': link,
        }
        return 'Successfully added "{0}"'.format(key)

    @botcmd(split_args_with=' ')
    def link_delete(self, msg, args):
        ''' Delete link
            example:
            !link delete google
        '''
        try:
            link_key = str(args.pop(0))
            del self[link_key]
            msg = 'Successfully deleted "{0}"'.format(link_key)
        except KeyError:
            msg = 'I have no record of {0}'.format(link_key)

        return msg

    @botcmd
    def link_list(self, msg, args):
        ''' List all available links
            example:
            !link list
        '''
        key_list = []

        for key in self.keys():
            key_list.append(key)

        return 'Available keys: {0}'.format(', '.join(key_list))
