import sgtk

HookClass = sgtk.get_hook_baseclass()


class SceneOperation(HookClass):
    def execute(self, operation, file_path, **kwargs):
        """
        Main hook entry point

        :operation: String
                    Scene operation to perform

        :file_path: String
                    File path to use if the operation
                    requires it (e.g. open)

        :returns:   Depends on operation:
                    'current_path' - Return the current scene
                                     file path as a String
                    all others     - None
        """

        engine = self.parent.engine
        operations = engine.operations
        engine.running_operation = True
        engine.current_operation = operation

        engine.logger.debug(
            "tk-multi-snapshot scene_operation, "
            "operation: {}, "
            "file_path: {}, "
            "kwargs: {}".format(operation, file_path, kwargs)
        )

        if operation == "current_path":
            engine.running_operation = False
            return operations.get_current_path()

        elif operation == "open":
            operations.open_file(file_path)
            engine.running_operation = False

        elif operation == "save":
            operations.save_file(operations.get_current_path())
            engine.running_operation = False
