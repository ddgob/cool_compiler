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

    def testDigitInputNumberOfTokens(self):
        lexer = Lexer('1')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testDigitInputTokenType(self):
        lexer = Lexer('1')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.NUM)

    def testDigitInputText(self):
        lexer = Lexer('1')
        token = lexer.getToken()
        self.assertEqual(token.text, '1')

    def testMultiDigitInputNumberOfTokens(self):
        lexer = Lexer('123')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testMultiDigitInputTokenType(self):
        lexer = Lexer('123')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.NUM)

    def testMultiDigitInputText(self):
        lexer = Lexer('123')
        token = lexer.getToken()
        self.assertEqual(token.text, '123')

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

    def testBlockCommentTokenInputNumberOfTokens(self):
        lexer = Lexer('**')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 0)

    def testCompleteBlockCommentInputNumberOfTokens(self):
        lexer = Lexer('* foo bar *')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 0)
    
    def testNoSpaceBlockCommentInputNumberOfTokens(self):
        lexer = Lexer('*foobar*')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 0)

    def testBlockCommentInputTokenType(self):
        lexer = Lexer('**')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.COM)

    def testCompleteBlockCommentInputTokenType(self):
        lexer = Lexer('* foo bar *')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.COM)

    def testBlockCommentInputText(self):
        lexer = Lexer('**')
        token = lexer.getToken()
        self.assertEqual(token.text, '**')

    def testCompleteBlockTokenCommentInputText(self):
        lexer = Lexer('* foo bar *')
        token = lexer.getToken()
        self.assertEqual(token.text, '* foo bar *')

    def testAddInputNumberOfTokens(self):
        lexer = Lexer('+')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testAddInputTokenType(self):
        lexer = Lexer('+')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.ADD)

    def testAddInputText(self):
        lexer = Lexer('+')
        token = lexer.getToken()
        self.assertEqual(token.text, '+')

    def testAddAndCommentAndNewLineInput(self):
        lexer = Lexer('+ -- foo bar\n')
        tokens = [token for token in lexer.tokens()]
        self.assertEqual(tokens[0].kind, TokenType.ADD)
        self.assertEqual(tokens[1].kind, TokenType.NLN)
        self.assertEqual(tokens[0].text, '+')
        self.assertEqual(tokens[1].text, '\n')
    
    def testAddAndCommentAndNewLineInvertedInput(self):
        lexer = Lexer('-- foo bar\n +')
        tokens = [token for token in lexer.tokens()]
        self.assertEqual(tokens[0].kind, TokenType.NLN)
        self.assertEqual(tokens[1].kind, TokenType.ADD)
        self.assertEqual(tokens[0].text, '\n')
        self.assertEqual(tokens[1].text, '+')

    def testSubtractionInputNumberOfTokens(self):
        lexer = Lexer('-')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testSubtractionInputTokenType(self):
        lexer = Lexer('-')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.SUB)

    def testSubtractionInputText(self):
        lexer = Lexer('-')
        token = lexer.getToken()
        self.assertEqual(token.text, '-')

    def testMultiplicationInputNumberOfTokens(self):
        lexer = Lexer('*')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testMultiplicationInputTokenType(self):
        lexer = Lexer('*')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.MUL)

    def testMultiplicationInputText(self):
        lexer = Lexer('*')
        token = lexer.getToken()
        self.assertEqual(token.text, '*')

    def testMultiplicationAndBlockCommentAndWhiteSpaceInputNumberOfTokens(self):
        lexer = Lexer('** *')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testMultiplicationAndBlockCommentAndWhiteSpaceInputTokenType(self):
        lexer = Lexer('** *')
        token1 = lexer.getToken()
        token2 = lexer.getToken()
        token3 = lexer.getToken()
        self.assertEqual(token1.kind, TokenType.COM)
        self.assertEqual(token2.kind, TokenType.WSP)
        self.assertEqual(token3.kind, TokenType.MUL)

    def testMultiplicationAndCommentAndWhiteSpaceInputText(self):
        lexer = Lexer('* foo bar * *')
        token1 = lexer.getToken()
        token2 = lexer.getToken()
        token3 = lexer.getToken()
        self.assertEqual(token1.text, '* foo bar *')
        self.assertEqual(token2.text, ' ')
        self.assertEqual(token3.text, '*')

    def testDivisionInputNumberOfTokens(self):
        lexer = Lexer('/')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testDivisionInputTokenType(self):
        lexer = Lexer('/')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.DIV)

    def testDivisionInputText(self):
        lexer = Lexer('/')
        token = lexer.getToken()
        self.assertEqual(token.text, '/')

    def testLessEqualInputNumberOfTokens(self):
        lexer = Lexer('<=')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testLessEqualInputTokenType(self):
        lexer = Lexer('<=')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.LEQ)

    def testLessEqualInputText(self):
        lexer = Lexer('<=')
        token = lexer.getToken()
        self.assertEqual(token.text, '<=')

    def testLessThanInputNumberOfTokens(self):
        lexer = Lexer('<')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testLessThanInputTokenType(self):
        lexer = Lexer('<')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.LTH)

    def testLessThanInputText(self):
        lexer = Lexer('<')
        token = lexer.getToken()
        self.assertEqual(token.text, '<')

    def testMinusInputNumberOfTokens(self):
        lexer = Lexer('~')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testMinusThanInputTokenType(self):
        lexer = Lexer('~')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.NEG)

    def testMinusThanInputText(self):
        lexer = Lexer('~')
        token = lexer.getToken()
        self.assertEqual(token.text, '~')

    def testNotInputNumberOfTokens(self):
        lexer = Lexer('!')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testNotThanInputTokenType(self):
        lexer = Lexer('!')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.NOT)

    def testNotThanInputText(self):
        lexer = Lexer('!')
        token = lexer.getToken()
        self.assertEqual(token.text, '!')

    def testTrueInputNumberOfTokens(self):
        lexer = Lexer('true')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testTrueThanInputTokenType(self):
        lexer = Lexer('true')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.TRU)

    def testTrueThanInputText(self):
        lexer = Lexer('true')
        token = lexer.getToken()
        self.assertEqual(token.text, 'true')

    def testFalseInputNumberOfTokens(self):
        lexer = Lexer('false')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testFalseThanInputTokenType(self):
        lexer = Lexer('false')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.FLS)

    def testFalseThanInputText(self):
        lexer = Lexer('false')
        token = lexer.getToken()
        self.assertEqual(token.text, 'false')

if __name__ == "__main__":
    pass