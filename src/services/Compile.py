import io
import os
import subprocess

from src.config import CompilerConfig
from src.http_error import NotFoundHttpError, ApiHttpError, ServerHttpError
from src.models.Code import CodeModel
from src.services.FileCode import FileCodeService, FileCodeError


class CompileService:
    @classmethod
    def compile(cls, id_user, id_file):
        code = CodeModel.query.filter(CodeModel.id == id_file).first()
        if not code:
            raise NotFoundHttpError
        if code.id_user != id_user:
            raise ApiHttpError(message="You have not permissions to run this code!", status_code=403)
        if code.ext not in CompilerConfig.AVAILABLE_COMPILES:
            raise ServerHttpError

        if code.ext == "js":
            return Compiler.javascript(code.filepath)
        raise ServerHttpError


class OutputCompiler:
    value: str
    is_error: bool

    def __init__(self, value, is_error):
        self.value = value
        self.is_error = is_error


class Compiler:
    @classmethod
    def javascript(cls, filepath):
        print(cls.check_imports_in_js_code(filepath))
        filepath = os.path.join(filepath)
        process = subprocess.Popen(["node", "--no-warnings", "--stack-trace-limit=1", filepath], stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
        try:
            output, error = process.communicate(timeout=CompilerConfig.TIME_EXPIRE)
        except subprocess.TimeoutExpired as e:
            process.kill()
            output, error = process.communicate()

        if error != b'':
            reader_error = io.BytesIO(error)
            char_response = f"node@16.4\n\n"
            reader_lines = reader_error.readlines()
            for i in range(1, len(reader_lines) - 1):
                char_response += reader_lines[i].decode("utf8")
            return OutputCompiler(value=char_response, is_error=True)
        if output:
            reader_output = io.BytesIO(output)
            response = reader_output.read(CompilerConfig.MAX_OUTPUT_LENGTH).decode('utf8')
            if response[-1] != "\n":
                response = response + "...\n"
            return OutputCompiler(value=response, is_error=False)

        return OutputCompiler(value="", is_error=False)

    @classmethod
    def check_imports_in_js_code(cls, filepath):
        try:
            value_rows = FileCodeService.get_value(filepath).split('\n')
            for row in value_rows:
                if row.find('require') != -1:
                    row = row.split(" ")
                    for i in range(0, len(row) - 1):
                        if row[i].find('function') != -1 and row[i + 1].find('require') != -1:
                            return True
            return False
        except FileCodeError:
            raise ServerHttpError
