from services.retriver.manager import FetcherManager


def run():
    manager = FetcherManager()
    manager.main()

if __name__ == "__main__":
    run()