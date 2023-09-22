from src.socket.server_threaded import TranslateServer


def main() -> int:
    TranslateServer().serve()
    return 0

if __name__ == '__main__':
    main()
