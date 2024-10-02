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
        lexer = Lexer('(**)')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 0)

    def testCompleteBlockCommentInputNumberOfTokens(self):
        lexer = Lexer('(* foo bar *)')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 0)
    
    def testNoSpaceBlockCommentInputNumberOfTokens(self):
        lexer = Lexer('(*foobar*)')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 0)

    def testBlockCommentInputTokenType(self):
        lexer = Lexer('(**)')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.COM)

    def testCompleteBlockCommentInputTokenType(self):
        lexer = Lexer('(* foo bar *)')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.COM)

    def testBlockCommentInputText(self):
        lexer = Lexer('(**)')
        token = lexer.getToken()
        self.assertEqual(token.text, '(**)')

    def testCompleteBlockTokenCommentInputText(self):
        lexer = Lexer('(* foo bar *)')
        token = lexer.getToken()
        self.assertEqual(token.text, '(* foo bar *)')

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
        self.assertEqual(tokens[0].text, '+')
    
    def testAddAndCommentAndNewLineInvertedInput(self):
        lexer = Lexer('-- foo bar\n +')
        tokens = [token for token in lexer.tokens()]
        self.assertEqual(tokens[0].kind, TokenType.ADD)
        self.assertEqual(tokens[0].text, '+')

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
        lexer = Lexer('(**) *')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testMultiplicationAndBlockCommentAndWhiteSpaceInputTokenType(self):
        lexer = Lexer('(**) *')
        token1 = lexer.getToken()
        token2 = lexer.getToken()
        token3 = lexer.getToken()
        self.assertEqual(token1.kind, TokenType.COM)
        self.assertEqual(token2.kind, TokenType.WSP)
        self.assertEqual(token3.kind, TokenType.MUL)

    def testMultiplicationAndCommentAndWhiteSpaceInputText(self):
        lexer = Lexer('(* foo bar *) *')
        token1 = lexer.getToken()
        token2 = lexer.getToken()
        token3 = lexer.getToken()
        self.assertEqual(token1.text, '(* foo bar *)')
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

    def testLeftParenthesesInputNumberOfTokens(self):
        lexer = Lexer('(')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testLeftParenthesesThanInputTokenType(self):
        lexer = Lexer('(')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.LPR)

    def testLeftParenthesesThanInputText(self):
        lexer = Lexer('(')
        token = lexer.getToken()
        self.assertEqual(token.text, '(')

    def testRightParenthesesInputNumberOfTokens(self):
        lexer = Lexer(')')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testRightParenthesesThanInputTokenType(self):
        lexer = Lexer(')')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.RPR)

    def testRightParenthesesThanInputText(self):
        lexer = Lexer(')')
        token = lexer.getToken()
        self.assertEqual(token.text, ')')

    def testTeacherExample1TokenType(self):
        lexer = Lexer('1+2\n')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.NUM)
        self.assertEqual(tokens[1].kind, TokenType.ADD)
        self.assertEqual(tokens[2].kind, TokenType.NUM)
        self.assertEqual(tokens[3].kind, TokenType.NLN)

    def testTeacherExample1Text(self):
        lexer = Lexer('1+2\n')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].text, '1')
        self.assertEqual(tokens[1].text, '+')
        self.assertEqual(tokens[2].text, '2')
        self.assertEqual(tokens[3].text, '\n')

    def testTeacherExample2TokenType(self):
        lexer = Lexer('1 + 21 - 3 / 4\n~3 + 2 <= 2 * 4\n')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.NUM)
        self.assertEqual(tokens[1].kind, TokenType.ADD)
        self.assertEqual(tokens[2].kind, TokenType.NUM)
        self.assertEqual(tokens[3].kind, TokenType.SUB)
        self.assertEqual(tokens[4].kind, TokenType.NUM)
        self.assertEqual(tokens[5].kind, TokenType.DIV)
        self.assertEqual(tokens[6].kind, TokenType.NUM)
        self.assertEqual(tokens[7].kind, TokenType.NLN)
        self.assertEqual(tokens[8].kind, TokenType.NEG)
        self.assertEqual(tokens[9].kind, TokenType.NUM)
        self.assertEqual(tokens[10].kind, TokenType.ADD)
        self.assertEqual(tokens[11].kind, TokenType.NUM)
        self.assertEqual(tokens[12].kind, TokenType.LEQ)
        self.assertEqual(tokens[13].kind, TokenType.NUM)
        self.assertEqual(tokens[14].kind, TokenType.MUL)
        self.assertEqual(tokens[15].kind, TokenType.NUM)
        self.assertEqual(tokens[16].kind, TokenType.NLN)

    def testTeacherExample2Text(self):
        lexer = Lexer('1 + 21 - 3 / 4\n~3 + 2 <= 2 * 4\n')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].text, '1')
        self.assertEqual(tokens[1].text, '+')
        self.assertEqual(tokens[2].text, '21')
        self.assertEqual(tokens[3].text, '-')
        self.assertEqual(tokens[4].text, '3')
        self.assertEqual(tokens[5].text, '/')
        self.assertEqual(tokens[6].text, '4')
        self.assertEqual(tokens[7].text, '\n')
        self.assertEqual(tokens[8].text, '~')
        self.assertEqual(tokens[9].text, '3')
        self.assertEqual(tokens[10].text, '+')
        self.assertEqual(tokens[11].text, '2')
        self.assertEqual(tokens[12].text, '<=')
        self.assertEqual(tokens[13].text, '2')
        self.assertEqual(tokens[14].text, '*')
        self.assertEqual(tokens[15].text, '4')
        self.assertEqual(tokens[16].text, '\n')

    def testTeacherExample3TokenType(self):
        lexer = Lexer('1 + 21 -- 3 / 4\n~3 + 2 <= 2 -- * 4')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.NUM)
        self.assertEqual(tokens[1].kind, TokenType.ADD)
        self.assertEqual(tokens[2].kind, TokenType.NUM)
        self.assertEqual(tokens[3].kind, TokenType.NEG)
        self.assertEqual(tokens[4].kind, TokenType.NUM)
        self.assertEqual(tokens[5].kind, TokenType.ADD)
        self.assertEqual(tokens[6].kind, TokenType.NUM)
        self.assertEqual(tokens[7].kind, TokenType.LEQ)
        self.assertEqual(tokens[8].kind, TokenType.NUM)

    def testTeacherExample3Text(self):
        lexer = Lexer('1 + 21 -- 3 / 4\n~3 + 2 <= 2 -- * 4')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].text, '1')
        self.assertEqual(tokens[1].text, '+')
        self.assertEqual(tokens[2].text, '21')
        self.assertEqual(tokens[3].text, '~')
        self.assertEqual(tokens[4].text, '3')
        self.assertEqual(tokens[5].text, '+')
        self.assertEqual(tokens[6].text, '2')
        self.assertEqual(tokens[7].text, '<=')
        self.assertEqual(tokens[8].text, '2')

    def testTeacherExample4TokenType(self):
        lexer = Lexer('343 + 324 - 63535 * ~344\n')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.NUM)
        self.assertEqual(tokens[1].kind, TokenType.ADD)
        self.assertEqual(tokens[2].kind, TokenType.NUM)
        self.assertEqual(tokens[3].kind, TokenType.SUB)
        self.assertEqual(tokens[4].kind, TokenType.NUM)
        self.assertEqual(tokens[5].kind, TokenType.MUL)
        self.assertEqual(tokens[6].kind, TokenType.NEG)
        self.assertEqual(tokens[7].kind, TokenType.NUM)
        self.assertEqual(tokens[8].kind, TokenType.NLN)

    def testTeacherExample4Text(self):
        lexer = Lexer('343 + 324 - 63535 * ~344\n')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].text, '343')
        self.assertEqual(tokens[1].text, '+')
        self.assertEqual(tokens[2].text, '324')
        self.assertEqual(tokens[3].text, '-')
        self.assertEqual(tokens[4].text, '63535')
        self.assertEqual(tokens[5].text, '*')
        self.assertEqual(tokens[6].text, '~')
        self.assertEqual(tokens[7].text, '344')
        self.assertEqual(tokens[8].text, '\n')

    def testTeacherExample5TokenType(self):
        lexer = Lexer('2 * (3 + 4)\n')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.NUM)
        self.assertEqual(tokens[1].kind, TokenType.MUL)
        self.assertEqual(tokens[2].kind, TokenType.LPR)
        self.assertEqual(tokens[3].kind, TokenType.NUM)
        self.assertEqual(tokens[4].kind, TokenType.ADD)
        self.assertEqual(tokens[5].kind, TokenType.NUM)
        self.assertEqual(tokens[6].kind, TokenType.RPR)
        self.assertEqual(tokens[7].kind, TokenType.NLN)

    def testTeacherExample5Text(self):
        lexer = Lexer('2 * (3 + 4)\n')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].text, '2')
        self.assertEqual(tokens[1].text, '*')
        self.assertEqual(tokens[2].text, '(')
        self.assertEqual(tokens[3].text, '3')
        self.assertEqual(tokens[4].text, '+')
        self.assertEqual(tokens[5].text, '4')
        self.assertEqual(tokens[6].text, ')')
        self.assertEqual(tokens[7].text, '\n')
    
    def testTeacherExample6TokenType(self):
        lexer = Lexer('1 + 3 * (* laskdjf a;lk ;kl *) 5 - 1\n')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.NUM)
        self.assertEqual(tokens[1].kind, TokenType.ADD)
        self.assertEqual(tokens[2].kind, TokenType.NUM)
        self.assertEqual(tokens[3].kind, TokenType.MUL)
        self.assertEqual(tokens[4].kind, TokenType.NUM)
        self.assertEqual(tokens[5].kind, TokenType.SUB)
        self.assertEqual(tokens[6].kind, TokenType.NUM)
        self.assertEqual(tokens[7].kind, TokenType.NLN)

    def testTeacherExample6Text(self):
        lexer = Lexer('1 + 3 * (* laskdjf a;lk ;kl *) 5 - 1\n')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].text, '1')
        self.assertEqual(tokens[1].text, '+')
        self.assertEqual(tokens[2].text, '3')
        self.assertEqual(tokens[3].text, '*')
        self.assertEqual(tokens[4].text, '5')
        self.assertEqual(tokens[5].text, '-')
        self.assertEqual(tokens[6].text, '1')
        self.assertEqual(tokens[7].text, '\n')
    
    def testTeacherExample7TokenType(self):
        lexer = Lexer('1 + (* laksdj fa;lskdjf alsdkjf\nlaskdjf\naslkdjf\nslkd  * lasdkjfa * ) akjd falskd f*)\n2\n')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.NUM)
        self.assertEqual(tokens[1].kind, TokenType.ADD)
        self.assertEqual(tokens[2].kind, TokenType.NLN)
        self.assertEqual(tokens[3].kind, TokenType.NUM)
        self.assertEqual(tokens[4].kind, TokenType.NLN)

    def testTeacherExample7Text(self):
        lexer = Lexer('1 + (* laksdj fa;lskdjf alsdkjf\nlaskdjf\naslkdjf\nslkd  * lasdkjfa * ) akjd falskd f*)\n2\n')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].text, '1')
        self.assertEqual(tokens[1].text, '+')
        self.assertEqual(tokens[2].text, '\n')
        self.assertEqual(tokens[3].text, '2')
        self.assertEqual(tokens[4].text, '\n')

if __name__ == "__main__":
    pass