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
        TODO: You will need to implement this method.
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
        TODO: Implement this method!
        """
        if self.position >= self.length:
            return Token('', TokenType.EOF)
        
        current_character = self.input[self.position]
        self.position += 1

        if current_character == '\n':
            return Token('\n', TokenType.NLN)
        elif current_character == ' ':
            return Token(' ', TokenType.WSP)
        elif current_character == '-':
            if self.position < self.length and self.input[self.position] == '-':
                comment = '-'
                while self.position < self.length and self.input[self.position] != '\n':
                    comment += self.input[self.position]
                    self.position += 1
                return Token(comment, TokenType.COM)
            return Token('-', TokenType.SUB)
        elif current_character == '*':
            initialPosition = self.position
            comment = current_character
            while self.position < self.length and self.input[self.position] != '*':
                comment += self.input[self.position]
                self.position += 1

            if self.position == self.length:
                self.position = initialPosition
                return Token('*', TokenType.MUL)
            
            self.position += 1
            comment += '*'
            return Token(comment, TokenType.COM)
        elif current_character == '+':
            return Token('+', TokenType.ADD)
        elif current_character == '/':
            return Token('/', TokenType.DIV)
        elif current_character == '<':
            if self.position < self.length and self.input[self.position] == '=':
                self.position += 1
                return Token('<=', TokenType.LEQ)
            else:
                return Token('<', TokenType.LTH)
        else:
            token = None
            return token