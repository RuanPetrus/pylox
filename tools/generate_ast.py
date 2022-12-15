#!/usr/bin/env python3
import sys


EXPR_LIST = [
    "Binary: Expr left, Token operator, Expr right",
    "Grouping : Expr expression",
    "Literal: Any value",
    "Unary: Token operator, Expr right",
]
TAB = "    "


def main():
    outputDir = sys.argv[1]
    defineAst(outputDir, "Expr", EXPR_LIST)


def defineAst(outputDir: str, base_name: str, types: list[str]):
    path = outputDir + "/" + base_name.lower() + ".py"
    with open(path, "w") as f:
        write_imports(f)
        write_base_class(f, base_name)
        classes = []

        for t in types:
            class_name = t.split(":")[0].strip()
            classes.append(class_name)

            c_args = t.split(":")[1]
            class_args = []
            for a in c_args.split(","):
                list_a = a.split()
                class_args.append((list_a[0].strip(), list_a[1].strip()))

            print(class_args)
            write_ast_class(f, base_name, class_name, class_args)

        write_visitors(f, base_name, classes)


def write_imports(f) -> None:
    f.write("from pylox_token import Token\n")
    f.write("from abc import ABC, abstractmethod\n")
    f.write("from typing import Protocol, Any\n")
    f.write("\n\n")


def write_base_class(f, base_name: str):
    f.write(f"class {base_name}(ABC):\n")
    f.write(f"{TAB}@abstractmethod\n")
    f.write(f"{TAB}def accept(visitor: ExprVisitor) -> Any:\n")
    f.write(f"{TAB}{TAB}pass\n")
    f.write("\n\n")


def write_ast_class(
    f, base_name: str, class_name: str, class_args: list[tuple[str, str]]
):
    arg_list = ", ".join(
        [arg_name + ": " + arg_type for arg_type, arg_name in class_args]
    )

    f.write(f"class {class_name + base_name}({base_name}):\n")
    f.write(f"{TAB}def __init__(self, {arg_list}):\n")

    for a in class_args:
        f.write(f"{TAB}{TAB}self.{a[1]} = {a[1]}\n")

    f.write("\n")
    f.write(f"{TAB}def accept(self, visitor: {base_name}Visitor) -> Any:\n")
    f.write(f"{TAB}{TAB}return visitor.visit{class_name}{base_name}(self)\n")
    f.write("\n\n")


def write_visitors(f, base_name: str, classes: list[str]):
    f.write(f"class {base_name}Visitor(Protocol):\n")

    for a in classes:
        f.write(
            f"{TAB}def visit{a}{base_name}(self, {base_name.lower()}: {a + base_name}) -> Any:\n"
        )

        f.write(f"{TAB}{TAB}...\n")

    f.write("\n\n")


if __name__ == "__main__":
    main()
