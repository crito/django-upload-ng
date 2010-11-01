from django.db import models
from django.template.defaultfilters import filesizeformat
import subprocess
import datetime

class Upload(models.Model):
    '''A file that got uploaded.'''
    def detect_mime(filepath):
        """detect mime using system  program"""
        proc = subprocess.Popen(['file', '--mime-type', '-b', filepath],
            stdout=subprocess.PIPE)
        out = proc.communicate()
        return out[0].strip()

    file = models.FileField(upload_to="media/uploads")
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    name = models.CharField('real file name', max_length=255)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    description = models.TextField('description', blank=True, help_text='attachment description')
    mime_type = models.CharField('MIME type', max_length=128, default='application/octet-stream')

    class Meta:
        ordering = ['-timestamp',]

    def __unicode__(self):
        return u"%s" % (self.file)

    def save(self, *args, **kvargs):
        if not self.id:
            self.set_file(self.file)
        self.mime_type = detect_mime(self.file.path)
        super(Attachment, self).save(*args, **kvargs)

    @property
    def size(self):
        return filesizeformat(self.file.size)
