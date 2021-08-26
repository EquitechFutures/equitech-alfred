import json
import os

from dotenv import load_dotenv

from alfred import Alfred


def print_share_summary(share_result):
    print("-" * 100)
    print(f'{"Page Name":<50}{"New Role":<20}{"Assigned To":<60}')
    print("-" * 100)
    for result in share_result:
        print(
            f'{result["page_name"]:<50}{result["new_role"]:<20}{str(result["assigned"]):<60}'
        )
    print("-" * 100)


def load_config(path):
    with open(path) as fp:
        return json.load(fp)


def main():
    load_dotenv()
    test_run = os.getenv("ALFRED_TEST", "false").lower() == "true"

    alfred_config = load_config("./config.json")
    template_db = alfred_config["db_template"]
    target_db = (
        alfred_config["db_assignment"] if not test_run else alfred_config["db_test"]
    )

    alfred = Alfred(token_v2=os.getenv("NOTION_TOKEN"))
    alfred.assign_all(template_db, target_db, user_ids=alfred_config["user_ids"])

    share_result = alfred.auto_share_pages(target_db)
    print_share_summary(share_result)

    print("Done")


if __name__ == "__main__":
    main()
