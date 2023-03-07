from django.db import models


class Client(models.Model):
    """ # ? top level client model """
    name = models.CharField(max_length=50, blank=False, null=False)
    surname = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(
        max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return str(self.id)


class Request(models.Model):
    """ #? second level requests associated with client """
    name = models.CharField(max_length=50, blank=False, null=False)
    submitted = models.BooleanField(default=False, blank=False)
    date_submitted = models.DateTimeField(auto_created=True, blank=False)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='requests')

    def __str__(self):
        return str(self.id)


class Document(models.Model):
    """ #? second level documents associate with client and request """
    name = models.CharField(max_length=50, blank=False, null=False)
    date = models.DateTimeField(auto_created=True, blank=False)
    document = models.FileField(
        upload_to='./managers/files', blank=False, null=False)
    request = models.ForeignKey(
        Request, on_delete=models.CASCADE, default=1, related_name='documents')
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return str(self.id)
