def create_schema(store, file):
    store.execute('''CREATE TABLE media (
            id INTEGER PRIMARY KEY,
            parent_id INTEGER,
            type INTEGER,
            file TEXT,
            cover TEXT,
            title TEXT,
            release INTEGER,
            rated TEXT,
            desc TEXT)''')

    store.execute('''CREATE TABLE media_tag (
            media_id INTEGER,
            tag_id INTEGER,
            PRIMARY KEY (media_id, tag_id))''')

    store.execute('''CREATE TABLE tag (
            id INTEGER PRIMARY KEY,
            parent_id INTEGER,
            name TEXT,
            desc TEXT)''')
