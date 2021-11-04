from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage()

storage = FileSystemStorage()

class FilesHandler:
    """
    Handle file creation and editting.

    Every time the owner or the collaborator publishes a new version of his file,
    the file will be updated on the server's disk.
    The owner and collaborator files will then be merged into the merged file.

    Attributes
    ----------
    """

    sessionId : str = ""

    def __init__(self, sessionId, content : dict = {}):
        """Initialize this class

        Create the necessary files :
        - Owner file
        - Collaborator file
        - Merged file

        And populates them with some content if provided.

        Parameters
        ----------
        sessionId : str
            This will be used to create a folder specific to that session.

        content : dict[str, str]
            Initial content to populate the files with.
            This associates content to each userId (such as `owner`, `collaborator`)

        """

        self.sessionId = sessionId

        if not storage.exists(self._getPath("merged")):
            self.files["owner"] = self._createFile("owner")
            self.files["collaborator"] = self._createFile("collaborator")
            self.files["merged"] = self._createFile("merged")

            self.write("owner", "")
            self.write("collaborator", "")

        if "owner" in content:
            self.write("owner", content["owner"])
        if "collaborator" in content:
            self.write("collaborator", content["collaborator"])


    def getPath(self, userId : str) -> str:
        return storage.path(self._getPath(userId))


    def _getPath(self, userId : str) -> str:
        """Creates and return the partial filepath for the specified userId

        This will in the form "foldername/filename".
        This is supposed to be fed to django's storage API which will figure out
        where the files are.
        This uses the sessionId attribute to know in which folder the files are stored.

        Parameters
        ----------
        userId : str
            The user's identifier used in the corresponding file's name.

        Returns
        -------
        str
            The path to the file corresponding to userId and sessionId.
            This is a partial path, formatted as "foldername/filename"
            This file might not exist.

        Raises
        ------
        AssertionError
            If called before self.sessionId is initialized.
        """

        assert self.sessionId != ""

        return storage.generate_filename(self.sessionId + "/" + userId)


    def _createFile(self, userId : str) -> str:
        """Create file using custom identifiers.

        Create a file using sessionId as a folder and userId as a file identifier.
        This is used to create the three files needed for synchronization

        NOTE: sessionId needs to be initialized before calling this function.

        Parameters
        ----------
        userId : str, required
            The user's identifier used in the corresponding file's name.

        Raises
        ------
        AssertionError
            If sessionId has not been initialized before this is called.

        Returns
        -------
        str
            The filename of the created file.
        """

        assert self.sessionId != ""

        # TODO: we do not check if the files exist. We simply override.

        return storage.save(self._getPath(userId), ContentFile(b''))


    def write(self, userId : str, content : str) -> int:
        """Overrides the user's file with provided content.

        The file's name will be the one returned by `self._getPath(userId)`

        Parameters
        ----------
        userId : str
            The user identifier for this file
        content : str
            The content to write the file with

        Returns
        -------
        The status code returned by write()
        """
        return storage.open(self._getPath(userId), mode="w").write(content)

    def read(self, userId : str) -> str:
        """Reads the user's file and returns content as a string.

        Parameters
        ----------
        userId : str
            The user identifier for this file

        Returns
        -------
        str
            The file's content
        """
        return storage.open(self._getPath(userId), mode="r").read()
