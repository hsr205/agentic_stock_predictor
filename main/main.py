from config.config import settings



def main() -> int:
    print(f"Hello from {__name__}")
    print(f"settings.app_name = {settings.app_name}")

    return 0


if __name__ == "__main__":
    main()
