import factory
import django.contrib.auth.models
from . import models


class User(factory.DjangoModelFactory):
    FACTORY_FOR = django.contrib.auth.models.User

    username = factory.Sequence(lambda n: 'user%d' % n)
    first_name = 'John'
    last_name = 'Doe'
    # admin = False


class Client(factory.DjangoModelFactory):
    FACTORY_FOR = models.Client

    name = factory.Sequence(lambda n: 'client%d' % n)
    address = factory.Sequence(lambda n: '%d rue de la paix' % n)


class InvoiceItem(factory.DjangoModelFactory):
    FACTORY_FOR = models.InvoiceItem

    description = factory.Sequence(lambda n: 'Item #%d' % n)
    quantity = 2
    vat = 20.0
    amount = 100.0


class Invoice(factory.DjangoModelFactory):
    FACTORY_FOR = models.Invoice

    name = factory.Sequence(lambda n: 'Invoice #%d' % n)
    client = factory.SubFactory(Client)
    owner = factory.SubFactory(User)


class EstimateItem(factory.DjangoModelFactory):
    FACTORY_FOR = models.EstimateItem

    description = factory.Sequence(lambda n: 'Item #%d' % n)
    quantity = 2
    vat = 20.0
    amount = 100.0


class Estimate(factory.DjangoModelFactory):
    FACTORY_FOR = models.Estimate

    name = factory.Sequence(lambda n: 'Estimate #%d' % n)
    client = factory.SubFactory(Client)
    owner = factory.SubFactory(User)
