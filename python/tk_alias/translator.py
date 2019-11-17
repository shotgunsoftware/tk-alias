import os
import subprocess


class AliasTranslator(object):
    def __init__(self, engine):
        self.engine = engine
        self.logger = engine.logger
        self.operations = engine.operations

    def translate_file(self, input_path, output_path):
        file_extension = os.path.splitext(output_path)[1][1:]

        if file_extension in ["igs", "iges"]:
            return self.translate_iges(input_path, output_path)

        elif file_extension in ["CATPart"]:
            return self.translate_catpart(input_path, output_path)

        elif file_extension in ["jt"]:
            return self.translate_jt(input_path, output_path)

        elif file_extension in ["stp", "step"]:
            return self.translate_step(input_path, output_path)

        elif file_extension in ["wre"]:
            return self.translate_wref(input_path, output_path)

        else:
            success = False
            message = "Unknown file format"

            return success, message

    @property
    def translator_dir(self):
        alias_bindir = self.engine.alias_bindir
        if os.path.exists(os.path.join(alias_bindir, "translators")):
            return os.path.join(alias_bindir, "translators")

        return alias_bindir

    def translate_iges(self, input_path, output_path):
        translator = os.path.join(self.translator_dir, "AliasToIges.exe")
        return self._translate(translator=translator, input_path=input_path, output_path=output_path)

    def translate_catpart(self, input_path, output_path):
        translator = os.path.join(self.translator_dir, "AlToC5.exe")
        return self._translate(translator=translator, input_path=input_path, output_path=output_path)

    def translate_jt(self, input_path, output_path):
        translator = os.path.join(self.translator_dir, "AlToJt.bat")
        extra_options = [
            "-e1s",
            "-g",
            "-xk",
            "-s 1.0000",
            "-u 128",
            "-m0",
            "-ta",
            "-t 0.100000",
            "-t1t 0.250000",
            "-t2t 1.000000",
            "-tl 1",
        ]

        return self._translate(translator=translator, input_path=input_path, output_path=output_path,
                               extra_options=extra_options)

    def translate_step(self, input_path, output_path):
        translator = os.path.join(self.translator_dir, "AliasToStep.exe")
        return self._translate(translator=translator, input_path=input_path, output_path=output_path)

    def translate_wref(self, input_path, output_path):
        translator = os.path.join(self.translator_dir, "AlToRef.exe")
        return self._translate(translator=translator, input_path=input_path, output_path=output_path)

    @property
    def license_info(self):
        info = self.operations.get_info()
        return '-productKey {product_key} ' \
               '-productVersion {product_version} ' \
               '-productLicenseType {product_license_type} ' \
               '-productLicensePath "{product_license_path}"'.format(
                product_key=info.get("product_key"),
                product_version=info.get("product_version"),
                product_license_type=info.get("product_license_type"),
                product_license_path=info.get("product_license_path"))

    def _translate(self, translator, input_path, output_path, extra_options=[]):
        command = []
        success = True
        message = "The file was translated successfully"

        command.append('"{translator}"')

        input_file = '"{}"'.format(input_path)
        output_file = '"{}"'.format(output_path)

        command.append("-i {input_file}".format(input_file=input_file))
        command.append("-o {output_file}".format(output_file=output_file))

        command.append(self.license_info)

        if extra_options:
            command += extra_options

        command = " ".join(command)
        self.logger.debug("Command: {command}")

        try:
            subprocess.call(command)
        except subprocess.CalledProcessError as e:
            message = e.message
            success = False

        return success, message

