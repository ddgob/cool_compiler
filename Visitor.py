import sys
from abc import ABC, abstractmethod
from Expression import *

class Visitor(ABC):
    """
    The visitor pattern consists of two abstract classes: the Expression and the
    Visitor. The Expression class defines on method: 'accept(visitor, args)'.
    This method takes in an implementation of a visitor, and the arguments that
    are passed from expression to expression. The Visitor class defines one
    specific method for each subclass of Expression. Each instance of such a
    subclasse will invoke the right visiting method.
    """

    @abstractmethod
    def visit_var(self, exp, arg):
        pass

    @abstractmethod
    def visit_bln(self, exp, arg):
        pass

    @abstractmethod
    def visit_num(self, exp, arg):
        pass

    @abstractmethod
    def visit_eql(self, exp, arg):
        pass

    @abstractmethod
    def visit_and(self, exp, arg):
        pass

    @abstractmethod
    def visit_or(self, exp, arg):
        pass

    @abstractmethod
    def visit_add(self, exp, arg):
        pass

    @abstractmethod
    def visit_sub(self, exp, arg):
        pass

    @abstractmethod
    def visit_mul(self, exp, arg):
        pass

    @abstractmethod
    def visit_div(self, exp, arg):
        pass

    @abstractmethod
    def visit_leq(self, exp, arg):
        pass

    @abstractmethod
    def visit_lth(self, exp, arg):
        pass

    @abstractmethod
    def visit_neg(self, exp, arg):
        pass

    @abstractmethod
    def visit_not(self, exp, arg):
        pass

    @abstractmethod
    def visit_let(self, exp, arg):
        pass

    @abstractmethod
    def visit_ifThenElse(self, exp, arg):
        pass

    @abstractmethod
    def visit_fn(self, exp, arg):
        pass

    @abstractmethod
    def visit_app(self, exp, arg):
        pass


class Function():
    """
    This is the class that represents functions. This class lets us distinguish
    the three types that now exist in the language: numbers, booleans and
    functions. Notice that the evaluation of an expression can now be a
    function. For instance:

        >>> f = Fn('v', Mul(Var('v'), Var('v')))
        >>> ev = EvalVisitor()
        >>> fval = f.accept(ev, {})
        >>> type(fval)
        <class 'Visitor.Function'>
    """
    def __init__(self, formal, body, env):
        self.formal = formal
        self.body = body
        self.env = env
    def __str__(self):
        return f"Fn({self.formal})"


class EvalVisitor(Visitor):
    """
    The EvalVisitor class evaluates logical and arithmetic expressions. The
    result of evaluating an expression is the value of that expression. The
    inherited attribute propagated throughout visits is the environment that
    associates the names of variables with values.

    Examples:
    >>> e0 = Let('v', Add(Num(40), Num(2)), Mul(Var('v'), Var('v')))
    >>> e1 = Not(Eql(e0, Num(1764)))
    >>> ev = EvalVisitor()
    >>> e1.accept(ev, {})
    False

    >>> e0 = Let('v', Add(Num(40), Num(2)), Sub(Var('v'), Num(2)))
    >>> e1 = Lth(e0, Var('x'))
    >>> ev = EvalVisitor()
    >>> e1.accept(ev, {'x': 41})
    True
    """

    def check_type(self, val, expected_type):
        if not type(val) == expected_type:
            sys.exit("Type error")

    def visit_var(self, exp, env):
        if exp.identifier in env:
            return env[exp.identifier]
        else:
            sys.exit(f"Def error")

    def visit_bln(self, exp, env):
        return exp.bln

    def visit_num(self, exp, env):
        return exp.num

    def visit_eql(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        if type(left) == int:
            self.check_type(right, int)
        elif type(left) == bool:
            self.check_type(right, bool)
        else:
            sys.exit("Type error")
        return left == right

    def visit_add(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        self.check_type(left, int)
        self.check_type(right, int)
        return left + right

    def visit_sub(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        self.check_type(left, int)
        self.check_type(right, int)
        return left - right

    def visit_mul(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        self.check_type(left, int)
        self.check_type(right, int)
        return left * right

    def visit_div(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        self.check_type(left, int)
        self.check_type(right, int)
        return left // right

    def visit_leq(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        self.check_type(left, int)
        self.check_type(right, int)
        return left <= right

    def visit_lth(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        self.check_type(left, int)
        self.check_type(right, int)
        return left < right

    def visit_neg(self, exp, env):
        eval = exp.exp.accept(self, env)
        self.check_type(eval, int)
        return -eval

    def visit_not(self, exp, env):
        eval = exp.exp.accept(self, env)
        self.check_type(eval, bool)
        return not eval

    def visit_let(self, exp, env):
        def_val = exp.exp_def.accept(self, env)
        updated_env = dict(env)
        updated_env[exp.identifier] = def_val
        return exp.exp_body.accept(self, updated_env)
    
    def visit_ifThenElse(self, exp, env):
        condition = exp.cond.accept(self, env)
        self.check_type(condition, bool)
        if condition:
            return exp.e0.accept(self, env)
        else:
            return exp.e1.accept(self, env)
    
    def visit_and(self, exp, env):
        left = exp.left.accept(self, env)
        self.check_type(left, bool)
        # Short circuit and 
        if left:
            right = exp.right.accept(self, env)
            self.check_type(right, bool)
            return right
        return False

    def visit_or(self, exp, env):
        left = exp.left.accept(self, env)
        self.check_type(left, bool)
        # Short circuit or
        if left: 
            return True
        right = exp.right.accept(self, env)
        self.check_type(right, bool)
        return right

    def visit_fn(self, exp, env): # Implemented for you :)
        """
        The evaluation of a function is the function itself. Remember: in our
        language, functions are values as well. So, now we have three kinds of
        values: numbers, booleans and functions.
        """
        return Function(exp.formal, exp.body, env)

    def visit_app(self, exp, env):
        """
        Here comes most of the complexity of the homework, in five or six lines
        of code! You must implement the evaluation of a function application.
        """
        fval = exp.function.accept(self, env)
        if not isinstance(fval, Function):
            sys.exit('Expected function during application')
        pval = exp.actual.accept(self, env)
        new_env = dict(fval.env)
        new_env[fval.formal] = pval
        return fval.body.accept(self, new_env)


class UseDefVisitor(Visitor):
    """
    The UseDefVisitor class reports the use of undefined variables. It takes
    as input an environment of defined variables, and produces, as output,
    the set of all the variables that are used without being defined.

    Examples:
    >>> e0 = Let('v', Add(Num(40), Num(2)), Mul(Var('v'), Var('v')))
    >>> e1 = Not(Eql(e0, Num(1764)))
    >>> ev = UseDefVisitor()
    >>> len(e1.accept(ev, set()))
    0

    >>> e0 = Let('v', Add(Num(40), Num(2)), Sub(Var('v'), Num(2)))
    >>> e1 = Lth(e0, Var('x'))
    >>> ev = UseDefVisitor()
    >>> len(e1.accept(ev, set()))
    1

    >>> e = Let('v', Add(Num(40), Var('v')), Sub(Var('v'), Num(2)))
    >>> ev = UseDefVisitor()
    >>> len(e.accept(ev, set()))
    1

    >>> e1 = Let('v', Add(Num(40), Var('v')), Sub(Var('v'), Num(2)))
    >>> e0 = Let('v', Num(3), e1)
    >>> ev = UseDefVisitor()
    >>> len(e0.accept(ev, set()))
    0
    """

    def visit_var(self, exp, env):
        if exp.identifier not in env:
            return set([exp.identifier])
        return set()

    def visit_bln(self, exp, env):
        return set()

    def visit_num(self, exp, env):
        return set()

    def visit_eql(self, exp, env):
        return exp.left.accept(self, env) | exp.right.accept(self, env)

    def visit_add(self, exp, env):
        return exp.left.accept(self, env) | exp.right.accept(self, env)

    def visit_sub(self, exp, env):
        return exp.left.accept(self, env) | exp.right.accept(self, env)

    def visit_mul(self, exp, env):
        return exp.left.accept(self, env) | exp.right.accept(self, env)

    def visit_div(self, exp, env):
        return exp.left.accept(self, env) | exp.right.accept(self, env)
    
    def visit_and(self, exp, env):
        return exp.left.accept(self, env) | exp.right.accept(self, env)
    
    def visit_or(self, exp, env):
        return exp.left.accept(self, env) | exp.right.accept(self, env)

    def visit_leq(self, exp, env):
        return exp.left.accept(self, env) | exp.right.accept(self, env)

    def visit_lth(self, exp, env):
        return exp.left.accept(self, env) | exp.right.accept(self, env)

    def visit_neg(self, exp, env):
        return exp.exp.accept(self, env)

    def visit_not(self, exp, env):
        return exp.exp.accept(self, env)

    def visit_ifThenElse(self, exp, env):
        return exp.cond.accept(self, env) | exp.e0.accept(self, env) | exp.e1.accept(self, env)

    def visit_let(self, exp, env):
        u_def = exp.exp_def.accept(self, env)
        updated_env = dict(env)
        updated_env[exp.identifier] = None
        u_body = exp.exp_body.accept(self, updated_env)
        return u_def | u_body

def safe_eval(exp):
    """
    This method applies one simple semantic analysis onto an expression, before
    evaluating it: it checks if the expression contains free variables, there
    is, variables used without being defined.

    Example:
    >>> e0 = Let('v', Add(Num(40), Num(2)), Mul(Var('v'), Var('v')))
    >>> e1 = Not(Eql(e0, Num(1764)))
    >>> safe_eval(e1)
    Value is False

    >>> e0 = Let('v', Add(Num(40), Num(2)), Sub(Var('v'), Num(2)))
    >>> e1 = Lth(e0, Var('x'))
    >>> safe_eval(e1)
    Error: expression contains undefined variables.
    """
    use_def_visitor = UseDefVisitor()
    if len(exp.accept(use_def_visitor, set())) > 0:
        print("Error: expression contains undefined variables.")
    else:
        eval_visitor = EvalVisitor()
        print(f"Value is {exp.accept(eval_visitor, {})}")


class CtrGenVisitor(Visitor):
    """
    This visitor creates constraints for a type-inference engine. Basically,
    it traverses the abstract-syntax tree of expressions, producing pairs like
    (type0, type1) on the way. A pair like (type0, type1) indicates that these
    two type variables are the same.

    Examples:
        >>> e = Let('v', Num(40), Let('w', Num(2), Add(Var('v'), Var('w'))))
        >>> ev = CtrGenVisitor()
        >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
        ["('TV_1', 'TV_2')", "('TV_2', 'TV_3')", "('v', <class 'int'>)", "('w', <class 'int'>)", "(<class 'int'>, 'TV_3')", "(<class 'int'>, 'v')", "(<class 'int'>, 'w')"]
    """

    def __init__(self):
        self.fresh_type_counter = 0

    def fresh_type_var(self):
        """
        Create a new type var using the current value of the fresh_type_counter.
        Two successive calls to this method will return different type names.
        Notice that the name of a type variable is always TV_x, where x is
        some integer number. That means that probably we would run into
        errors if someone declares a variable called, say, TV_1 or TV_2, as in
        "let TV_1 <- 1 in TV_1 end". But you can assume that such would never
        happen in the test cases. In practice, we should define a new class
        to represent type variables. But let's keep the implementation as
        simple as possible.

        Example:
            >>> ev = CtrGenVisitor()
            >>> [ev.fresh_type_var(), ev.fresh_type_var()]
            ['TV_1', 'TV_2']
        """
        self.fresh_type_counter += 1
        return f"TV_{self.fresh_type_counter}"

    """
    The CtrGenVisitor class creates constraints that, once solved, will give
    us the type of the different variables. Every accept method takes in
    two arguments (in addition to self):
    
    exp: is the expression that is being analyzed.
    type_var: that is a name that works as a placeholder for the type of the
    expression. Whenever we visit a new expression, we create a type variable
    to represent its type (you can do that with the method fresh_type_var).
    The only exception is the type of Var expressions. In this case, the type
    of a Var expression is the identifier of that expression.
    """

    def visit_var(self, exp, type_var):
        """
        Example:
            >>> e = Var('v')
            >>> ev = CtrGenVisitor()
            >>> e.accept(ev, ev.fresh_type_var())
            {('v', 'TV_1')}
        """
        return {(exp.identifier, type_var)}

    def visit_bln(self, exp, type_var):
        """
        Example:
            >>> e = Bln(True)
            >>> ev = CtrGenVisitor()
            >>> e.accept(ev, ev.fresh_type_var())
            {(<class 'bool'>, 'TV_1')}
        """
        return {(type(True), type_var)}

    def visit_num(self, exp, type_var):
        """
        Example:
            >>> e = Num(1)
            >>> ev = CtrGenVisitor()
            >>> e.accept(ev, ev.fresh_type_var())
            {(<class 'int'>, 'TV_1')}
        """
        return {(type(1), type_var)}

    def visit_eql(self, exp, type_var):
        """
        Example:
            >>> e = Eql(Num(1), Bln(True))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'bool'>, 'TV_1')", "(<class 'bool'>, 'TV_2')", "(<class 'int'>, 'TV_2')"]

        Notice that if we have repeated constraints, they only appear once in
        the set of constraints (after all, it's a set!). As an example, we
        would have two occurrences of the pair (TV_2, int) in the following
        example:
            >>> e = Eql(Num(1), Num(2))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'bool'>, 'TV_1')", "(<class 'int'>, 'TV_2')"]
        """
        fresh_type = self.fresh_type_var()
        left_cnstrnt = exp.left.accept(self, fresh_type)
        right_cnstrnt = exp.right.accept(self, fresh_type)
        return left_cnstrnt | right_cnstrnt | {(type(True), type_var)}

    def visit_and(self, exp, type_var):
        """
        Example:
            >>> e = And(Bln(False), Bln(True))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'bool'>, 'TV_1')", "(<class 'bool'>, <class 'bool'>)"]

        In the above example, notice that we ended up getting a trivial
        constraint, e.g.: (<class 'bool'>, <class 'bool'>). That's alright:
        don't worry about these trivial constraints at this point. We can
        remove them from the set of constraints later on, when we try to
        solve them.
        """
        left_cnstrnt = exp.left.accept(self, type(True))
        right_cnstrnt = exp.right.accept(self, type(True))
        return left_cnstrnt | right_cnstrnt | {(type(True), type_var)}

    def visit_or(self, exp, type_var):
        """
        Example:
            >>> e = Or(Bln(False), Bln(True))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'bool'>, 'TV_1')", "(<class 'bool'>, <class 'bool'>)"]
        """
        left_cnstrnt = exp.left.accept(self, type(True))
        right_cnstrnt = exp.right.accept(self, type(True))
        return left_cnstrnt | right_cnstrnt | {(type(True), type_var)}

    def visit_add(self, exp, type_var):
        """
        Example:
            >>> e = Add(Num(1), Num(2))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'int'>, 'TV_1')", "(<class 'int'>, <class 'int'>)"]
        """
        left_cnstrnt = exp.left.accept(self, type(1))
        right_cnstrnt = exp.right.accept(self, type(1))
        return left_cnstrnt | right_cnstrnt | {(type(1), type_var)}

    def visit_sub(self, exp, type_var):
        """
        Example:
            >>> e = Sub(Num(1), Num(2))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'int'>, 'TV_1')", "(<class 'int'>, <class 'int'>)"]
        """
        left_cnstrnt = exp.left.accept(self, type(1))
        right_cnstrnt = exp.right.accept(self, type(1))
        return left_cnstrnt | right_cnstrnt | {(type(1), type_var)}

    def visit_mul(self, exp, type_var):
        """
        Example:
            >>> e = Mul(Num(1), Num(2))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'int'>, 'TV_1')", "(<class 'int'>, <class 'int'>)"]
        """
        left_cnstrnt = exp.left.accept(self, type(1))
        right_cnstrnt = exp.right.accept(self, type(1))
        return left_cnstrnt | right_cnstrnt | {(type(1), type_var)}

    def visit_div(self, exp, type_var):
        """
        Example:
            >>> e = Div(Num(1), Num(2))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'int'>, 'TV_1')", "(<class 'int'>, <class 'int'>)"]
        """
        left_cnstrnt = exp.left.accept(self, type(1))
        right_cnstrnt = exp.right.accept(self, type(1))
        return left_cnstrnt | right_cnstrnt | {(type(1), type_var)}

    def visit_leq(self, exp, type_var):
        """
        Example:
            >>> e = Leq(Num(1), Num(2))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'bool'>, 'TV_1')", "(<class 'int'>, <class 'int'>)"]
        """
        left_cnstrnt = exp.left.accept(self, type(1))
        right_cnstrnt = exp.right.accept(self, type(1))
        return left_cnstrnt | right_cnstrnt | {(type(True), type_var)}

    def visit_lth(self, exp, type_var):
        """
        Example:
            >>> e = Lth(Num(1), Num(2))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'bool'>, 'TV_1')", "(<class 'int'>, <class 'int'>)"]
        """
        left_cnstrnt = exp.left.accept(self, type(1))
        right_cnstrnt = exp.right.accept(self, type(1))
        return left_cnstrnt | right_cnstrnt | {(type(True), type_var)}

    def visit_neg(self, exp, type_var):
        """
        Example:
            >>> e = Neg(Num(1))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'int'>, 'TV_1')", "(<class 'int'>, <class 'int'>)"]
        """
        return exp.exp.accept(self, type(1)) | {(type(1), type_var)}

    def visit_not(self, exp, type_var):
        """
        Example:
            >>> e = Not(Bln(True))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'bool'>, 'TV_1')", "(<class 'bool'>, <class 'bool'>)"]
        """
        return exp.exp.accept(self, type(True)) | {(type(True), type_var)}

    def visit_let(self, exp, type_var):
        """
        Example:
            >>> e = Let('v', Num(42), Var('v'))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["('TV_1', 'TV_2')", "('v', 'TV_2')", "(<class 'int'>, 'v')"]
        """
        def_cnstrnt = exp.exp_def.accept(self, exp.identifier)
        fresh_type = self.fresh_type_var()
        body_cnstrnt = exp.exp_body.accept(self, fresh_type)
        return def_cnstrnt | body_cnstrnt | {(type_var, fresh_type)}

    def visit_ifThenElse(self, exp, type_var):
        """
        Example:
            >>> e = IfThenElse(Bln(True), Num(42), Num(30))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["('TV_1', 'TV_2')", "(<class 'bool'>, <class 'bool'>)", "(<class 'int'>, 'TV_2')"]
        """
        cond_cnstrnt = exp.cond.accept(self, type(True))
        fresh_type = self.fresh_type_var()
        e0_cnstrnt = exp.e0.accept(self, fresh_type)
        e1_cnstrnt = exp.e1.accept(self, fresh_type)
        return cond_cnstrnt | e0_cnstrnt | e1_cnstrnt | {(type_var, fresh_type)}