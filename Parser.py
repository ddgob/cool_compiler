import sys

from Expression import *
from Lexer import Token, TokenType

"""
This file implements the parser of arithmetic expressions.

References:
    see https://www.engr.mun.ca/~theo/Misc/exp_parsing.htm
"""

class Parser:
    def __init__(self, tokens):
        """
        Initializes the parser. The parser keeps track of the list of tokens
        and the current token. For instance:
        """
        self.tokens = list(tokens)
        self.cur_token_idx = 0 # This is just a suggestion!

    def parse(self):
        """
        Returns the expression associated with the stream of tokens.

        Examples:
        >>> parser = Parser([Token('123', TokenType.NUM)])
        >>> exp = parser.parse()
        >>> exp.eval()
        123

        >>> parser = Parser([Token('True', TokenType.TRU)])
        >>> exp = parser.parse()
        >>> exp.eval()
        True

        >>> parser = Parser([Token('False', TokenType.FLS)])
        >>> exp = parser.parse()
        >>> exp.eval()
        False

        >>> tk0 = Token('~', TokenType.NEG)
        >>> tk1 = Token('123', TokenType.NUM)
        >>> parser = Parser([tk0, tk1])
        >>> exp = parser.parse()
        >>> exp.eval()
        -123

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval()
        12

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('~', TokenType.NEG)
        >>> tk3 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> exp = parser.parse()
        >>> exp.eval()
        -12

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('/', TokenType.DIV)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval()
        7

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('+', TokenType.ADD)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval()
        7

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('-', TokenType.SUB)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval()
        26

        >>> tk0 = Token('2', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('(', TokenType.LPR)
        >>> tk3 = Token('3', TokenType.NUM)
        >>> tk4 = Token('+', TokenType.ADD)
        >>> tk5 = Token('4', TokenType.NUM)
        >>> tk6 = Token(')', TokenType.RPR)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6])
        >>> exp = parser.parse()
        >>> exp.eval()
        14

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('==', TokenType.EQL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval()
        True

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<=', TokenType.LEQ)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval()
        True

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<', TokenType.LTH)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval()
        False

        >>> tk0 = Token('not', TokenType.NOT)
        >>> tk1 = Token('4', TokenType.NUM)
        >>> tk2 = Token('<', TokenType.LTH)
        >>> tk3 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> exp = parser.parse()
        >>> exp.eval()
        True
        """
        """
        Grammer for the parser:
        bool_expr ::= 'not' bool_expr | comp_expr
        comp_expr ::= exp '==' exp | exp '<' exp | exp '<=' exp | exp
        exp       ::= term | term '+' exp | term '-' exp
        term      ::= factor | factor '*' term | factor '/' term
        factor    ::= '~' factor | '(' bool_expr ')' | num | boolean
        boolean   ::= 'true' | 'false'


        bool_expression         ::= 'not' bool_expression 
                                | comparison_expression

        comparison_expression   ::= arithmetic_expression '==' arithmetic_expression 
                                | arithmetic_expression '<' arithmetic_expression 
                                | arithmetic_expression '<=' arithmetic_expression 
                                | arithmetic_expression

        arithmetic_expression   ::= term 
                                | term '+' arithmetic_expression 
                                | term '-' arithmetic_expression

        term                    ::= factor 
                                | factor '*' term 
                                | factor '/' term

        factor                  ::= '~' factor 
                                | '(' bool_expression ')' 
                                | number 
                                | boolean_literal

        boolean_literal         ::= 'true' 
                                | 'false'
        """
        return self.bool_expression()
    
    def advance(self):
        if self.cur_token_idx < len(self.tokens) - 1:
            self.cur_token_idx += 1

    def current_token(self):
        return self.tokens[self.cur_token_idx]

    def match(self, token_type):
        if self.current_token().kind == token_type:
            self.advance()
            return True
        return False

    def bool_expression(self):
        if self.match(TokenType.NOT):
            return Not(self.bool_expression())
        else:
            return self.comparison_expression()

    def comparison_expression(self):
        left = self.arithmetic_expression()
        
        if self.match(TokenType.EQL):
            right = self.arithmetic_expression()
            return Eql(left, right)
        elif self.match(TokenType.LTH):
            right = self.arithmetic_expression()
            return Lth(left, right)
        elif self.match(TokenType.LEQ):
            right = self.arithmetic_expression()
            return Leq(left, right)
        
        return left

    def arithmetic_expression(self):
        left = self.term()
        
        while self.current_token().kind in (TokenType.ADD, TokenType.SUB):
            if self.match(TokenType.ADD):
                right = self.term()
                left = Add(left, right)
            elif self.match(TokenType.SUB):
                right = self.term()
                left = Sub(left, right)
        
        return left

    def term(self):
        left = self.factor()
        
        while self.current_token().kind in (TokenType.MUL, TokenType.DIV):
            if self.match(TokenType.MUL):
                right = self.factor()
                left = Mul(left, right)
            elif self.match(TokenType.DIV):
                right = self.factor()
                left = Div(left, right)
        
        return left

    def factor(self):
        if self.match(TokenType.NEG):
            return Neg(self.factor())
        elif self.match(TokenType.LPR):
            expr = self.bool_expression()
            if not self.match(TokenType.RPR):
                raise ValueError("Expected closing parenthesis")
            return expr
        elif self.current_token().kind == TokenType.NUM:
            num_value = int(self.current_token().text)
            self.advance()
            return Num(num_value)
        elif self.match(TokenType.TRU):
            return Bln(True)
        elif self.match(TokenType.FLS):
            return Bln(False)
        else:
            raise ValueError("Unexpected token: " + self.current_token().text)