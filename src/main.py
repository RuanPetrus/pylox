import sys
from scanner import Scanner


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
        scanner = Scanner(ErrorCtx, source)
        tokens = scanner.scanTokens()

        for token in tokens:
            print(token)


class ErrorCtx:
    @staticmethod
    def error(line: int, message: str):
        ErrorCtx._report(line, "", message)

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
