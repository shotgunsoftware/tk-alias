import sgtk

HookClass = sgtk.get_hook_baseclass()


class SceneOperation(HookClass):
    def execute(self, operation, file_path, context=None, parent_action=None, file_version=None, read_only=None,
                **kwargs):

        engine = self.parent.engine
        operations = engine.operations

        engine.logger.debug("tk-multi-workfiles2 scene_operation, "
                            "operation: {}, "
                            "file_path: {}, "
                            "context: {}, "
                            "parent_action: {}, "
                            "file_version: {}, "
                            "read_only: {}".format(operation,
                                                   file_path,
                                                   context,
                                                   parent_action,
                                                   file_version,
                                                   read_only))

        if operation == "current_path":
            return operations.get_current_path()

        elif operation == "open":
            operations.open_file(file_path)

        elif operation == "save":
            operations.save_file()

        elif operation == "save_as":
            operations.save_file_as(file_path)

        elif operation == "reset":
            if parent_action == "new_file":
                operations.create_new_file()
            elif parent_action != "open_file":
                operations.reset_scene()

            return True
