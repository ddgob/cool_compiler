import sys
import enum


class Token:
    """
    This class contains the definition of Tokens. A token has two fields: its
    text and its kind. The "kind" of a token is a constant that identifies it
    uniquely. See the TokenType to know the possible identifiers (if you want).
    You don't need to change this class.
    """
    def __init__(self, tokenText, tokenKind):
        # The token's actual text. Used for identifiers, strings, and numbers.
        self.text = tokenText
        # The TokenType that this token is classified as.
        self.kind = tokenKind


class TokenType(enum.Enum):
    """
    These are the possible tokens. You don't need to change this class at all.
    """
    EOF = -1  # End of file
    NLN = 0   # New line
    WSP = 1   # White Space
    COM = 2   # Comment
    NUM = 3   # Number (integers)
    STR = 4   # Strings
    TRU = 5   # The constant true
    FLS = 6   # The constant false
    EQL = 201
    ADD = 202
    SUB = 203
    MUL = 204
    DIV = 205
    LEQ = 206
    LTH = 207
    NEG = 208
    NOT = 209
    LPR = 210
    RPR = 211


class Lexer:

    def __init__(self, source):
        """
        The constructor of the lexer. It receives the string that shall be
        scanned.
        """
        self.input = source
        self.position = 0
        self.length = len(source)

    def tokens(self):
        """
        This method is a token generator: it converts the string encapsulated
        into this object into a sequence of Tokens. Examples:

        >>> l = Lexer('1 * 2 - 3')
        >>> [tk.kind for tk in l.tokens()]
        [<TokenType.NUM: 3>, <TokenType.ADD: 202>, <TokenType.NUM: 3>]

        >>> l = Lexer('1 * 2 -- 3\\n')
        >>> [tk.kind for tk in l.tokens()]
        [<TokenType.NUM: 3>, <TokenType.MUL: 204>, <TokenType.NUM: 3>]
        """
        token = self.getToken()
        while token.kind != TokenType.EOF:
            if token.kind != TokenType.WSP and token.kind != TokenType.COM:
                yield token
            token = self.getToken()

    def getToken(self):
        """
        Return the next token.
        """
        if self.position >= self.length:
            return Token('', TokenType.EOF)

        currentCharacter = self.input[self.position]
        self.position += 1

        if currentCharacter == ' ':
            return Token(' ', TokenType.WSP)
        elif currentCharacter.isdigit():
            number = currentCharacter
            while self.position < self.length and self.input[self.position].isdigit():
                number += self.input[self.position]
                self.position += 1
            return Token(number, TokenType.NUM)
        elif currentCharacter == '+':
            return Token('+', TokenType.ADD)
        elif currentCharacter == '*':
            return Token('*', TokenType.MUL)
        elif currentCharacter == '/':
            return Token('/', TokenType.DIV)
        elif currentCharacter == '-':
            if self.position < self.length and self.input[self.position] == '-':
                comment = '-'
                while self.position < self.length and self.input[self.position] != '\n':
                    comment += self.input[self.position]
                    self.position += 1
                if self.position < self.length and self.input[self.position] == '\n':
                    comment += '\n'
                self.position += 1
                return Token(comment, TokenType.COM)
            return Token('-', TokenType.SUB)
        elif currentCharacter == '\n':
            return Token('\n', TokenType.NLN)
        elif currentCharacter == '<':
            if self.position < self.length and self.input[self.position] == '=':
                self.position += 1
                return Token('<=', TokenType.LEQ)
            else:
                return Token('<', TokenType.LTH)
        elif currentCharacter == '~':
            return Token('~', TokenType.NEG)
        elif currentCharacter == 'n':
            firstCharAfterN = self.input[self.position]
            self.position += 1
            secondCharAfterN = self.input[self.position]
            if firstCharAfterN == 'o' and secondCharAfterN == 't':
                self.position += 1
                return Token('not', TokenType.NOT)
        elif currentCharacter == 't':
            firstCharAfterTIsR = self.input[self.position] == 'r'
            self.position += 1
            secondCharAfterTIsU = self.input[self.position] == 'u'
            self.position += 1
            thirdCharAfterTIsE = self.input[self.position] == 'e'
            if firstCharAfterTIsR and secondCharAfterTIsU and thirdCharAfterTIsE:
                self.position += 1
                return Token('true', TokenType.TRU)
        elif currentCharacter == 'f':
            firstCharAfterFIsA = self.input[self.position] == 'a'
            self.position += 1
            secondCharAfterFIsL = self.input[self.position] == 'l'
            self.position += 1
            thirdCharAfterFIsS = self.input[self.position] == 's'
            self.position += 1
            fourthCharAfterFIsE = self.input[self.position] == 'e'
            if (
                firstCharAfterFIsA and
                secondCharAfterFIsL and
                thirdCharAfterFIsS and
                fourthCharAfterFIsE
            ):
                self.position += 1
                return Token('false', TokenType.FLS)
        elif currentCharacter == '(':
            if self.position < self.length and self.input[self.position] == '*':
                self.position += 1
                comment = '(*'
                while True:
                    if self.position + 1 < self.length and self.input[self.position] == '*' and self.input[self.position + 1] == ')':
                        break
                    comment += self.input[self.position]
                    self.position += 1
                self.position += 2
                comment += '*)'
                return Token(comment, TokenType.COM)
            return Token('(', TokenType.LPR)
        elif currentCharacter == ')':
            return Token(')', TokenType.RPR)
        else:
            raise ValueError(f"Character not recognized: {currentCharacter}")
