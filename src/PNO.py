import FileHandler as fh
import subprocess
import prompt_toolkit as pt
import os, datetime
Log = list()
def log(message):
    global Log
    Log.append(message)

folder = None
def getNotebook(name):
    pnoFolder = os.path.expanduser('~/PNO/')
    try:
        root = fh.Folder(os.path.join(pnoFolder, 'Notebooks/' + name))
    except Exception as e:
        raise e
    return root
root = getNotebook('szkoła')

def makeDirText(folder) -> str:
    menuList = list()
    if len(folder.folders) > 0:
        menuList.append('Folders:\n')
        for x in folder.folders:
            menuList.append(' ' + str(len(menuList)) + '. ' + x.properties['Title'] + '\n')
    if len(folder.files) > 0:
        menuList.append('Files:\n')
        for x in folder.files:
            menuList.append(' ' + str(len(menuList)) + '. ' + x + '\n')
    if len(menuList) > 0:
        res = str()
        for x in menuList:
            res += x
        return res
    else:
        return 'Wow such empty...'

def main():
    global root
    global folder
    kb = pt.key_binding.KeyBindings()
    folder = root

    @kb.add('c-q')
    def exit(event):
        event.app.exit()
    
    @kb.add('o')
    def open(event):
        global folder
        line = event.app.current_buffer.document.current_line
        if line[0] == ' ':
            num = int(line[1:line.find('.')])
            if not num > len(folder.folders) + 1:
                folder = folder.folders[num - 1]
                event.app.current_buffer.set_document(pt.document.Document(text = makeDirText(folder)), bypass_readonly = True)
            else:
                num -= len(folder.folders) + 2
                log(num)
                os.system('xdg-open ' + os.path.join(folder.dir, folder.files[num]))
    #TODO add more keys

    text = pt.document.Document(text = makeDirText(root))
    displayer = pt.buffer.Buffer(read_only = True, multiline = True, document = text)

    bottomText1 = pt.layout.controls.FormattedTextControl(text = pt.HTML('<ansigreen>c-q -> exit, o -> open </ansigreen>'))
    aboveText1 = pt.layout.controls.FormattedTextControl(text = pt.HTML('<ansigreen>Python Note Manager v.2</ansigreen>'))

    root_container = pt.layout.containers.HSplit([
        pt.layout.containers.Window(content = aboveText1),
        pt.layout.containers.Window(content = pt.layout.controls.BufferControl(displayer)),
        pt.layout.containers.Window(content = bottomText1)
        ])

    layout = pt.layout.Layout(root_container)
    app = pt.Application(key_bindings = kb, layout = layout, full_screen = True)
    app.run()


if __name__ == '__main__':
    main()
    for x in Log:
        print(x)
