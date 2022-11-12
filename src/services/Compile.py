import io
import os
import subprocess

from src.config import CompilerConfig, Config
from src.http_error import NotFoundHttpError, ApiHttpError, ServerHttpError
from src.models.Code import CodeModel


class CompileService:
    @classmethod
    def compile(cls, id_user, id_file):
        code: CodeModel = CodeModel.query.filter(CodeModel.id == id_file).first()
        if not code:
            raise NotFoundHttpError
        if code.id_user != id_user:
            raise ApiHttpError(message="You have not permissions to run this code!", status_code=403)
        if code.ext not in CompilerConfig.AVAILABLE_COMPILES:
            raise ServerHttpError

        try:
            if code.ext == "js":
                return Compiler.javascript(filepath=code.filepath, filename=code.title)
            elif code.ext == "ts":
                return Compiler.typescript(id_code=code.id, filepath=code.filepath, filename=code.title)
            elif code.ext == "py":
                return Compiler.python(filepath=code.filepath, filename=code.title)
            elif code.ext == "php":
                return Compiler.php(filepath=code.filepath, filename=code.title)
        except BaseCompilerError as e:
            print("Compiler error:", e.message)
            raise ServerHttpError

        raise ServerHttpError


class BaseCompilerError(Exception):
    message: str

    def __init__(self, message):
        super().__init__(message)


class OutputCmdProcess:
    def __init__(self, output: bytes, error: bytes):
        self.output_buffer = io.BytesIO(b'')
        self.error_buffer = io.BytesIO(b'')
        self.output = ""
        self.error = ""

        if output != b'':
            self.output_buffer = io.BytesIO(output)
            self.output = io.BytesIO(output).read(CompilerConfig.MAX_OUTPUT_LENGTH).decode('utf-8')
        if error != b'':
            self.error_buffer = io.BytesIO(error)
            self.error = error.decode('utf-8')


class CmdProcess:
    @classmethod
    def run(cls, command: list) -> OutputCmdProcess:
        process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            output, error = process.communicate(timeout=CompilerConfig.TIME_EXPIRE)
        except subprocess.TimeoutExpired as e:
            process.kill()
            output, error = process.communicate()

        return OutputCmdProcess(output=output,error=error)


class OutputCompiler:
    value: str
    is_error: bool

    def __init__(self, value, is_error, version_compiler):
        self.value = value
        self.is_error = is_error
        self.version_compiler = version_compiler


class Compiler:
    @classmethod
    def javascript(cls, filepath, filename) -> OutputCompiler:
        relative_filepath = os.path.relpath(filepath)
        abs_filepath = "/private" + os.path.abspath(filepath)
        process = CmdProcess.run(command=[CompilerConfig.NODE_CMD, "--no-warnings", "--stack-trace-limit=1", filepath])

        if process.error:
            return OutputCompiler(value=process.error.replace(abs_filepath, filename).replace(relative_filepath, filename),
                                  is_error=True,
                                  version_compiler=CompilerConfig.NODE_VERSION)
        else:
            return OutputCompiler(value=process.output,
                                  is_error=False,
                                  version_compiler=CompilerConfig.NODE_VERSION)

    @classmethod
    def typescript(cls, id_code, filepath, filename) -> OutputCompiler:
        relative_filepath = os.path.relpath(filepath)
        abs_filepath = os.path.abspath(filepath)
        output_js_filepath = f"{Config.STORAGE_PATH}/{id_code}.js"

        process = CmdProcess.run(command=[CompilerConfig.TYPESCRIPT_CMD, "--module", "none", "--pretty", "false", "--strict", "--noEmitOnError", "--outFile", output_js_filepath, filepath])

        # If output approach it is mean typescript generate error,
        # Check each line for filepath and replace to filename

        if process.output != "" and not os.path.exists(output_js_filepath):
            return OutputCompiler(value=process.output.replace(relative_filepath, filename).replace(abs_filepath, filename),
                                  is_error=True,
                                  version_compiler=CompilerConfig.TYPESCRIPT_VERSION)
        else:
            output_compile_js = cls.javascript(output_js_filepath, filename=filename)
            try:
                os.unlink(output_js_filepath)
            except OSError:
                raise BaseCompilerError("TS: Error delete output js file")

            return OutputCompiler(value=output_compile_js.value,
                                  is_error=output_compile_js.is_error,
                                  version_compiler=CompilerConfig.TYPESCRIPT_VERSION)

    @classmethod
    def python(cls, filepath, filename) -> OutputCompiler:
        relative_filepath = os.path.relpath(filepath)
        abs_filepath = os.path.abspath(filepath)

        process = CmdProcess.run(command=[CompilerConfig.PYTHON_CMD, filepath])

        if process.error:
            return OutputCompiler(value=process.error.replace(relative_filepath, filename).replace(abs_filepath, filename),
                                  is_error=True,
                                  version_compiler=CompilerConfig.PYTHON_VERSION)
        else:
            return OutputCompiler(value=process.output,
                                  is_error=False,
                                  version_compiler=CompilerConfig.PYTHON_VERSION)

    @classmethod
    def php(cls, filepath, filename) -> OutputCompiler:
        process = CmdProcess.run(command=[CompilerConfig.PHP_CMD, filepath])

        relative_filepath = os.path.relpath(filepath)
        abs_filepath = os.path.abspath(filepath)

        if process.error:
            return OutputCompiler(value=process.error.replace(relative_filepath, filename).replace(abs_filepath, filename),
                                  is_error=True,
                                  version_compiler=CompilerConfig.PHP_VERSION)
        else:
            return OutputCompiler(value=process.output,
                                  is_error=False,
                                  version_compiler=CompilerConfig.PHP_VERSION)
