import unittest
from boston_commands import resolve_shortcut

class BostonCommandTests(unittest.TestCase):
    def test_navigation(self):
        self.assertEqual(resolve_shortcut(' /BOSTON '), 'x')
        self.assertEqual(resolve_shortcut('/neighborhood'), 'b')
        self.assertEqual(resolve_shortcut('/dispatch'), 'u')

    def test_do_not_rewrite_message_content(self):
        self.assertIsNone(resolve_shortcut('/neighborhood', {'command': 'MAIL'}))
        self.assertIsNone(resolve_shortcut('/dispatch', {'command': 'BULLETIN_POST_CONTENT'}))
        self.assertIsNone(resolve_shortcut('This is a message /boston'))
        self.assertEqual(resolve_shortcut('/help', {'command': 'MAIL'}), 'q')

if __name__ == '__main__':
    unittest.main()
