import unittest
from preprocesser.models import _base


class TestPreProcesser(unittest.TestCase):

    def test_removeHashtagInFrontOfWord(self):
        text = 'some random text with #whitebear'
        expected_text = 'some random text with whitebear'
        output_text, _ = _base.removeHashtagInFrontOfWord(text)
        self.assertEqual(output_text, expected_text)

    def test_removeHtMentionsSuccessions(self):
        text = 'some random text with @nlozano @odelgado @mribera #whitebear'
        expected_text = 'some random text with'
        output_text, _ = _base.removeHtMentionsSuccessions(text)
        self.assertEqual(output_text, expected_text)

    def test_removeNumbers(self):
        text = '2023'
        expected_text = ''
        output_text, _ = _base.removeNumbers(text, use_placeholder=False)
        self.assertEqual(output_text, expected_text)

    def test_removeStopWords(self):
        text = 'lo que tú digas'
        output_text = _base.removeStopWords(text, 'es')
        self.assertEqual(output_text[0], 'digas')

    def test_removeUnicode(self):
        text = 'what\n'
        expected_text = 'what'
        output_text = _base.removeUnicode(text)
        self.assertEqual(output_text, expected_text)

    def test_removeUrls(self):
        text = 'some random text with https://random.url http://hello.com'
        expected_text = 'some random text with'
        output_text, _ = _base.removeUrls(text, use_placeholder=False)
        self.assertEqual(output_text[0].strip(), expected_text)

    def test_replaceMultiStopMark(self):
        text = '...'
        expected_text = '.'
        output_text, _ = _base.replaceMultiStopMark(text)
        self.assertEqual(output_text, expected_text)

    def test_replaceAtUser(self):
        text = 'some random text with @nlozano @odelgado @mribera'
        expected_text = 'some random text with'
        output_text, _ = _base.replaceAtUser(text, use_placeholder=False)
        self.assertEqual(output_text.strip(), expected_text)

    def test_replaceElongated(self):
        text = 'YEEEEEEESSS'
        expected_text = 'YES'
        output_text, _ = _base.replaceElongated(text)
        self.assertEqual(output_text, expected_text)

    def test_replaceMultiExclamationMark(self):
        text = '!!!'
        expected_text = '!'
        output_text, _ = _base.replaceMultiExclamationMark(text)
        self.assertEqual(output_text, expected_text)

    def test_replaceMultiQuestionMark(self):
        text = '???'
        expected_text = '?'
        output_text, _ = _base.replaceMultiQuestionMark(text)
        self.assertEqual(output_text, expected_text)

    def test_removePunctuation(self):
        text = 'have a good night!'
        expected_text = 'have a good night '
        output_text,  = _base.removePunctuation(text)
        self.assertEqual(output_text, expected_text)

    def test_removeMultiWhiteSpace(self):
        text = 'what     '
        expected_text = 'what '
        output_text = _base.removeMultiWhiteSpace(text)
        self.assertEqual(output_text, expected_text)

    def test_toLower(self):
        text = 'YES'
        expected_text = 'yes'
        output_text = _base.toLower(text)
        self.assertEqual(output_text, expected_text)

    def test_removeTags(self):
        text = 'some random text with #whitebear'
        expected_text = 'some random text with'
        output_text, _ = _base.removeTags(text, use_placeholder=False)
        self.assertEqual(output_text[0].strip(), expected_text)

    def test_removeNonAlphChar(self):
        text = '_night_'
        expected_text = 'night'
        output_text = _base.removeNonAlphChar(text)
        self.assertEqual(output_text, expected_text)
