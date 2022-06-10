import sublime
import sublime_plugin
import os


class AutoFoldCode(sublime_plugin.EventListener):
    def on_load_async(self, view):
        _row, _col = view.rowcol(view.sel()[0].b)
        view.run_command("fold_by_level", {"level": 1 if _row > 0 else 2})
