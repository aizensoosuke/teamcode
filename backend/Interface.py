from backend import Merger
from backend.FilesHandler import FilesHandler


def getContent(sessionId):
    filesHandler = FilesHandler(sessionId)
    return filesHandler.read("merged")

def postContent(sessionId, userId, fileSubmitted):
    filesHandler = FilesHandler(sessionId)
    filesHandler.write(userId, fileSubmitted)
    Merger.merge(filesHandler)
    return "Successfully merged updated file."
