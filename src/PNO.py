import FileHandler as fh
import prompt_toolkit as pt
import os, datetime

def getNotebook(name):
    pnoFolder = os.path.expanduser('~/PNO/')
    try:
        root = fh.Folder(os.path.join(pnoFolder, 'Notebooks/' + name))
    except Exception as e:
        raise e
    return root

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
    kb = pt.key_binding.KeyBindings()

    @kb.add('c-q')
    def exit(event):
        event.app.exit()
    #TODO add more keys
    root = getNotebook('szkoła')


    text = pt.document.Document(text = makeDirText(root))
    displayer = pt.buffer.Buffer(read_only = True, multiline = True, document = text)

    bottomText1 = pt.layout.controls.FormattedTextControl(text = pt.HTML('<ansigreen>c-q -> exit, #TODO </ansigreen>'))
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
