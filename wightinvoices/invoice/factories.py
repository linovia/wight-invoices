import factory
from . import models


class Client(factory.DjangoModelFactory):
    FACTORY_FOR = models.Client

    name = factory.Sequence(lambda n: 'client%d' % n)
    address = factory.Sequence(lambda n: '%d rue de la paix' % n)
