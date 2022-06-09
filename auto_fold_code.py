import sublime
import sublime_plugin
import os


class AutoFoldCode(sublime_plugin.EventListener):
    def on_load_async(self, view):
        view.run_command("fold_by_level", {"level": 2})
