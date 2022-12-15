#!/usr/bin/env python3
from pylox_token import Token
from abc import ABC, abstractmethod

from typing import Protocol, Any


class Expr(ABC):
    @abstractmethod
    def accept(visitor) -> Any:
        pass


class BinaryExpr(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.right = right
        self.operator = operator

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitBinaryExpr(self)


class ExprVisitor(Protocol):
    def visitBinaryExpr(self, expr: BinaryExpr) -> Any:
        ...
