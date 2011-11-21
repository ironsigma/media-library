#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from medialib.model import TableBase
from medialib.service import ImportJson
import json
import os

try:
    os.unlink('medialib.db')
except OSError: pass

try:
    os.unlink('medialib.db-journal')
except OSError: pass

engine = create_engine('sqlite:///medialib.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

TableBase.metadata.create_all(engine)
session.flush()

json_import = ImportJson(session)
datafile = open('medialib.json', 'r')
objects = json.load(datafile, object_hook=json_import.to_media_object)

session.flush()
session.commit()
