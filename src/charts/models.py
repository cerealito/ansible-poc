from django.db import models


class Host(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class FSUsageSample(models.Model):
    host = models.ForeignKey(Host)
    datetime = models.DateTimeField('Date and time')
    percent = models.FloatField()

    def __unicode__(self):
        return self.host.name + '  ' + unicode(str(self.datetime) + '  ' + str(self.percent))


class MemUsageSample(models.Model):
    host = models.ForeignKey(Host)
    datetime = models.DateTimeField('Date and time')
    num_mb = models.IntegerField('Megabytes of physical memory available')

    def __unicode__(self):
        return self.host.name + '  ' + unicode(str(self.datetime) + '  ' + str(self.num_mb))
