from storm.locals import Int, Unicode, Reference, ReferenceSet

class Tag(object):
    __storm_table__ = 'tag'

    id = Int(primary=True)
    parent_id = Int()
    name = Unicode()
    description = Unicode(name='desc')

    parent = Reference(parent_id, id)
    children = ReferenceSet(id, parent_id)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "id: %s, parent: %s, name: %s, description: %s" % (
                self.id, self.parent_id, self.name, self.description)
