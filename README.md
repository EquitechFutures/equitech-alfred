# EquiTech Alfred

Alfred simplifies the process of handing out course assignments on Notion.

At its core, Alfred duplicates Notion blocks across databases and auto-shares page with correct permissions. It can also disable read-write-access after a particular date & time.

Developed for EquiTech Future's [Global Summer Institute 2021](https://www.equitechfutures.com/gsi)

## Setup

Install python dependencies

    pip install -r ./notion/requirements.txt
    pip install -r ./requirements.txt

## Usage

### Notion

You need to setup two Notion databases

1. Template Database ([Notion template](https://precious-shroud-805.notion.site/d337bf0dff1143e1b36a47e0aebf3768?v=b0f2704baa3b49ed92be9b296a1cb0d3)) - This is where you'll create a page/template that you want to duplicate
2. Target Database ([Notion template](https://precious-shroud-805.notion.site/fe21bd2e3ecd4c20b01c9e62c9c94896?v=d59acf7100a341a38ca2519d17fe8353)) - This is where the pages will be copied & shared for each user.

### Alfred Configuration

Create a config file called `config.json` and fill it with the following info

- `db_template`: Notion Link* of the *Template Database*
- `db_assignment`: Notion Link*  of the *Target Database*
- `db_test`: Notion database for testing
- `user_ids`: List of Notion user ids to assign it to

*(\* = Not the "Share to Web" link. Use the "Copy Link")*

Sample `config.json`:

    {
        "db_template": "https://www.notion.so/<id>?v=<v>",
        "db_assignment": "https://www.notion.so/<id>?v=<v>",
        "db_test": "https://www.notion.so/<id>?v=<v>",
        "user_ids": [
            "bb88e669-db01-48d1-a4a4-9f2985491878",
            "78a82c51-eb1e-4604-9324-11e58c1581ea",
            "a853544a-8d48-41de-a568-d2cd932e9435",
            "c0eeab57-3a79-41c1-abfc-0a4f55fa3cf5",
            "1d706278-4b4d-45a2-ad13-ba3608cd1ba6",
            "3e0735e4-f1d4-4c98-99d0-797a7e208d05",
            "26e76c17-d6e1-4894-9c84-28eca3ff782e"
        ]
    }

### Setup Credentials

`notion-py` requires credentials pair of the Notion account OR the `token_v2` cookie value.

For Alfred, it's recommended you use the `token_v2` cookie.

- Login to Notion in browser
- Inspect (Ctrl+Shift+I on Chrome)
- In the inspect window. Application > Cookies > https://notion.so > Copy `token_v2` value

Either set this as an environment variable `NOTION_TOKEN=<your token_v2 value>` or paste this in a `.env` file as follows

```bash
NOTION_TOKEN="<your token_v2 value>"
```

### Running Alfred

```bash
$ python main.py
```

Alfred will look for all templates that are in `READY` state and start copying them for each user provided in the `user_ids` list.

## Possible Upgrades

- Load User IDs from a notion database directly (instead of passing it through `config.json`)
- Currently, only fixed set of page properties are copied. Probably generalize this?

## License

MIT

