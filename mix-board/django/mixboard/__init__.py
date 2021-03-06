# had to put this in the top-level mixboard package or it wouldn't be loaded,
# for some reason

from mixboard import settings
from pipeline.compilers import SubProcessCompiler

class CssToJsCompiler(SubProcessCompiler):
    output_extension = 'css_js'

    def match_file(self, path):
        return path.endswith('.css')

    def compile_file(self, content, path):
        command = settings.PIPELINE_CSS_TO_JS_BINARY + " " + path
        return self.execute_command(command, content)
