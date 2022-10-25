import sys
from enum import Enum, auto

from typing import Any, List


class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()

    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens.
    BANG = auto()
    BANG_EQUAL = auto()

    EQUAL = auto()
    EQUAL_EQUAL = auto()

    GREATER = auto()
    GREATER_EQUAL = auto()

    LESS = auto()
    LESS_EQUAL = auto()

    # Literals.
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords.
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()

    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: Any, line: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f"{self.token_type} {self.lexeme} {self.literal}"


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []

        self.keywords = {}
        self.keywords["and"] = TokenType.AND
        self.keywords["class"] = TokenType.CLASS
        self.keywords["else"] = TokenType.ELSE
        self.keywords["false"] = TokenType.FALSE
        self.keywords["for"] = TokenType.FOR
        self.keywords["fun"] = TokenType.FUN
        self.keywords["if"] = TokenType.IF
        self.keywords["nil"] = TokenType.NIL
        self.keywords["or"] = TokenType.OR
        self.keywords["print"] = TokenType.PRINT
        self.keywords["return"] = TokenType.RETURN
        self.keywords["super"] = TokenType.SUPER
        self.keywords["this"] = TokenType.THIS
        self.keywords["true"] = TokenType.TRUE
        self.keywords["var"] = TokenType.VAR
        self.keywords["while"] = TokenType.WHILE

    def scanTokens(self) -> List[Token]:
        while not self._isAtEnd():
            self.start = self.current
            self._scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

        return self.tokens

    def _isAtEnd(self) -> bool:
        return self.current >= len(self.source)

    def _scanToken(self):
        c = self._advance()
        if c == "(":
            self._addSimpleToken(TokenType.LEFT_PAREN)
        elif c == ")":
            self._addSimpleToken(TokenType.RIGHT_PAREN)
        elif c == "{":
            self._addSimpleToken(TokenType.LEFT_BRACE)
        elif c == "}":
            self._addSimpleToken(TokenType.RIGHT_BRACE)
        elif c == ",":
            self._addSimpleToken(TokenType.COMMA)
        elif c == ".":
            self._addSimpleToken(TokenType.DOT)
        elif c == "-":
            self._addSimpleToken(TokenType.MINUS)
        elif c == "+":
            self._addSimpleToken(TokenType.PLUS)
        elif c == ";":
            self._addSimpleToken(TokenType.SEMICOLON)
        elif c == "*":
            self._addSimpleToken(TokenType.STAR)

        elif c == "!":
            self._addSimpleToken(
                TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
            )
        elif c == "=":
            self._addSimpleToken(
                TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
            )
        elif c == "<":
            self._addSimpleToken(
                TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
            )
        elif c == ">":
            self._addSimpleToken(
                TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
            )

        elif c == "/":
            if self._match("/"):
                # A comment goes until the end of the line
                while self._peek() != "\n" and not self._isAtEnd():
                    self._advance()

            elif self._match("*"):
                while (
                    self._peek() != "*"
                    and self._peekNext() != "/"
                    and not self._isAtEnd()
                ):
                    if self._peek() == "\n":
                        self.line += 1

                    self._advance()

                self.current += 2  # Consuming the */

            else:
                self._addSimpleToken(TokenType.SLASH)

        elif c == " ":
            pass
        elif c == "\r":
            pass
        elif c == "\t":
            pass
        elif c == "\n":
            self.line += 1

        elif c == '"':
            self._string()

        else:
            if Scanner._isDigit(c):
                self._number()

            elif Scanner._isAlpha(c):
                self._identifier()

            else:
                Pylox.error(self.line, f"Unexpected character: {c}.")

    def _identifier(self):
        while Scanner._isAlphaNumeric(self._peek()):
            self._advance()

        token_type = self.keywords.get(self.source[self.start : self.current])

        if token_type is None:
            token_type = TokenType.IDENTIFIER

        self._addSimpleToken(token_type)

    def _number(self):
        while self._isDigit(self._peek()):
            self._advance()

        if self._peek() == "." and Scanner._isDigit(self._peekNext()):
            self._advance()

            while Scanner._isDigit(self._peek()):
                self._advance()

        self._addToken(TokenType.NUMBER, float(self.source[self.start : self.current]))

    @staticmethod
    def _isDigit(c: str) -> bool:
        return "0" <= c <= "9"

    @staticmethod
    def _isAlpha(c: str) -> bool:
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"

    @staticmethod
    def _isAlphaNumeric(c: str) -> bool:
        return Scanner._isAlpha(c) or Scanner._isDigit(c)

    def _string(self):
        while self._peek() != '"' and not self._isAtEnd():
            if self._peek() == "\n":
                self.line += 1
            self._advance()

        if self._isAtEnd():
            Pylox.error(self.line, "Unterminated string.")
            return

        self._advance()
        value = self.source[self.start + 1 : self.current - 1]
        self._addToken(TokenType.STRING, value)

    def _peekNext(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"

        return self.source[self.current + 1]

    def _peek(self) -> str:
        if self._isAtEnd():
            return "\0"

        return self.source[self.current]

    def _advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def _addSimpleToken(self, token_type: TokenType):
        self._addToken(token_type, None)

    def _addToken(self, token_type: TokenType, literal: Any):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def _match(self, expected: str) -> bool:
        if self._isAtEnd():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True


class Pylox:
    hadError = False

    @staticmethod
    def runFile(file_path: str):
        with open(file_path, "r") as f:
            src = f.read()

        if Pylox.hadError:
            exit(65)

        Pylox.run(src)

    @staticmethod
    def runPrompt():
        while True:
            print(">", end=" ")
            line = input()

            if not line:
                break

            Pylox.run(line)
            Pylox.hadError = False

    @staticmethod
    def run(source: str):
        scanner = Scanner(source)
        tokens = scanner.scanTokens()

        for token in tokens:
            print(token)

    @staticmethod
    def error(line: int, message: str):
        Pylox._report(line, "", message)

    @staticmethod
    def _report(line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}")
        Pylox.hadError = True


def main():
    if len(sys.argv) > 2:
        print("Usage: pylox [script]")
        exit(64)

    elif len(sys.argv) == 2:
        Pylox.runFile(sys.argv[1])

    else:
        Pylox.runPrompt()


if __name__ == "__main__":
    main()
