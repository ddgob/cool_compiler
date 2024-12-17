import sys
from abc import ABC, abstractmethod
from Expression import *
import Asm as AsmModule


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


class GenVisitor(Visitor):
    def __init__(self):
        self.label_counter = 0

    def new_var(self):
        self.label_counter += 1
        return f"v{self.label_counter}"

    def visit_var(self, exp, prog):
        return exp.identifier

    def visit_bln(self, exp, prog):
        reg = self.new_var()
        val = 1 if exp.bln else 0
        prog.add_inst(AsmModule.Addi(reg, "x0", val))
        return reg

    def visit_num(self, exp, prog):
        reg = self.new_var()
        prog.add_inst(AsmModule.Addi(reg, "x0", exp.num))
        return reg

    def compute_equality(self, lhs_reg, rhs_reg, prog):
        delta = self.new_var()
        cond1 = self.new_var()
        cond2 = self.new_var()
        equal_reg = self.new_var()

        prog.add_inst(AsmModule.Sub(delta, lhs_reg, rhs_reg))
        prog.add_inst(AsmModule.Slti(cond1, delta, 1))
        prog.add_inst(AsmModule.Slti(cond2, delta, 0))
        prog.add_inst(AsmModule.Xor(equal_reg, cond1, cond2))
        return equal_reg

    def visit_eql(self, exp, prog):
        lhs = exp.left.accept(self, prog)
        rhs = exp.right.accept(self, prog)
        return self.compute_equality(lhs, rhs, prog)

    def visit_add(self, exp, prog):
        lhs = exp.left.accept(self, prog)
        rhs = exp.right.accept(self, prog)
        result_reg = self.new_var()
        prog.add_inst(AsmModule.Add(result_reg, lhs, rhs))
        return result_reg

    def visit_sub(self, exp, prog):
        lhs = exp.left.accept(self, prog)
        rhs = exp.right.accept(self, prog)
        result_reg = self.new_var()
        prog.add_inst(AsmModule.Sub(result_reg, lhs, rhs))
        return result_reg

    def visit_mul(self, exp, prog):
        lhs = exp.left.accept(self, prog)
        rhs = exp.right.accept(self, prog)
        result_reg = self.new_var()
        prog.add_inst(AsmModule.Mul(result_reg, lhs, rhs))
        return result_reg

    def visit_div(self, exp, prog):
        lhs = exp.left.accept(self, prog)
        rhs = exp.right.accept(self, prog)
        result_reg = self.new_var()
        prog.add_inst(AsmModule.Div(result_reg, lhs, rhs))
        return result_reg

    def visit_lth(self, exp, prog):
        lhs = exp.left.accept(self, prog)
        rhs = exp.right.accept(self, prog)
        result_reg = self.new_var()
        prog.add_inst(AsmModule.Slt(result_reg, lhs, rhs))
        return result_reg

    def visit_leq(self, exp, prog):
        lhs = exp.left.accept(self, prog)
        rhs = exp.right.accept(self, prog)
        less_reg = self.new_var()
        eq_reg = self.compute_equality(lhs, rhs, prog)
        prog.add_inst(AsmModule.Slt(less_reg, lhs, rhs))
        leq_reg = self.new_var()
        prog.add_inst(AsmModule.Add(leq_reg, less_reg, eq_reg))
        return leq_reg

    def visit_neg(self, exp, prog):
        value_reg = exp.exp.accept(self, prog)
        result_reg = self.new_var()
        prog.add_inst(AsmModule.Sub(result_reg, "x0", value_reg))
        return result_reg

    def visit_not(self, exp, prog):
        value_reg = exp.exp.accept(self, prog)
        return self.compute_equality(value_reg, "x0", prog)

    def visit_let(self, exp, prog):
        init_value = exp.exp_def.accept(self, prog)
        prog.add_inst(AsmModule.Add(exp.identifier, init_value, "x0"))
        body_value = exp.exp_body.accept(self, prog)
        return body_value