from django.db import models
from django.template.defaultfilters import filesizeformat

import os
import subprocess
import datetime


class Upload(models.Model):
    '''A file that got uploaded.'''
    def detect_mime(self, filepath):
        """detect mime using system  program"""
        proc = subprocess.Popen(['file', '--mime-type', '-b', filepath],
            stdout=subprocess.PIPE)
        out = proc.communicate()
        return out[0].strip()

    file = models.FileField(upload_to="media/uploads")
    size = models.PositiveIntegerField(blank=True, default=0)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    name = models.CharField('real file name', max_length=255)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    description = models.TextField('description', blank=True, help_text='attachment description')
    mime_type = models.CharField('MIME type', max_length=128, default='application/octet-stream')

    class Meta:
        ordering = ['-timestamp',]

    def __unicode__(self):
        return u"%s" % (self.file)

    def set_file(self, fl):
        self.name = os.path.basename(fl.name)
        print type(fl)
        #self.size = fl.size
        self.file = fl

    def save(self, *args, **kwargs):
        if not self.id:
            self.set_file(self.file)
        self.mime_type = self.detect_mime(self.file.path)
        super(Upload, self).save(*args, **kwargs)

    @property
    def size(self):
        return filesizeformat(self.file.size)
