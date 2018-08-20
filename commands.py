import json


class Command(object):
    """
    Represents a request sent from the Engine to the C++ plugin.
    """

    def __init__(self, CommandName):
        self.command = CommandName

    def __to_json(self):
        """
        Encode the object to JSON.
        """
        return json.dumps(self, default=lambda o: o.__dict__)

    def to_string(self):
        return self.__to_json()


class LoadImageCommand(Command):

    def __init__(self, filePath):
        super(LoadImageCommand, self).__init__("LoadImage")
        self.path = filePath


class MenuRebuildCommand(Command):

    """
    Request the creation of the menu.
    """
    def __init__(self, buttonList = []):
        super(MenuRebuildCommand, self).__init__("MenuRebuild")
        self.buttons = buttonList


class FileOpenCommand(Command):
    def __init__(self, filePath):
        super(FileOpenCommand, self).__init__("FileOpen")
        self.path = filePath


class FileSaveCommand(Command):
    def __init__(self, filePath):
        super(FileSaveCommand, self).__init__("FileSave")
        self.path = filePath.replace("/", "\\") or ""  # This prevent a None value for being sent.


class StageOpenCommand(Command):
    def __init__(self, filePath):
        super(StageOpenCommand, self).__init__("StageOpen")
        self.path = filePath


class FileLoadCommand(Command):
    def __init__(self, filePath, importReference, namespace=None, create_stage=False):
        super(FileLoadCommand, self).__init__("FileLoad")
        self.path = filePath
        self.importReference = importReference
        if namespace:
            self.namespace = namespace
        self.create_stage = str(create_stage).lower()


class CurrentFileCommand(Command):
    def __init__(self):
        super(CurrentFileCommand, self).__init__("CurrentFile")


class PidRequest(Command):
    def __init__(self):
        super(PidRequest, self).__init__("PidRequest")


class SceneBreakdownCommand(Command):
    def __init__(self):
        super(SceneBreakdownCommand, self).__init__("SceneBreak")


class UpdateSceneCommand(Command):
    def __init__(self, references):
        super(UpdateSceneCommand, self).__init__("UpdateReferences")
        self.refs = references


class ContextChangeCommand(Command):
    def __init__(self, path):
        super(ContextChangeCommand, self).__init__("ContextChange")
        self.path = path


class ResetCommand(Command):
    """
    Represents the command to reset a scene.
    """

    def __init__(self):
        super(ResetCommand, self).__init__("Reset")


class ExportAnnotationsCommand(Command):
    def __init__(self):
        super(ExportAnnotationsCommand, self).__init__("ExportAnnotations")


class ExportVariantsCommand(Command):
    def __init__(self, file_name_prefix, temp_dir):
        super(ExportVariantsCommand, self).__init__("ExportVariants")
        self.file_name_prefix = file_name_prefix
        self.temp_dir = temp_dir
