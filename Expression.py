from abc import ABC, abstractmethod

class Expression(ABC):
    @abstractmethod
    def eval(self, env=None):
        raise NotImplementedError

class Bln(Expression):
    """
    This class represents expressions that are boolean values. There are only
    two boolean values: true and false. The evaluation of such an expression is
    the boolean itself.
    """
    def __init__(self, bln):
        self.bln = bln
    def eval(self, env=None):
        """
        Example:
        >>> e = Bln(True)
        >>> e.eval()
        True
        """
        return self.bln

class Num(Expression):
    """
    This class represents expressions that are numbers. The evaluation of such
    an expression is the number itself.
    """
    def __init__(self, num):
        self.num = num
    def eval(self, env=None):
        """
        Example:
        >>> e = Num(3)
        >>> e.eval()
        3
        """
        return self.num

class BinaryExpression(Expression):
    """
    This class represents binary expressions. A binary expression has two
    sub-expressions: the left operand and the right operand.
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @abstractmethod
    def eval(self, env=None):
        raise NotImplementedError

class Eql(BinaryExpression):
    """
    This class represents the equality between two expressions. The evaluation
    of such an expression is True if the subexpressions are the same, or false
    otherwise.
    """
    def eval(self, env=None):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Eql(n1, n2)
        >>> e.eval()
        False

        >>> n1 = Num(3)
        >>> n2 = Num(3)
        >>> e = Eql(n1, n2)
        >>> e.eval()
        True
        """
        return self.left.eval(env) == self.right.eval(env)

class Add(BinaryExpression):
    """
    This class represents addition of two expressions. The evaluation of such
    an expression is the addition of the two subexpression's values.
    """
    def eval(self, env=None):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Add(n1, n2)
        >>> e.eval()
        7
        """
        return self.left.eval(env) + self.right.eval(env)

class Sub(BinaryExpression):
    """
    This class represents subtraction of two expressions. The evaluation of such
    an expression is the subtraction of the two subexpression's values.
    """
    def eval(self, env=None):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Sub(n1, n2)
        >>> e.eval()
        -1
        """
        return self.left.eval(env) - self.right.eval(env)

class Mul(BinaryExpression):
    """
    This class represents multiplication of two expressions. The evaluation of
    such an expression is the product of the two subexpression's values.
    """
    def eval(self, env=None):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Mul(n1, n2)
        >>> e.eval()
        12
        """
        return self.left.eval(env) * self.right.eval(env)

class Div(BinaryExpression):
    """
    This class represents the integer division of two expressions. The
    evaluation of such an expression is the integer quocient of the two
    subexpression's values.
    """
    def eval(self, env=None):
        """
        Example:
        >>> n1 = Num(28)
        >>> n2 = Num(4)
        >>> e = Div(n1, n2)
        >>> e.eval()
        7
        >>> n1 = Num(22)
        >>> n2 = Num(4)
        >>> e = Div(n1, n2)
        >>> e.eval()
        5
        """
        return self.left.eval(env) // self.right.eval(env)

class Leq(BinaryExpression):
    """
    This class represents comparison of two expressions using the
    less-than-or-equal comparator. The evaluation of such an expression is a
    boolean value that is true if the left operand is less than or equal the
    right operand. It is false otherwise.
    """
    def eval(self, env=None):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Leq(n1, n2)
        >>> e.eval()
        True
        >>> n1 = Num(3)
        >>> n2 = Num(3)
        >>> e = Leq(n1, n2)
        >>> e.eval()
        True
        >>> n1 = Num(4)
        >>> n2 = Num(3)
        >>> e = Leq(n1, n2)
        >>> e.eval()
        False
        """
        return self.left.eval(env) <= self.right.eval(env)

class Lth(BinaryExpression):
    """
    This class represents comparison of two expressions using the
    less-than comparison operator. The evaluation of such an expression is a
    boolean value that is true if the left operand is less than the right
    operand. It is false otherwise.
    """
    def eval(self, env=None):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Lth(n1, n2)
        >>> e.eval()
        True
        >>> n1 = Num(3)
        >>> n2 = Num(3)
        >>> e = Lth(n1, n2)
        >>> e.eval()
        False
        >>> n1 = Num(4)
        >>> n2 = Num(3)
        >>> e = Lth(n1, n2)
        >>> e.eval()
        False
        """
        return self.left.eval(env) < self.right.eval(env)

class UnaryExpression(Expression):
    """
    This class represents unary expressions. A unary expression has only one
    sub-expression.
    """
    def __init__(self, exp):
        self.exp = exp

    @abstractmethod
    def eval(self, env=None):
        raise NotImplementedError

class Neg(UnaryExpression):
    """
    This expression represents the additive inverse of a number. The additive
    inverse of a number n is the number -n, so that the sum of both is zero.
    """
    def eval(self, env=None):
        """
        Example:
        >>> n = Num(3)
        >>> e = Neg(n)
        >>> e.eval()
        -3
        >>> n = Num(0)
        >>> e = Neg(n)
        >>> e.eval()
        0
        """
        return -self.exp.eval(env)

class Not(UnaryExpression):
    """
    This expression represents the negation of a boolean. The negation of a
    boolean expression is the logical complement of that expression.
    """
    def eval(self, env=None):
        """
        Example:
        >>> t = Bln(True)
        >>> e = Not(t)
        >>> e.eval()
        False
        >>> t = Bln(False)
        >>> e = Not(t)
        >>> e.eval()
        True
        """
        return not self.exp.eval(env)

class Var(Expression):
    def __init__(self, name):
        self.name = name

    def eval(self, env=None):
        """
        Example:
        >>> env = {'x': 10}
        >>> v = Var('x')
        >>> v.eval(env)
        10

        >>> env = {'y': False}
        >>> v = Var('y')
        >>> v.eval(env)
        False

        >>> env = {}
        >>> v = Var('z')
        >>> v.eval(env)
        Traceback (most recent call last):
        ...
        ValueError: Variavel inexistente z
        """
        if self.name in env:
            return env[self.name]
        else:
            raise ValueError(f"Variavel inexistente {self.name}")

class Let(Expression):
    def __init__(self, var_name, value_expr, body_expr):
        self.var_name = var_name
        self.value_expr = value_expr
        self.body_expr = body_expr

    def eval(self, env=None):
        """
        Example:
        >>> env = {}
        >>> let_expr = Let("x", Num(5), Add(Var("x"), Num(3)))
        >>> let_expr.eval(env)
        8

        >>> env = {'y': 10}
        >>> let_expr = Let("x", Num(7), Mul(Var("x"), Var("y")))
        >>> let_expr.eval(env)
        70

        >>> env = {}
        >>> let_expr = Let("a", Num(2), Let("b", Num(3), Add(Var("a"), Var("b"))))
        >>> let_expr.eval(env)
        5

        >>> env = {'x': 4}
        >>> let_expr = Let("x", Num(10), Var("x"))
        >>> let_expr.eval(env)
        10

        >>> env = {}
        >>> let_expr = Let("x", Num(5), Leq(Var("x"), Num(10)))
        >>> let_expr.eval(env)
        True
        """
        val = self.value_expr.eval(env)
        new_env = dict(env) if env is not None else {}
        new_env[self.var_name] = val
        return self.body_expr.eval(new_env)