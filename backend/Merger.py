import subprocess
from backend.FilesHandler import FilesHandler

def merge(filesHandler : FilesHandler) -> None:
    ownerPath = filesHandler.getPath("owner")
    collaboratorPath = filesHandler.getPath("collaborator")
    mergedPath = filesHandler.getPath("collaborator")

    command = f'git merge-file "{mergedPath}" "{ownerPath}" "{collaboratorPath}" --ours'

    subprocess.run(command)
