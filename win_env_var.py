# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import winreg
import os


def add_env_var(path: str, reg_root_key_path=winreg.HKEY_LOCAL_MACHINE) -> None:
    '''
    添加环境变量
    :param user_env: 要添加的路径
    :param reg_root_key_path: 注册表根键路径
    :return:
    '''

    # 打开环境变量键
    key = winreg.OpenKey(
        reg_root_key_path,
        r'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment', 0, winreg.KEY_ALL_ACCESS)

    # 获取当前环境变量值
    value, type = winreg.QueryValueEx(key, 'Path')

    # 将路径添加到环境变量中
    if path not in value:
        value += ';' + path

    # 更新环境变量值
    winreg.SetValueEx(key, 'Path', 0, type, value)

    # 关闭sub_key和key
    winreg.CloseKey(key)


class AddWinEnvVarCommand(sublime_plugin.WindowCommand):
    def run(self):
        self._options = ['Git', 'Other']
        sublime.set_timeout(
            lambda: self.window.show_quick_panel(self._options, self.on_select),
            10)

    def on_select(self, index: int) -> None:
        path_dict = {
            'Git': os.path.join(os.path.dirname(
                os.path.abspath(self.window.active_view().settings().get('sublime_merge_path'))), 'Git\\cmd\\')
        }
        path = path_dict.get(self._options[index], '')
        if not path:
            self.window.show_input_panel('executable path:', '', self.path_callback, None, None)
        else:
            sublime.set_timeout(lambda: self.path_callback(path), 10)

    def path_callback(self, path: str) -> None:
        sublime.set_timeout(lambda: add_env_var(path), 10)
