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
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        123

        >>> parser = Parser([Token('True', TokenType.TRU)])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        True

        >>> parser = Parser([Token('False', TokenType.FLS)])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        False

        >>> tk0 = Token('~', TokenType.NEG)
        >>> tk1 = Token('123', TokenType.NUM)
        >>> parser = Parser([tk0, tk1])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        -123

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        12

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('~', TokenType.NEG)
        >>> tk3 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        -12

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('/', TokenType.DIV)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        7

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('+', TokenType.ADD)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        7

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('-', TokenType.SUB)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
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
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        14

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('==', TokenType.EQL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        True

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<=', TokenType.LEQ)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        True

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<', TokenType.LTH)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        False

        >>> tk0 = Token('not', TokenType.NOT)
        >>> tk1 = Token('4', TokenType.NUM)
        >>> tk2 = Token('<', TokenType.LTH)
        >>> tk3 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        True

        >>> env = {'x': 10}
        >>> parser = Parser([Token('x', TokenType.VAR)])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, env)
        10

        >>> env = {'y': False}
        >>> parser = Parser([Token('y', TokenType.VAR)])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, env)
        False

        >>> env = {'a': 5, 'b': 3}
        >>> parser = Parser([Token('a', TokenType.VAR), Token('+', TokenType.ADD), Token('b', TokenType.VAR)])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, env)
        8

        >>> env = {'z': 7}
        >>> parser = Parser([Token('z', TokenType.VAR), Token('*', TokenType.MUL), Token('z', TokenType.VAR)])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, env)
        49

        >>> env = {}
        >>> parser = Parser([Token('w', TokenType.VAR)])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, env)
        Traceback (most recent call last):
        ...
        ValueError: Variavel inexistente w

        >>> parser = Parser([
        ...     Token('let', TokenType.LET), Token('x', TokenType.VAR), Token('<-', TokenType.ASS),
        ...     Token('5', TokenType.NUM), Token('in', TokenType.INN),
        ...     Token('x', TokenType.VAR), Token('+', TokenType.ADD), Token('3', TokenType.NUM),
        ...     Token('end', TokenType.END)
        ... ])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        8

        >>> parser = Parser([
        ...     Token('let', TokenType.LET), Token('x', TokenType.VAR), Token('<-', TokenType.ASS),
        ...     Token('7', TokenType.NUM), Token('in', TokenType.INN),
        ...     Token('x', TokenType.VAR), Token('*', TokenType.MUL), Token('x', TokenType.VAR),
        ...     Token('end', TokenType.END)
        ... ])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        49

        >>> parser = Parser([
        ...     Token('let', TokenType.LET), Token('a', TokenType.VAR), Token('<-', TokenType.ASS),
        ...     Token('2', TokenType.NUM), Token('in', TokenType.INN),
        ...     Token('let', TokenType.LET), Token('b', TokenType.VAR), Token('<-', TokenType.ASS),
        ...     Token('3', TokenType.NUM), Token('in', TokenType.INN),
        ...     Token('a', TokenType.VAR), Token('+', TokenType.ADD), Token('b', TokenType.VAR),
        ...     Token('end', TokenType.END), Token('end', TokenType.END)
        ... ])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        5

        >>> parser = Parser([
        ...     Token('let', TokenType.LET), Token('x', TokenType.VAR), Token('<-', TokenType.ASS),
        ...     Token('10', TokenType.NUM), Token('in', TokenType.INN),
        ...     Token('x', TokenType.VAR), Token('<=', TokenType.LEQ), Token('15', TokenType.NUM),
        ...     Token('end', TokenType.END)
        ... ])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        True

        >>> parser = Parser([
        ...     Token('let', TokenType.LET), Token('x', TokenType.VAR), Token('<-', TokenType.ASS),
        ...     Token('5', TokenType.NUM), Token('in', TokenType.INN),
        ...     Token('let', TokenType.LET), Token('y', TokenType.VAR), Token('<-', TokenType.ASS),
        ...     Token('x', TokenType.VAR), Token('*', TokenType.MUL), Token('3', TokenType.NUM),
        ...     Token('in', TokenType.INN), Token('y', TokenType.VAR), Token('end', TokenType.END),
        ...     Token('+', TokenType.ADD), Token('2', TokenType.NUM),
        ...     Token('end', TokenType.END)
        ... ])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        17

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
                                | variable 
                                | let_expression
        
        let_expression          ::= 'let' variable '<-' bool_expression 'in' bool_expression 'end'

        variable                ::= alpha (alpha | digit)*

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
        
        while self.current_token().kind in (TokenType.EQL, TokenType.LTH, TokenType.LEQ):
            if self.match(TokenType.EQL):
                right = self.arithmetic_expression()
                left = Eql(left, right)
            elif self.match(TokenType.LTH):
                right = self.arithmetic_expression()
                left = Lth(left, right)
            elif self.match(TokenType.LEQ):
                right = self.arithmetic_expression()
                left = Leq(left, right)
        
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
        elif self.current_token().kind == TokenType.VAR:
            var_name = self.current_token().text
            self.advance()
            return Var(var_name)
        elif self.match(TokenType.LET):
            return self.let_expression()
        elif self.match(TokenType.NLN):
            return self.factor()
        else:
            raise ValueError("Unexpected token: " + self.current_token().text)

    def let_expression(self):
        var_name = None
        if self.current_token().kind == TokenType.VAR:
            var_name = self.current_token().text
            self.advance()
        else:
            raise ValueError("Expected variable name after 'let'")
        
        if not self.match(TokenType.ASS):
            raise ValueError("Expected '<-' after variable name in 'let' expression")
        
        value_expr = self.bool_expression()
        
        if not self.match(TokenType.INN):
            raise ValueError("Expected 'in' after value expression in 'let' expression")
        
        body_expr = self.bool_expression()
        
        if not self.match(TokenType.END):
            raise ValueError("Expected 'end' after body expression in 'let' expression")
        
        return Let(var_name, value_expr, body_expr)

if __name__ == "__main__":
    parser = Parser([
    Token('let', TokenType.LET),
    Token('v', TokenType.VAR),
    Token('<-', TokenType.ASS),
    Token('1', TokenType.NUM),
    Token('in', TokenType.INN),
    Token('v', TokenType.VAR),
    Token('+', TokenType.ADD),
    Token('v', TokenType.VAR),
    Token('end', TokenType.END)
])
    exp = parser.parse()
    eval = exp.eval()
    eval2 = 1



