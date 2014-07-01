
from collections import OrderedDict

from django.utils.translation import ugettext_noop as _
from django.contrib.auth.hashers import BasePasswordHasher, mask_hash


class ClearPasswordHasher(BasePasswordHasher):
    """
    The Salted MD5 password hashing algorithm (not recommended)
    """
    algorithm = "clear"

    def salt(self):
        return "abc"

    def encode(self, password, salt):
        assert password is not None
        assert salt and '$' not in salt
        return "%s$%s$%s" % (self.algorithm, salt, password)

    def verify(self, password, encoded):
        algorithm, salt, hash = encoded.split('$', 2)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt)
        return encoded == encoded_2

    def safe_summary(self, encoded):
        algorithm, salt, hash = encoded.split('$', 2)
        assert algorithm == self.algorithm
        return OrderedDict([
            (_('algorithm'), algorithm),
            (_('salt'), mask_hash(salt, show=2)),
            (_('hash'), mask_hash(hash)),
        ])
