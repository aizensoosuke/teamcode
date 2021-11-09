import uuid
import subprocess

from django.db import models
from django.core.files.base import ContentFile

# Create your models here.
class Session(models.Model):
    """Handle session, file creation and editting.

    Every time a user publishes a new version of his file,
    the file will be updated on the server's disk.
    The files will then be merged into the merged file.
    """

    sessionId = models.CharField(max_length=255, unique=True)
    hostId = models.CharField(max_length=255)
    tmpFile = models.FileField(max_length=255)
    mergedFile = models.FileField(max_length=255)

    def get(self):
        return self.mergedFile.read()

    def merge(self):
        users = User.objects.all().filter(session__sessionId = self.sessionId)
        for user in users:
            subprocess.run(["git", "merge-file", self.tmpFile.path, self.mergedFile.path, user.userFile.path, "--ours"])
        return "Successfully merged all files into one"

    @classmethod
    def genPath(cls, sessionId, filename):
        return f'sessionFiles/{sessionId}/sessfiles/{filename}'

    @classmethod
    def create(cls, hostId):
        """Create a new session hosted by User with id hostId.
        The hostId is required.
        """

        newId = uuid.uuid4()

        newSession = cls(sessionId=newId, hostId=hostId, mergedFile=cls.genPath(newId, "merged"), tmpFile=cls.genPath(newId, "tmp"))
        newSession.mergedFile.save(newSession.mergedFile.name, ContentFile(""))
        newSession.tmpFile.save(newSession.tmpFile.name, ContentFile(""))

        return newSession

    def __str__(self):
        return self.sessionId

class User(models.Model):
    """Represent a user that can connect to a Session."""

    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    userId = models.CharField(max_length=255, unique=True)
    userFile = models.FileField(max_length=255)


    def get(self) -> str:
        """Get the merged file from the user's session.

        Return the file's content as an str
        """
        return self.session.getMerged()

    def read(self) -> str:
        """Read the user's file.

        Return the file's content as an str"""

        content = self.userFile.open(mode="r").read()
        self.userFile.close()

        return content

    def write(self, content) -> str:
        """Override the user's file with provided `content`.

        Return the status code returned by write()
        """

        self.userFile.open(mode="w").write(content)
        self.userFile.close()
        self.save()

        return self.session.merge()

    @classmethod
    def genPath(cls, sessionId, userId):
        return f'sessionFiles/{sessionId}/{userId}'

    @classmethod
    def join(cls, sessionId : str):
       """Join an existing session with id `sessionId`"""

       newId = uuid.uuid4()
       session = Session.objects.filter(sessionId = sessionId)

       newUser = cls(userId=newId, session=session, userFile=cls.genPath(session.sessionId, newId))
       newUser.userFile.save(newUser.userFile.name, ContentFile(""))
       newUser.save()

       return newUser

    @classmethod
    def create(cls):
        """Create a new session.
        This user will be the host of the new session."""

        newId = uuid.uuid4()
        session = Session.create(newId)

        newUser = cls(userId=newId, session=session, userFile=cls.genPath(session.sessionId, newId))
        newUser.userFile.save(newUser.userFile.name, ContentFile(""))
        newUser.save()

        return newUser

    def __str__(self):
        return self.userId
