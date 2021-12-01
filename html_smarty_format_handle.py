import sublime
import sublime_plugin


class HtmlSmartyFormatHandleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.find_all('{ /')
        if regions:
            for region in regions:
                self.view.replace(edit, region, '{/')

class HtmlSmartyFormat(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        view.run_command("html_smarty_format_handle")
