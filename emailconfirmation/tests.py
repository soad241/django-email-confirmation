from django.test import TestCase
from django.contrib.auth.models import User

import models

class EmailAddressTest(TestCase):
    def test_save(self):
        user = User.objects.create_user('user', 'user@localhost')
        email = models.EmailAddress.objects.create(user=user, 
                                                   email='joe@schmoe.com')
        self.failUnlessEqual('schmoe.com', email.domain)
        
