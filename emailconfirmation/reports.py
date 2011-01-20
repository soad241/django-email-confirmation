from django.db.models import Sum, Avg, Count
from gattlib.aggregates import SumIf
import defreports
import models

class EmailAddressReport(defreports.Report):
    name = 'Email Address Report'
    slug = 'email-address-report'
    model = models.EmailAddress
    
    filter_by = defreports.filters(
        defreports.DateFilter('date'),
        defreports.Filter('date', name='Days', multiple=True), 
        defreports.Filter('domain'),
        defreports.BooleanFilter('verified'),
    )
    group_by = defreports.groupbys(
        'domain', 
        'date', 
        'verified',
    )
    list_aggregates = defreports.columns(
        defreports.Column(Count('id'), name='Emails'),
        defreports.Column(Count('user', distinct=True), name='Users'),
        defreports.PercentageCalculatedColumn('Verified', 
                              'Emails', name='Verification %'),
        defreports.Column(SumIf('verified'), name='Verified'),
    )
        
defreports.site.register(EmailAddressReport)
