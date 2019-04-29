import sgtk

HookClass = sgtk.get_hook_baseclass()


class SceneOperation(HookClass):
    def execute(self, operation, file_path, context=None, parent_action=None, file_version=None, read_only=None,
                **kwargs):

        if operation == "current_path":
            return self.parent.engine.get_current_file()

        elif operation == "open":
            self.parent.engine.load_file(file_path, lambda: None)

        elif operation == "save":
            if file_path:
                self.parent.engine.save_file(file_path, parent=self.parent.instance_name)
            else:
                current_path = self.parent.engine.get_current_file()
                if current_path:
                    self.parent.engine.save_file(current_path, parent=self.parent.instance_name)

        elif operation == "save_as":
            self.parent.engine.save_file(file_path, parent=self.parent.instance_name)

        elif operation == "reset":
            self.parent.engine.current_file = None
            current_file = self.parent.engine.get_current_file()

            if current_file is not None:
                self.parent.engine.current_file = current_file

            if parent_action == "open_file":
                return True

            self.parent.engine.reset_scene(current_file=current_file)

            return True
