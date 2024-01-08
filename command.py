# -*- coding: utf-8 -*-
import sublime
import sublime_plugin


class LspIntelephenseReindexWorkspaceCommand(sublime_plugin.WindowCommand):
    """ Re-index the workspace. """

    session_name = __package__

    def run(self) -> None:
        window = self.window
        if not window:
            return
        self.window.run_command('lsp_restart_server', {'config_name': "LSP-intelephense"})
        # self._wm = windows.lookup(window)
        # self._stop_server()
        # configs = self._wm.get_config_manager().match_view(self.view)
        # for config in configs:
        # if config.name == self.session_name:
        # config.init_options.set('clearCache', True)
        # self.window.run_command('lsp_restart_server', {'config_name': "LSP-intelephense"})
        # self._start_server()
        # config.init_options.set('clearCache', False)

    # def remove():

    # def _start_server(self) -> None:
    #     self._wm.register_listener_async(windows.listener_for_view(self.view))

    # def _stop_server(self) -> None:
    #     self._wm.end_config_sessions_async(self.session_name)
