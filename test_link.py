import link
from errbot.backends.test import testbot
from errbot import plugin_manager


class TestLink(object):
    extra_plugin_dir = '.'

    def test_link_add(self, testbot):
        testbot.push_message('!link add github http://github.com')
        assert 'Successfully added "github"' in testbot.pop_message()

    def test_link_available(self, testbot):
        self.test_link_add(testbot)
        testbot.push_message('!link github')
        assert 'http://github.com' in testbot.pop_message()

    def test_link_delete(self, testbot):
        self.test_link_add(testbot)
        testbot.push_message('!link delete github')
        assert 'Successfully deleted "github"' in testbot.pop_message()

    def test_link_list(self, testbot):
        self.test_link_add(testbot)
        testbot.push_message('!link list')
        assert 'Available keys: github' in testbot.pop_message()

    def test_link_add_fail(self, testbot):
        testbot.push_message('!link add wrong_args')
        assert 'Wrong number of arguments. You need 2.' in testbot.pop_message()

    def test_link_fail(self, testbot):
        testbot.push_message('!link notfound')
        assert 'I have no link for notfound' in testbot.pop_message()

    def test_link_delete_fail(self, testbot):
        testbot.push_message('!link delete notfound')
        assert 'I have no record of notfound' in testbot.pop_message()
