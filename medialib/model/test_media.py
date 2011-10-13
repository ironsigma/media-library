import pytest
from ..model import Media, Rating, Subrating, Tag

def pytest_funcarg__disney_tag(request):
    return Tag(id=200, name='Disney', desc='Disney studios')

def pytest_funcarg__d_subrating(request):
    return Subrating(name='D', desc='D something')

def pytest_funcarg__r_rating(request):
    return Rating(name='R', desc='R Rating')

def pytest_funcarg__empty_media(request):
    return Media()

def pytest_funcarg__t3_movie(request):
    return Media(id=84023, title='T3', type='Movie', file='t3.avi', cover='t3.jpg',
            rating=Rating(name='R', desc='R Rating'), release=2003, desc='Terminator 3')

class TestMedia:

    def test_init(self, empty_media, t3_movie, disney_tag, r_rating, d_subrating):
        media = Media(id=3000, title='Vanilla Sky', type='Movie', file='vsky.avi',
                cover='vsky.jpg', release=1995, desc='Trippy', tags=[disney_tag],
                rating=r_rating, subratings=[d_subrating],
                parent=empty_media, children=[t3_movie])

        assert media.id == 3000
        assert media.title == 'Vanilla Sky'
        assert media.type == 'Movie'
        assert media.file == 'vsky.avi'
        assert media.cover == 'vsky.jpg'
        assert media.release == 1995
        assert media.desc == 'Trippy'
        assert media.rating is r_rating
        assert media.subratings[0] is d_subrating
        assert media.parent is empty_media
        assert media.children[0] is t3_movie
        assert media.tags[0] is disney_tag

    def test_types(self, empty_media):
        empty_media.type = 'Folder'
        assert empty_media.type == 'Folder'

        empty_media.type = 'Movie'
        assert empty_media.type == 'Movie'

        empty_media.type = 'Show'
        assert empty_media.type == 'Show'

        with pytest.raises(ValueError):
            empty_media.type = 'Foo'

