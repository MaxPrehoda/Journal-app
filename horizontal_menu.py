#!/usr/bin/env python
import urwid
top=None

class MenuButton(urwid.Button):
    def __init__(self, caption, callback):
        super(MenuButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'  \N{BULLET} ', caption], 2), None, 'selected')

class EditField(urwid.Edit):
    def __init__(self, caption, callback):
        super(EditField, self).__init__("")
        urwid.connect_signal(self, 'postchange', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'  \N{BULLET} ', caption], 2), None, 'selected')

class SubMenu(urwid.WidgetWrap):
    def __init__(self, caption, choices):
        super(SubMenu, self).__init__(MenuButton(
            [caption, u"\N{HORIZONTAL ELLIPSIS}"], self.open_menu))
        line = urwid.Divider(u'\N{LOWER ONE QUARTER BLOCK}')
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.AttrMap(urwid.Text([u"\n  ", caption]), 'heading'),
            urwid.AttrMap(line, 'line'),
            urwid.Divider()] + choices + [urwid.Divider()]))
        self.menu = urwid.AttrMap(listbox, 'options')

    def open_menu(self, button):
        top.open_box(self.menu)


class EditMenu(urwid.WidgetWrap):
    def __init__(self, caption, callback):
        super(EditMenu, self).__init__(EditField(
            [caption, u"\N{HORIZONTAL ELLIPSIS}"], self.text_changed))
        self.callback = callback

    def text_changed(self,edit_widget,text2):
        pass
        #quit()
        #if edit_widget.text == "\n":
        #    self.callback(edit_widget,text2)

    def keypress(self,size,key):
        if key == 'enter':
            choices = self.callback(self._w.text)
            line = urwid.Divider(u'\N{LOWER ONE QUARTER BLOCK}')
            listbox = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.AttrMap(urwid.Text([u"\n  ", "Search Results"]), 'heading'),
            urwid.AttrMap(line, 'line'),
            urwid.Divider()] + choices + [urwid.Divider()]))
            top.open_box(urwid.AttrMap(listbox, 'options'))
        elif key in ('up','down'):
            return key
        else:
            self._wrapped_widget.keypress(size,key)


class Choice(urwid.WidgetWrap):
    def __init__(self, caption,handler = None,info = None):
        super(Choice, self).__init__(
            MenuButton(caption, self.item_chosen))
        self.handler = handler
        self.caption = caption
        self.info = info

    def item_chosen(self, button):
        if self.handler == None:
            response = urwid.Text([u'  You chose ', self.caption, u'\n'])
            done = MenuButton(u'Ok', exit_program)
            response_box = urwid.Filler(urwid.Pile([response, done]))
            top.open_box(urwid.AttrMap(response_box, 'options'))
        else:
            self.handler(self.caption,self.info)

def exit_program(key):
    raise urwid.ExitMainLoop()

focus_map = {
    'heading': 'focus heading',
    'options': 'focus options',
    'line': 'focus line'}


class HorizontalMenu(urwid.Columns):
    palette = [
        (None,  'light gray', 'black'),
        ('heading', 'black', 'light gray'),
        ('line', 'black', 'light gray'),
        ('options', 'dark gray', 'black'),
        ('focus heading', 'white', 'dark red'),
        ('focus line', 'black', 'dark red'),
        ('focus options', 'black', 'light gray'),
        ('selected', 'white', 'dark blue')]
    def __init__(self):
        super(HorizontalMenu, self).__init__([], dividechars=1)

    def open_box(self, box):
        if self.contents:
            del self.contents[self.focus_position + 1:]
        self.contents.append((urwid.AttrMap(box, 'options', focus_map),
            self.options('given', 24)))
        self.focus_position = len(self.contents) - 1

def horizontal_menu(menus): 
    global top
    top = HorizontalMenu()
    top.open_box(menus.menu)
    return urwid.Filler(top, 'middle', 10)

def main(): #test the menu system with this
    menu_top = SubMenu(u'Main Menu', [
    SubMenu(u'Applications', [
        SubMenu(u'Accessories', [
            Choice(u'Text Editor'),
            Choice(u'Terminal'),
        ]),
    ]),
    SubMenu(u'System', [
        SubMenu(u'Preferences', [
            Choice(u'Appearance'),
        ]),
        Choice(u'Lock Screen'),
    ]),
    ])
    urwid.MainLoop(horizontal_menu(menu_top), HorizontalMenu.palette).run()

if __name__ == "__main__":
    main()
