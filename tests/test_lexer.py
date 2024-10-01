import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Lexer import Lexer, TokenType

class TestLexer(unittest.TestCase):
    
    def testEmptyInputNumberOfTokens(self):
        lexer = Lexer('')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 0)

    def testEmptyInputTokenType(self):
        lexer = Lexer('')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.EOF)

    def testEmptyInputText(self):
        lexer = Lexer('')
        token = lexer.getToken()
        self.assertEqual(token.text, '')

    def testNewLineInputNumberOfTokens(self):
        lexer = Lexer('\n')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testNewLineInputTokenType(self):
        lexer = Lexer('\n')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.NLN)

    def testNewLineInputText(self):
        lexer = Lexer('\n')
        token = lexer.getToken()
        self.assertEqual(token.text, '\n')

    def testWhiteSpaceInputNumberOfTokens(self):
        lexer = Lexer(' ')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 0)

    def testWhiteSpaceInputTokenType(self):
        lexer = Lexer(' ')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.WSP)

    def testWhiteSpaceInputText(self):
        lexer = Lexer(' ')
        token = lexer.getToken()
        self.assertEqual(token.text, ' ')

    def testSingleLineCommentTokenInputNumberOfTokens(self):
        lexer = Lexer('--')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 0)

    def testCompleteSingleLineCommentInputNumberOfTokens(self):
        lexer = Lexer('-- foo bar')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 0)
    
    def testNoSpaceSingleLineCommentInputNumberOfTokens(self):
        lexer = Lexer('--foobar')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 0)

    def testSingleLineCommentInputTokenType(self):
        lexer = Lexer('--')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.COM)

    def testCompleteSingleLineCommentInputTokenType(self):
        lexer = Lexer('-- foo bar')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.COM)

    def testSingleLineCommentInputText(self):
        lexer = Lexer('--')
        token = lexer.getToken()
        self.assertEqual(token.text, '--')

    def testCompleteSingleLineTokenCommentInputText(self):
        lexer = Lexer('-- foo bar')
        token = lexer.getToken()
        self.assertEqual(token.text, '-- foo bar')

if __name__ == "__main__":
    pass