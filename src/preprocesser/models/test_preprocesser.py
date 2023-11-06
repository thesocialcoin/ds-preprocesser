import unittest
from preprocesser.models import _base

#import emoji

class TestPreProcesser(unittest.TestCase):
    
    #def test_removeEmojis(self):

        #output_text = _base.removeEmojis(emoji.emojize('bon dia :sparkling_heart::sparkles:', use_palceholder=False))
        #self.assertEqual(output_text, 'bon dia')
    
    def test_removeHashtagInFrontOfWord(self):

        output_text = _base.removeHashtagInFrontOfWord('some random text with #whitebear')
        self.assertEqual(output_text[0], 'some random text with whitebear')
    
    def test_removeHtMentionsSuccessions(self):

        output_text = _base.removeHtMentionsSuccessions('some random text with @nlozano @odelgado @mribera #whitebear')
        self.assertEqual(output_text[0], 'some random text with')
    
    def test_removeNumbers(self):

        output_text = _base.removeNumbers('2023', use_placeholder=False)
        self.assertEqual(output_text[0], '')


    def test_removeStopWords(self):

        output_text = _base.removeStopWords('lo que tú digas', 'es')
        self.assertEqual(output_text[0], 'digas')

    
    def test_removeUnicode(self):

        output_text = _base.removeUnicode('what\n')
        self.assertEqual(output_text, 'what')

    
    def test_removeUrls(self):

        output_text = _base.removeUrls('some random text with https://random.url http://hello.com', use_placeholder=False)
        self.assertEqual(output_text[0].rstrip(), 'some random text with')

    
    def test_replaceMultiStopMark(self):

        output_text = _base.replaceMultiStopMark('...')
        self.assertEqual(output_text[0], '.')


    def test_replaceAtUser(self):

        output_text = _base.replaceAtUser('some random text with @nlozano @odelgado @mribera', use_placeholder=False)
        self.assertEqual(output_text[0].rstrip(), 'some random text with')

    
    def test_replaceElongated(self):

        output_text = _base.replaceElongated('YEEEEEEESSS')
        self.assertEqual(output_text[0], 'YES')

    
    def test_replaceMultiExclamationMark(self):

        output_text = _base.replaceMultiExclamationMark('!!!')
        self.assertEqual(output_text[0], '!')


    def test_replaceMultiQuestionMark(self):

        output_text = _base.replaceMultiQuestionMark('???')
        self.assertEqual(output_text[0], '?')

    
    def test_removePunctuation(self):

        output_text = _base.removePunctuation('have a good night!')
        self.assertEqual(output_text[0], 'have a good night ')

    
    def test_removeMultiWhiteSpace(self):

        output_text = _base.removeMultiWhiteSpace('what     ')
        self.assertEqual(output_text, 'what ')

    
    def test_toLower(self):

        output_text = _base.toLower('YES')
        self.assertEqual(output_text, 'yes')

    
    def test_removeTags(self):

        output_text = _base.removeTags('some random text with #whitebear', use_placeholder=False)
        self.assertEqual(output_text[0].rstrip(), 'some random text with')

    
    def test_removeNonAlphChar(self):

        output_text = _base.removeNonAlphChar('_night_')
        self.assertEqual(output_text, 'night')

