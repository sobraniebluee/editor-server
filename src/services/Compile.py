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

        filepath = os.path.join(code.filepath)

        try:
            if code.ext == "js":
                return Compiler.javascript(code.filepath)
            elif code.ext == "ts":
                return Compiler.typescript(id_code=code.id, filepath=code.filepath, filename=code.title)
            elif code.ext == "py":
                return Compiler.python(filepath=code.filepath, filename=code.title)

        except BaseCompilerError as e:
            print("Compiler error:", e.message)
            raise ServerHttpError

        raise ServerHttpError


class OutputCompiler:
    value: str
    is_error: bool

    def __init__(self, value, is_error, version_compiler):
        self.value = value
        self.is_error = is_error
        self.version_compiler = version_compiler


class BaseCompilerError(Exception):
    message: str

    def __init__(self, message):
        super().__init__(message)


class CmdProcess:
    @classmethod
    def run(cls, command: list, io_reader=False) -> tuple[None | bytes | io.BytesIO, None | bytes | io.BytesIO]:
        process = subprocess.Popen(command,stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            output, error = process.communicate(timeout=CompilerConfig.TIME_EXPIRE)
        except subprocess.TimeoutExpired as e:
            process.kill()
            output, error = process.communicate()

        if output == b'':
            output = None

        if error == b'':
            error = None

        if io_reader:
            if output:
                output = io.BytesIO(output)
            if error:
                error = io.BytesIO(error)

        return output, error


class Compiler:
    @classmethod
    def javascript(cls, filepath) -> OutputCompiler:
        output, error = CmdProcess.run(io_reader=True, command=[CompilerConfig.NODE_CMD, "--no-warnings", "--stack-trace-limit=1", filepath])

        if error:
            output_utf8 = ""
            reader_lines = error.readlines()
            for i in range(1, len(reader_lines) - 1):
                output_utf8 += reader_lines[i].decode("utf8")
            return OutputCompiler(value=output_utf8,
                                  is_error=True,
                                  version_compiler=CompilerConfig.NODE_VERSION)
        if output:
            output_utf8 = output.read(CompilerConfig.MAX_OUTPUT_LENGTH).decode('utf8')
            if output_utf8[-1] != "\n":
                output_utf8 = output_utf8 + "...\n"
            return OutputCompiler(value=output_utf8,
                                  is_error=False,
                                  version_compiler=CompilerConfig.NODE_VERSION)

        return OutputCompiler(value="",
                              is_error=False,
                              version_compiler=CompilerConfig.NODE_VERSION)

    @classmethod
    def typescript(cls, id_code, filepath, filename) -> OutputCompiler:
        relative_filepath = os.path.relpath(filepath)
        abs_filepath = os.path.abspath(filepath)
        output_js_filepath = f"{Config.STORAGE_PATH}/{id_code}.js"

        output, error = CmdProcess.run(io_reader=True, command=[CompilerConfig.TYPESCRIPT_CMD, "--module", "none", "--pretty", "false", "--strict", "--noEmitOnError", "--outFile", output_js_filepath, filepath])
        # If output approach it is mean typescript generate error,
        # Check each line for filepath and replace to filename
        if output is not None and not os.path.exists(output_js_filepath):
            lines = output.readlines()
            output_utf8 = ""
            for line in lines:
                output_utf8 += line.decode("utf-8").replace(relative_filepath, filename).replace(abs_filepath, filename)

            return OutputCompiler(value=output_utf8,
                                  is_error=True,
                                  version_compiler=CompilerConfig.TYPESCRIPT_VERSION)
        else:
            output_compile_js = cls.javascript(output_js_filepath)
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

        output, error = CmdProcess.run(io_reader=True, command=[CompilerConfig.PYTHON_CMD, filepath])

        if error:
            lines = error.readlines()
            output_utf8 = ""
            for line in lines:
                output_utf8 += line.decode("utf-8").replace(relative_filepath, filename).replace(abs_filepath, filename)

            return OutputCompiler(value=output_utf8,
                                  is_error=True,
                                  version_compiler=CompilerConfig.PYTHON_VERSION)

        if output:
            output_utf8 = output.read(CompilerConfig.MAX_OUTPUT_LENGTH).decode('utf-8')
            if output_utf8[-1] != "\n":
                output_utf8 = output_utf8 + "...\n"
            return OutputCompiler(value=output_utf8,
                                  is_error=False,
                                  version_compiler=CompilerConfig.PYTHON_VERSION)

