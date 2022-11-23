from hello.hello import Hello


def main() -> None:
    hello = Hello("abc")
    hello.greet()


if __name__ == "__main__":
    main()
