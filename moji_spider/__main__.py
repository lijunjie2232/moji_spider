from tortoise import run_async

from .handler import offical_folder_to_db, share_folder_to_db


def main():
    run_async(share_folder_to_db())
    run_async(offical_folder_to_db())


if __name__ == "__main__":
    main()
