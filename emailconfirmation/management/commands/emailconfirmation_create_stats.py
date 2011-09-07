import logging
import lockfile
import datetime
import itertools
import random

from django.core.management import base
from optparse import make_option
from django.conf import settings
from django.db import transaction
from django.db.models import Min, Max
from emailconfirmation import models
logger = logging.getLogger('djangoproject.emailconfirmation.commands.emailconfirmation_create_stats')

class Command(base.NoArgsCommand):
    option_list = base.NoArgsCommand.option_list + (
        make_option('-s', action='store_true', dest='silentmode',
            default=False, help='Run in silent mode'),
        make_option('--debug', action='store_true',
            dest='debugmode', default=False,
            help='Debug mode (overrides silent mode)'),
    )

    def handle_noargs(self, **options):
        if not options['silentmode']:
            logging.getLogger('djangoproject').setLevel(logging.INFO)
        if options['debugmode']:
            logging.getLogger('djangoproject').setLevel(logging.DEBUG)
        
        lock = lockfile.FileLock('/tmp/emailconfirmation_create_stats')
        lock.acquire(10)
        with lock:
            date = datetime.date.today() - datetime.timedelta(days=1)
            timestamp = datetime.datetime.now() - datetime.timedelta(days=1)
            total = models.EmailAddress.objects.filter(date=date).count()
            verified = models.EmailAddress.objects.filter(date=date, 
                                                          verified=True).count()
            if total:
                pct = float(verified)/float(total)*100            
            else:
                pct = 0.0
            models.DaliyMailVerificationStat.objects.create(
                date=date,
                created_at=timestamp,
                verification_pct=pct)
            logger.info("Got %s verified emails" % pct)
