import sgtk

HookClass = sgtk.get_hook_baseclass()


class SceneOperation(HookClass):
    def execute(self, operation, file_path, context=None, parent_action=None, file_version=None, read_only=None,
                **kwargs):

        engine = self.parent.engine
        operations = engine.operations
        engine.running_operation = True
        engine.current_operation = operation
        engine.parent_action = parent_action

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
            engine.running_operation = False
            return operations.get_current_path()

        elif operation == "open":
            operations.open_file(file_path)
            engine.running_operation = False

        elif operation == "save":
            operations.save_file(operations.get_current_path())
            engine.running_operation = False

        elif operation == "save_as":
            operations.save_file(file_path)
            engine.running_operation = False

        elif operation == "reset":
            if parent_action == "new_file":
                if operations.is_pristine():
                    operations.reset()
                elif operations.want_to_delete_current_objects():
                    operations.reset()
                else:
                    operations.create_stage()
            elif parent_action != "open_file":
                operations.reset()

            engine.running_operation = False

            return True
        else:
            engine.running_operation = False
