import sys

from Expression import *
from Lexer import Token, TokenType
from Visitor import EvalVisitor

"""
This file implements a parser for SML with anonymous functions. The grammar is
as follows:

fn_exp  ::= fn <var> => fn_exp
          | if_exp
if_exp  ::= <if> if_exp <then> fn_exp <else> fn_exp
          | or_exp
or_exp  ::= and_exp (or and_exp)*
and_exp ::= eq_exp (and eq_exp)*
eq_exp  ::= cmp_exp (= cmp_exp)*
cmp_exp ::= add_exp ([<=|<] add_exp)*
add_exp ::= mul_exp ([+|-] mul_exp)*
mul_exp ::= unary_exp ([*|/] unary_exp)*
unary_exp ::= <not> unary_exp
             | ~ unary_exp
             | let_exp
let_exp ::= <let> <var> <- fn_exp <in> fn_exp <end>
          | val_exp
val_exp ::= val_tk (val_tk)*
val_tk ::= <var> | ( fn_exp ) | <num> | <true> | <false>

References:
    see https://www.engr.mun.ca/~theo/Misc/exp_parsing.htm#classic
"""

class Parser:
    def __init__(self, tokens):
        """
        Initializes the parser. The parser keeps track of the list of tokens
        and the current token. For instance:
        """
        self.tokens = list(tokens)
        self.cur_token_idx = 0 # This is just a suggestion!
        self.is_end_tokens = False
    
    def advance(self):
        if self.cur_token_idx < len(self.tokens) - 1:
            self.cur_token_idx += 1
        else:
            self.is_end_tokens = True

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
    
    def parse(self):
        """
        Returns the expression associated with the stream of tokens.

        Examples:
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

        >>> tk0 = Token('fn', TokenType.FNX)
        >>> tk1 = Token('v', TokenType.VAR)
        >>> tk2 = Token('=>', TokenType.ARW)
        >>> tk3 = Token('v', TokenType.VAR)
        >>> tk4 = Token('+', TokenType.ADD)
        >>> tk5 = Token('1', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> print(exp.accept(ev, None))
        Fn(v)

        >>> tk0 = Token('(', TokenType.LPR)
        >>> tk1 = Token('fn', TokenType.FNX)
        >>> tk2 = Token('v', TokenType.VAR)
        >>> tk3 = Token('=>', TokenType.ARW)
        >>> tk4 = Token('v', TokenType.VAR)
        >>> tk5 = Token('+', TokenType.ADD)
        >>> tk6 = Token('1', TokenType.NUM)
        >>> tk7 = Token(')', TokenType.RPR)
        >>> tk8 = Token('2', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7, tk8])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, {})
        3
        """
        return self.fn_exp()
    
    def fn_exp(self):
        """
        Parses function expressions.

        Grammar:
            fn_exp ::= fn <var> => fn_exp | if_exp
        """
        if self.match(TokenType.FNX):
            token = self.current_token()
            if token.kind != TokenType.VAR:
                raise ValueError("Expected a variable after 'fn'")
            formal = token.text
            self.advance()
            if not self.match(TokenType.ARW):
                raise ValueError("Expected '=>' after parameter")
            body = self.fn_exp()
            return Fn(formal, body)
        return self.if_exp()

    def if_exp(self):
        """
        Parses conditional expressions.

        Grammar:
            if_exp ::= <if> if_exp <then> fn_exp <else> fn_exp | or_exp
        """
        if self.match(TokenType.IFX):
            condition = self.if_exp()
            self.advance_newlines()
            if not self.match(TokenType.THN):
                raise ValueError("Expected 'then' after condition")
            true_val = self.fn_exp()
            self.advance_newlines()
            if not self.match(TokenType.ELS):
                raise ValueError("Expected 'else' after then branch")
            false_val = self.fn_exp()
            self.advance_newlines()
            return IfThenElse(condition, true_val, false_val)
        return self.or_exp()

    def or_exp(self):
        """
        Parses logical OR expressions.

        Grammar:
            or_exp ::= and_exp (or and_exp)*
        """
        left = self.and_exp()
        while self.match(TokenType.ORX):
            right = self.and_exp()
            left = Or(left, right)
        return left

    def and_exp(self):
        """
        Parses logical AND expressions.

        Grammar:
            and_exp ::= eq_exp (and eq_exp)*
        """
        left = self.eq_exp()
        while self.match(TokenType.AND):
            right = self.eq_exp()
            left = And(left, right)
        return left

    def eq_exp(self):
        """
        Parses equality expressions.

        Grammar:
            eq_exp ::= cmp_exp (= cmp_exp)*
        """
        left = self.cmp_exp()
        while self.match(TokenType.EQL):
            right = self.cmp_exp()
            left = Eql(left, right)
        return left

    def cmp_exp(self):
        """
        Parses comparison expressions.

        Grammar:
            cmp_exp ::= add_exp ([<=|<] add_exp)*
        """
        left = self.add_exp()
        while self.current_token().kind in (TokenType.LEQ, TokenType.LTH):
            operator = self.current_token().kind
            self.advance()
            right = self.add_exp()
            if operator == TokenType.LEQ:
                left = Leq(left, right)
            elif operator == TokenType.LTH:
                left = Lth(left, right)
        return left

    def add_exp(self):
        """
        Parses addition and subtraction expressions.

        Grammar:
            add_exp ::= mul_exp ([+|-] mul_exp)*
        """
        left = self.mul_exp()
        while self.current_token().kind in (TokenType.ADD, TokenType.SUB):
            operator = self.current_token().kind
            self.advance()
            right = self.mul_exp()
            if operator == TokenType.ADD:
                left = Add(left, right)
            elif operator == TokenType.SUB:
                left = Sub(left, right)
        return left

    def mul_exp(self):
        """
        Parses multiplication and division expressions.

        Grammar:
            mul_exp ::= unary_exp ([*|/] unary_exp)*
        """
        left = self.unary_exp()
        while self.current_token().kind in (TokenType.MUL, TokenType.DIV):
            operator = self.current_token().kind
            self.advance()
            right = self.unary_exp()
            if operator == TokenType.MUL:
                left = Mul(left, right)
            elif operator == TokenType.DIV:
                left = Div(left, right)
        return left

    def unary_exp(self):
        """
        Parses unary expressions.

        Grammar:
            unary_exp ::= <not> unary_exp | ~ unary_exp | let_exp
        """
        if self.match(TokenType.NOT):
            expr = self.unary_exp()
            return Not(expr)
        elif self.match(TokenType.NEG):
            expr = self.unary_exp()
            return Neg(expr)
        return self.let_exp()

    def let_exp(self):
        """
        Parses let expressions.

        Grammar:
            let_exp ::= <let> <var> <- fn_exp <in> fn_exp <end> | val_exp
        """
        if self.match(TokenType.LET):
            self.advance_newlines()
            token = self.current_token()
            if token.kind != TokenType.VAR:
                raise ValueError("Expected a variable after 'fn'")
            identifier = token.text
            self.advance()
            if not self.match(TokenType.ASN):
                raise ValueError("Expected '<-' after variable in 'let'")
            exp_def = self.fn_exp()
            self.advance_newlines()
            if not self.match(TokenType.INX):
                raise ValueError("Expected 'in' in let expression")
            self.advance_newlines()
            exp_body = self.fn_exp()
            self.advance_newlines()
            if not self.match(TokenType.END):
                raise ValueError("Expected 'end' after let body")
            return Let(identifier, exp_def, exp_body)
        return self.val_exp()

    def val_exp(self):
        """
        Parses value expressions, accounting for the application of functions.

        Grammar:
            val_exp ::= val_tk (val_tk)*

        Applications of functions have the highest precedence, and associativity
        is left-to-right. For example, `f g x` is parsed as `((f g) x)`.
        """
        expr = self.val_tk()  # Parse the first value token

        while True:
            if not self.is_end_tokens and self.current_token().kind in (TokenType.VAR, TokenType.LPR, TokenType.NUM, TokenType.TRU, TokenType.FLS):
                # Parse subsequent value tokens as arguments for function application
                argument = self.val_tk()
                expr = App(expr, argument)
            else:
                break
        return expr

    def val_tk(self):
        """
        Parses individual value tokens.

        Grammar:
            val_tk ::= <var> | ( fn_exp ) | <num> | <true> | <false>
        """
        token = self.current_token()
        if token.kind == TokenType.VAR:
            self.advance()
            return Var(token.text)
        elif token.kind == TokenType.NUM:
            self.advance()
            return Num(int(token.text))
        elif token.kind == TokenType.TRU:
            self.advance()
            return Bln(True)
        elif token.kind == TokenType.FLS:
            self.advance()
            return Bln(False)
        elif token.kind == TokenType.LPR:
            self.advance()
            expr = self.fn_exp()
            if not self.match(TokenType.RPR):
                raise ValueError("Expected ')' after expression")
            return expr
        else:
            sys.exit("Parse error")