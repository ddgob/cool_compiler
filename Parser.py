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
        Traceback (most recent call last):
        ...
        SystemExit: Type error

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
        SystemExit: Def error

        >>> parser = Parser([
        ...     Token('let', TokenType.LET), Token('x', TokenType.VAR), Token('<-', TokenType.ASN),
        ...     Token('5', TokenType.NUM), Token('in', TokenType.INX),
        ...     Token('x', TokenType.VAR), Token('+', TokenType.ADD), Token('3', TokenType.NUM),
        ...     Token('end', TokenType.END)
        ... ])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        8

        >>> parser = Parser([
        ...     Token('let', TokenType.LET), Token('x', TokenType.VAR), Token('<-', TokenType.ASN),
        ...     Token('7', TokenType.NUM), Token('in', TokenType.INX),
        ...     Token('x', TokenType.VAR), Token('*', TokenType.MUL), Token('x', TokenType.VAR),
        ...     Token('end', TokenType.END)
        ... ])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        49

        >>> parser = Parser([
        ...     Token('let', TokenType.LET), Token('a', TokenType.VAR), Token('<-', TokenType.ASN),
        ...     Token('2', TokenType.NUM), Token('in', TokenType.INX),
        ...     Token('let', TokenType.LET), Token('b', TokenType.VAR), Token('<-', TokenType.ASN),
        ...     Token('3', TokenType.NUM), Token('in', TokenType.INX),
        ...     Token('a', TokenType.VAR), Token('+', TokenType.ADD), Token('b', TokenType.VAR),
        ...     Token('end', TokenType.END), Token('end', TokenType.END)
        ... ])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        5

        >>> parser = Parser([
        ...     Token('let', TokenType.LET), Token('x', TokenType.VAR), Token('<-', TokenType.ASN),
        ...     Token('10', TokenType.NUM), Token('in', TokenType.INX),
        ...     Token('x', TokenType.VAR), Token('<=', TokenType.LEQ), Token('15', TokenType.NUM),
        ...     Token('end', TokenType.END)
        ... ])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        True

        >>> parser = Parser([
        ...     Token('let', TokenType.LET), Token('x', TokenType.VAR), Token('<-', TokenType.ASN),
        ...     Token('5', TokenType.NUM), Token('in', TokenType.INX),
        ...     Token('let', TokenType.LET), Token('y', TokenType.VAR), Token('<-', TokenType.ASN),
        ...     Token('x', TokenType.VAR), Token('*', TokenType.MUL), Token('3', TokenType.NUM),
        ...     Token('in', TokenType.INX), Token('y', TokenType.VAR), Token('end', TokenType.END),
        ...     Token('+', TokenType.ADD), Token('2', TokenType.NUM),
        ...     Token('end', TokenType.END)
        ... ])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        17

        >>> parser = Parser([Token('123', TokenType.NUM)])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        123

        >>> parser = Parser([Token('True', TokenType.TRU)])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> parser = Parser([Token('False', TokenType.FLS)])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        False

        >>> tk0 = Token('~', TokenType.NEG)
        >>> tk1 = Token('123', TokenType.NUM)
        >>> parser = Parser([tk0, tk1])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        -123

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        12

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('~', TokenType.NEG)
        >>> tk3 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        -12

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('/', TokenType.DIV)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        7

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('+', TokenType.ADD)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        7

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('-', TokenType.SUB)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
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
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        14

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('==', TokenType.EQL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<=', TokenType.LEQ)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<', TokenType.LTH)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        False

        >>> tk0 = Token('not', TokenType.NOT)
        >>> tk1 = Token('(', TokenType.LPR)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> tk3 = Token('<', TokenType.LTH)
        >>> tk4 = Token('4', TokenType.NUM)
        >>> tk5 = Token(')', TokenType.RPR)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('true', TokenType.TRU)
        >>> tk1 = Token('or', TokenType.ORX)
        >>> tk2 = Token('false', TokenType.FLS)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('true', TokenType.TRU)
        >>> tk1 = Token('and', TokenType.AND)
        >>> tk2 = Token('false', TokenType.FLS)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        False

        >>> tk0 = Token('let', TokenType.LET)
        >>> tk1 = Token('v', TokenType.VAR)
        >>> tk2 = Token('<-', TokenType.ASN)
        >>> tk3 = Token('42', TokenType.NUM)
        >>> tk4 = Token('in', TokenType.INX)
        >>> tk5 = Token('v', TokenType.VAR)
        >>> tk6 = Token('end', TokenType.END)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, {})
        42

        >>> tk0 = Token('let', TokenType.LET)
        >>> tk1 = Token('v', TokenType.VAR)
        >>> tk2 = Token('<-', TokenType.ASN)
        >>> tk3 = Token('21', TokenType.NUM)
        >>> tk4 = Token('in', TokenType.INX)
        >>> tk5 = Token('v', TokenType.VAR)
        >>> tk6 = Token('+', TokenType.ADD)
        >>> tk7 = Token('v', TokenType.VAR)
        >>> tk8 = Token('end', TokenType.END)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7, tk8])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, {})
        42

        >>> tk0 = Token('if', TokenType.IFX)
        >>> tk1 = Token('2', TokenType.NUM)
        >>> tk2 = Token('<', TokenType.LTH)
        >>> tk3 = Token('3', TokenType.NUM)
        >>> tk4 = Token('then', TokenType.THN)
        >>> tk5 = Token('1', TokenType.NUM)
        >>> tk6 = Token('else', TokenType.ELS)
        >>> tk7 = Token('2', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        1

        >>> tk0 = Token('if', TokenType.IFX)
        >>> tk1 = Token('false', TokenType.FLS)
        >>> tk2 = Token('then', TokenType.THN)
        >>> tk3 = Token('1', TokenType.NUM)
        >>> tk4 = Token('else', TokenType.ELS)
        >>> tk5 = Token('2', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        2

        >>> parser = Parser([
        ...     Token('not', TokenType.NOT), Token('3', TokenType.NUM),
        ...     Token('<', TokenType.LTH), Token('2', TokenType.NUM)
        ... ])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        Traceback (most recent call last):
        ...
        SystemExit: Type error

        >>> parser = Parser([
        ...     Token('not', TokenType.NOT),
        ...     Token('(', TokenType.LPR),
        ...     Token('(', TokenType.LPR),
        ...     Token('2', TokenType.NUM),
        ...     Token('+', TokenType.ADD),
        ...     Token('5', TokenType.NUM),
        ...     Token(')', TokenType.RPR),
        ...     Token('*', TokenType.MUL),
        ...     Token('2', TokenType.NUM),
        ...     Token('<', TokenType.LTH),
        ...     Token('13', TokenType.NUM),
        ...     Token('=', TokenType.EQL),
        ...     Token('true', TokenType.TRU),
        ...     Token(')', TokenType.RPR)
        ... ])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        True

        >>> parser = Parser([
        ...     Token('let', TokenType.LET),
        ...     Token("\\n", TokenType.NLN),
        ...     Token('x', TokenType.VAR),
        ...     Token('<-', TokenType.ASN),
        ...     Token('23', TokenType.NUM),
        ...     Token('\\n', TokenType.NLN),
        ...     Token('in', TokenType.INX),
        ...     Token('\\n', TokenType.NLN),
        ...     Token('if', TokenType.IFX),
        ...     Token('x', TokenType.VAR),
        ...     Token('<', TokenType.LTH),
        ...     Token('20', TokenType.NUM),
        ...     Token('\\n', TokenType.NLN),
        ...     Token('then', TokenType.THN),
        ...     Token('true', TokenType.TRU),
        ...     Token('\\n', TokenType.NLN),
        ...     Token('else', TokenType.ELS),
        ...     Token('false', TokenType.FLS),
        ...     Token('\\n', TokenType.NLN),
        ...     Token('end', TokenType.END)
        ... ])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        False

        >>> parser = Parser([
        ...     Token('if', TokenType.IFX),
        ...     Token('2', TokenType.NUM),
        ...     Token('<', TokenType.LTH),
        ...     Token('3', TokenType.NUM),
        ...     Token('then', TokenType.THN),
        ...     Token('true', TokenType.TRU),
        ...     Token('else', TokenType.ELS),
        ...     Token('false', TokenType.FLS)
        ... ])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        True

        >>> parser = Parser([
        ...     Token('let', TokenType.LET),
        ...     Token('x', TokenType.VAR),
        ...     Token('<-', TokenType.ASN),
        ...     Token('23', TokenType.NUM),
        ...     Token('in', TokenType.INX),
        ...     Token('if', TokenType.IFX),
        ...     Token('if', TokenType.IFX),
        ...     Token('x', TokenType.VAR),
        ...     Token('<', TokenType.LTH),
        ...     Token('20', TokenType.NUM),
        ...     Token('then', TokenType.THN),
        ...     Token('false', TokenType.FLS),
        ...     Token('else', TokenType.ELS),
        ...     Token('true', TokenType.TRU),
        ...     Token('then', TokenType.THN),
        ...     Token('true', TokenType.TRU),
        ...     Token('else', TokenType.ELS),
        ...     Token('false', TokenType.FLS),
        ...     Token('end', TokenType.END)
        ... ])
        >>> exp = parser.parse()
        >>> visitor = EvalVisitor()
        >>> exp.accept(visitor, {})
        True

        bool_expression         ::= if_then_else_expression
                                | or_expression

        if_then_else_expression ::= 'if' or_expression 'then' or_expression 'else' or_expression

        or_expression           ::= and_expression
                                | and_expression 'or' or_expression

        and_expression          ::= eql_expression
                                | eql_expression 'and' and_expression

        eql_expression          ::= comparison_expression
                                | comparison_expression '==' comparison_expression

        comparison_expression   ::= arithmetic_expression '<' arithmetic_expression 
                                | arithmetic_expression '<=' arithmetic_expression 
                                | arithmetic_expression

        arithmetic_expression   ::= term 
                                | term '+' arithmetic_expression 
                                | term '-' arithmetic_expression

        term                    ::= factor 
                                | factor '*' term 
                                | factor '/' term

        factor                  ::= 'not' factor 
                                | '~' factor 
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

    def advance_newlines(self):
        while self.current_token().kind == TokenType.NLN and self.cur_token_idx < len(self.tokens) - 1:
            self.advance()

    def current_token(self):
        return self.tokens[self.cur_token_idx]

    def match(self, token_type):
        if self.current_token().kind == token_type:
            self.advance()
            return True
        return False
    
    def bool_expression(self):
        if self.current_token().kind == TokenType.IFX:
            return self.if_then_else_expression()
        return self.or_expression()
        
    def if_then_else_expression(self):
        if not self.match(TokenType.IFX):
            sys.exit(f"Parse error")
        
        condition = self.bool_expression()

        self.advance_newlines()
        
        if not self.match(TokenType.THN):
            sys.exit(f"Parse error")
        
        then_expr = self.bool_expression()

        self.advance_newlines()
        
        if not self.match(TokenType.ELS):
            sys.exit(f"Parse error")
        
        else_expr = self.bool_expression()

        self.advance_newlines()
        
        return IfThenElse(condition, then_expr, else_expr)

    def or_expression(self):
        left = self.and_expression()
        
        while self.current_token().kind == TokenType.ORX:
            self.advance()
            right = self.and_expression()
            left = Or(left, right)
        
        return left
    
    def and_expression(self):
        left = self.eql_expression()
        
        while self.current_token().kind == TokenType.AND:
            self.advance()
            right = self.eql_expression()
            left = And(left, right)
        
        return left
    
    def eql_expression(self):
        left = self.comparison_expression()
        
        if self.match(TokenType.EQL):
            right = self.comparison_expression()
            return Eql(left, right)
        
        return left

    def comparison_expression(self):
        left = self.arithmetic_expression()
        
        while self.current_token().kind in (TokenType.LTH, TokenType.LEQ):
            if self.match(TokenType.LTH):
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
        if self.match(TokenType.NOT):
            return Not(self.factor())
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
            sys.exit(f"Parse error")

    def let_expression(self):

        self.advance_newlines()

        var_name = None
        if self.current_token().kind == TokenType.VAR:
            var_name = self.current_token().text
            self.advance()
        else:
            sys.exit(f"Parse error")
        
        if not self.match(TokenType.ASN):
            sys.exit(f"Parse error")
        
        value_expr = self.bool_expression()

        self.advance_newlines()
        
        if not self.match(TokenType.INX):
            sys.exit(f"Parse error")

        self.advance_newlines()
        
        body_expr = self.bool_expression()

        self.advance_newlines()
        
        if not self.match(TokenType.END):
            sys.exit(f"Parse error")
        
        return Let(var_name, value_expr, body_expr)