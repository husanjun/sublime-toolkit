import sublime
import sublime_plugin


class HtmlSmartyFormatHandleCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        regions = self.view.find_all(r'{\s/')
        regions.reverse()
        if regions:
            for region in regions:
                self.view.replace(edit, region, '{/')


class HtmlSmartyFormat(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        syntax = sublime.syntax_from_path(view.settings().get('syntax'))
        if syntax and 'text.html' in syntax.scope:
            sublime.set_timeout_async(lambda: view.run_command("html_smarty_format_handle"))

    # def on_post_text_command(self, command_name, args):
    #     if command_name in ('lsp_format_document', 'lsp_format_document_range'):
    #         sublime.set_timeout(lambda: self.view.run_command("html_smarty_format_handle"))
