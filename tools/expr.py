from pylox_token import Token
from abc import ABC, abstractmethod
from typing import Protocol, Any


class Expr(ABC):
    @abstractmethod
    def accept(visitor: ExprVisitor) -> Any:
        pass


class BinaryExpr(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitBinaryExpr(self)


class GroupingExpr(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitGroupingExpr(self)


class LiteralExpr(Expr):
    def __init__(self, value: Any):
        self.value = value

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitLiteralExpr(self)


class UnaryExpr(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitUnaryExpr(self)


class ExprVisitor(Protocol):
    def visitBinaryExpr(self, expr: BinaryExpr) -> Any:
        ...
    def visitGroupingExpr(self, expr: GroupingExpr) -> Any:
        ...
    def visitLiteralExpr(self, expr: LiteralExpr) -> Any:
        ...
    def visitUnaryExpr(self, expr: UnaryExpr) -> Any:
        ...


