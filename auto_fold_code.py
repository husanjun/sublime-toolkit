import sublime
import sublime_plugin
import os


class AutoFoldCodeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        _row, _col = self.view.rowcol(self.view.sel()[0].b)
        self.view.run_command("fold_by_level", {"level": 1 if _row > 0 else 2})
        # sublime.active_window().active_view().unfold(sublime.active_window().active_view().folded_regions()[2])


class AutoFoldCode(sublime_plugin.EventListener):
    def on_load_async(self, view):
        # view.run_command("auto_fold_code")
        pass
