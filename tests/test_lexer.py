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
        lexer = Lexer('not')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)

    def testNotThanInputTokenType(self):
        lexer = Lexer('not')
        token = lexer.getToken()
        self.assertEqual(token.kind, TokenType.NOT)

    def testNotThanInputText(self):
        lexer = Lexer('not')
        token = lexer.getToken()
        self.assertEqual(token.text, 'not')

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
        lexer = Lexer('1 + 21 - 3 div 4\n~3 + 2 <= 2 * 4\n')
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
        lexer = Lexer('1 + 21 - 3 div 4\n~3 + 2 <= 2 * 4\n')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].text, '1')
        self.assertEqual(tokens[1].text, '+')
        self.assertEqual(tokens[2].text, '21')
        self.assertEqual(tokens[3].text, '-')
        self.assertEqual(tokens[4].text, '3')
        self.assertEqual(tokens[5].text, 'div')
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
        lexer = Lexer('1 + 21 -- 3 div 4\n~3 + 2 <= 2 -- * 4')
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
        lexer = Lexer('1 + 21 -- 3 div 4\n~3 + 2 <= 2 -- * 4')
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

    def testLetInEndTokenType(self):
        lexer = Lexer('let in end')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.LET)
        self.assertEqual(tokens[1].kind, TokenType.INX)
        self.assertEqual(tokens[2].kind, TokenType.END)

    def testLetInEndText(self):
        lexer = Lexer('let in end')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].text, 'let')
        self.assertEqual(tokens[1].text, 'in')
        self.assertEqual(tokens[2].text, 'end')

    def testIfThenElseTokenType(self):
        lexer = Lexer('if then else')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.IFX)
        self.assertEqual(tokens[1].kind, TokenType.THN)
        self.assertEqual(tokens[2].kind, TokenType.ELS)

    def testIfThenElseText(self):
        lexer = Lexer('if then else')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].text, 'if')
        self.assertEqual(tokens[1].text, 'then')
        self.assertEqual(tokens[2].text, 'else')

    def testAndOrTokenType(self):
        lexer = Lexer('and or')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.AND)
        self.assertEqual(tokens[1].kind, TokenType.ORX)

    def testAndOrText(self):
        lexer = Lexer('and or')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].text, 'and')
        self.assertEqual(tokens[1].text, 'or')

    def testFunctionKeywordTokenType(self):
        lexer = Lexer('fn')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.FNX)

    def testFunctionKeywordText(self):
        lexer = Lexer('fn')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].text, 'fn')

    def testArrowTokenType(self):
        lexer = Lexer('=>')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.ARW)

    def testArrowText(self):
        lexer = Lexer('=>')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].text, '=>')

    def testFunctionDefinitionTokens(self):
        lexer = Lexer('fn x => x + 1')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.FNX)  # 'fn'
        self.assertEqual(tokens[1].kind, TokenType.VAR)  # 'x'
        self.assertEqual(tokens[2].kind, TokenType.ARW)  # '=>'
        self.assertEqual(tokens[3].kind, TokenType.VAR)  # 'x'
        self.assertEqual(tokens[4].kind, TokenType.ADD)  # '+'
        self.assertEqual(tokens[5].kind, TokenType.NUM)  # '1'

    def testFunctionDefinitionText(self):
        lexer = Lexer('fn x => x + 1')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].text, 'fn')
        self.assertEqual(tokens[1].text, 'x')
        self.assertEqual(tokens[2].text, '=>')
        self.assertEqual(tokens[3].text, 'x')
        self.assertEqual(tokens[4].text, '+')
        self.assertEqual(tokens[5].text, '1')

    def testDivisionOperatorRecognition(self):
        lexer = Lexer('div')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)  # Ensure only one token is returned
        self.assertEqual(tokens[0].kind, TokenType.DIV)  # Check token type
        self.assertEqual(tokens[0].text, 'div')  # Check token text

    def testModuloOperatorRecognition(self):
        lexer = Lexer('mod')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)  # Ensure only one token is returned
        self.assertEqual(tokens[0].kind, TokenType.MOD)  # Check token type
        self.assertEqual(tokens[0].text, 'mod')  # Check token text

    def testValKeywordRecognition(self):
        lexer = Lexer('val')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)  # Ensure only one token is returned
        self.assertEqual(tokens[0].kind, TokenType.VAL)  # Check token type
        self.assertEqual(tokens[0].text, 'val')  # Check token text

    def testFunKeywordRecognition(self):
        lexer = Lexer('fun')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)  # Ensure only one token is returned
        self.assertEqual(tokens[0].kind, TokenType.FUN)  # Check token type
        self.assertEqual(tokens[0].text, 'fun')  # Check token text

    def testFunAndValTogether(self):
        lexer = Lexer('fun val')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 2)  # Ensure two tokens are returned
        self.assertEqual(tokens[0].kind, TokenType.FUN)  # Check first token type
        self.assertEqual(tokens[0].text, 'fun')  # Check first token text
        self.assertEqual(tokens[1].kind, TokenType.VAL)  # Check second token type
        self.assertEqual(tokens[1].text, 'val')  # Check second token text
    
    def testTypeArrowTokenType(self):
        lexer = Lexer('->')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)  # Ensure only one token is returned
        self.assertEqual(tokens[0].kind, TokenType.TPF)  # Check token type
        self.assertEqual(tokens[0].text, '->')  # Check token text

    def testColonTokenType(self):
        lexer = Lexer(':')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)  # Ensure only one token is returned
        self.assertEqual(tokens[0].kind, TokenType.COL)  # Check token type
        self.assertEqual(tokens[0].text, ':')  # Check token text

    def testIntKeywordTokenType(self):
        lexer = Lexer('int')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)  # Ensure only one token is returned
        self.assertEqual(tokens[0].kind, TokenType.INT)  # Check token type
        self.assertEqual(tokens[0].text, 'int')  # Check token text

    def testBoolKeywordTokenType(self):
        lexer = Lexer('bool')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 1)  # Ensure only one token is returned
        self.assertEqual(tokens[0].kind, TokenType.LGC)  # Check token type
        self.assertEqual(tokens[0].text, 'bool')  # Check token text

    def testTypeAnnotationExpression(self):
        lexer = Lexer('x: int -> bool')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 5)  # Ensure five tokens are returned
        self.assertEqual(tokens[0].kind, TokenType.VAR)  # 'x'
        self.assertEqual(tokens[0].text, 'x')
        self.assertEqual(tokens[1].kind, TokenType.COL)  # ':'
        self.assertEqual(tokens[1].text, ':')
        self.assertEqual(tokens[2].kind, TokenType.INT)  # 'int'
        self.assertEqual(tokens[2].text, 'int')
        self.assertEqual(tokens[3].kind, TokenType.TPF)  # '->'
        self.assertEqual(tokens[3].text, '->')
        self.assertEqual(tokens[4].kind, TokenType.LGC)  # 'bool'
        self.assertEqual(tokens[4].text, 'bool')

    def testMultipleTypeAnnotations(self):
        lexer = Lexer('let f: int -> bool = fn x: int => x < 0')
        tokens = list(lexer.tokens())
        self.assertEqual(tokens[0].kind, TokenType.LET)  # 'let'
        self.assertEqual(tokens[1].kind, TokenType.VAR)  # 'f'
        self.assertEqual(tokens[2].kind, TokenType.COL)  # ':'
        self.assertEqual(tokens[3].kind, TokenType.INT)  # 'int'
        self.assertEqual(tokens[4].kind, TokenType.TPF)  # '->'
        self.assertEqual(tokens[5].kind, TokenType.LGC)  # 'bool'
        self.assertEqual(tokens[6].kind, TokenType.EQL)  # '='
        self.assertEqual(tokens[7].kind, TokenType.FNX)  # 'fn'
        self.assertEqual(tokens[8].kind, TokenType.VAR)  # 'x'
        self.assertEqual(tokens[9].kind, TokenType.COL)  # ':'
        self.assertEqual(tokens[10].kind, TokenType.INT)  # 'int'
        self.assertEqual(tokens[11].kind, TokenType.ARW)  # '=>'
        self.assertEqual(tokens[12].kind, TokenType.VAR)  # 'x'
        self.assertEqual(tokens[13].kind, TokenType.LTH)  # '<'
        self.assertEqual(tokens[14].kind, TokenType.NUM)  # '0'

    def testColonAndArrowTogether(self):
        lexer = Lexer(': ->')
        tokens = list(lexer.tokens())
        self.assertEqual(len(tokens), 2)  # Ensure two tokens are returned
        self.assertEqual(tokens[0].kind, TokenType.COL)  # ':'
        self.assertEqual(tokens[0].text, ':')
        self.assertEqual(tokens[1].kind, TokenType.TPF)  # '->'
        self.assertEqual(tokens[1].text, '->')


if __name__ == "__main__":
    pass
