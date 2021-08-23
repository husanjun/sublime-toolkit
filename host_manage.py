import sublime
import sublime_plugin
import os


class HostManageCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        path = os.path.join(os.environ['SYSTEMROOT'], "system32\\drivers\\etc\\hosts")
        self.view.window().open_file(path)
