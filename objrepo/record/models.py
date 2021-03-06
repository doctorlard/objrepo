from django.db import models
from jsonfield.fields import JSONField

class Record(models.Model):
    metadata = JSONField(blank=True)
    title = models.TextField()

    def all_metadata(self):
        result = {}

        for l in self.out_links.filter(inherit=True):
            if l.prefix is None:
                result.update(l.link_to.all_metadata())
            else:
                for k,v in l.link_to.all_metadata().iteritems():
                    result[l.prefix + ':' + k] = v

        result.update(self.metadata)
        return result

class Link(models.Model):
    link_from = models.ForeignKey(Record, related_name='out_links')
    link_to = models.ForeignKey(Record, related_name='in_links')
    label = models.TextField()
    inherit = models.BooleanField()
    prefix = models.CharField(blank=True, null=True, max_length=128)
