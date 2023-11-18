import sublime
import sublime_plugin
import winreg
import os


def add_context_menu(
        menu_name: str,
        command: str,
        reg_key_path: str,
        reg_root_key_path=winreg.HKEY_CLASSES_ROOT,
        shortcut_key=None
) -> None:
    '''
    添加一个右键菜单的方法
    :param menu_name: 显示的菜单名称
    :param command: 菜单执行的命令
    :param reg_root_key_path: 注册表根键路径
    :param reg_key_path: 要添加到的注册表父键的路径（相对路径）
    :param shortcut_key: 菜单快捷键，如：'S'
    :return:
    '''
    # 打开名称父键
    key = winreg.OpenKey(reg_root_key_path, reg_key_path)
    # 为key创建一个名称为menu_name的sub_key，并设置sub_key的值为menu_name加上快捷键，数据类型为winreg.SZ字符串类型
    winreg.SetValue(key, menu_name, winreg.REG_SZ, menu_name + '(&{0})'.format(shortcut_key) if shortcut_key else '')

    # 打开刚刚创建的名为menu_name的sub_key
    sub_key = winreg.OpenKey(key, menu_name, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(sub_key, 'Icon', 0, winreg.REG_EXPAND_SZ, command+',0')
    # 为sub_key添加名为'command'的子键，并设置其值为command + ' "%v"'，数据类型为winreg.SZ字符串类型
    winreg.SetValue(sub_key, 'command', winreg.REG_SZ, command + ' "%v"')

    # 关闭sub_key和key
    winreg.CloseKey(sub_key)
    winreg.CloseKey(key)


def del_context_menu(menu_name: str, reg_key_path: str, reg_root_key_path=winreg.HKEY_CLASSES_ROOT) -> None:
    '''
    删除一个右键菜单注册表子键
    :param reg_root_key_path:根键
    :param reg_key_path: 父键
    :param menu_name: 菜单子键名称
    :return: None
    '''
    try:
        parent_key = winreg.OpenKey(reg_root_key_path, reg_key_path)
        if parent_key:
            menu_key = winreg.OpenKey(parent_key, menu_name)
            if menu_key:
                answer = sublime.ok_cancel_dialog('Delete {}?'.format(winreg.QueryValue(parent_key, menu_name)))
                if answer is not True:
                    return
                try:
                    # 必须先删除子键的子键，才能删除子键本身
                    winreg.DeleteKey(menu_key, 'command')
                except Exception as e:
                    print(e)
                else:
                    winreg.DeleteKey(parent_key, menu_name)
            # 关闭
            winreg.CloseKey(menu_key)
        winreg.CloseKey(parent_key)
    except Exception as msg:
        print(msg)


class AddWinContextMenuCommand(sublime_plugin.WindowCommand):
    def run(self):
        sublime.set_timeout(
            lambda: self.window.show_quick_panel(['file & folder', 'file', 'folder'], self.on_select),
            10)

    def on_select(self, index: int) -> None:
        self.index = index
        sublime.set_timeout(lambda: self.path_callback(sublime.executable_path()), 10)
        # self.window.show_input_panel('executable path:', '', self.path_callback, None, None)

    def path_callback(self, path: str) -> None:
        self.window.show_input_panel('context menu name:', 'Open with {}'.format(os.path.basename(path).split('.')[0]),
                                     lambda x: self.menu_callback(x, path), None, None)

    def menu_callback(self, menu_name: str, path: str) -> None:
        if self.index == 1:
            self.add_context_file(menu_name, path)
        elif self.index == 2:
            self.add_context_folder(menu_name, path)
        else:
            self.add_context_file(menu_name, path)
            self.add_context_folder(menu_name, path)

    def add_context_file(self, menu_name: str, path: str) -> None:
        add_context_menu(menu_name, path, r'*\\shell')

    def add_context_folder(self, menu_name: str, path: str) -> None:
        add_context_menu(menu_name, path, 'Directory\\shell')


class DelWinContextMenuCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.show_input_panel('context menu name:', 'Please input menu name', self.menu_callback, None, None)

    def menu_callback(self, menu_name: str) -> None:
        del_context_menu(menu_name, r'*\\shell')
        del_context_menu(menu_name, 'Directory\\shell')
