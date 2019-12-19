from pathvalidate import sanitize_filepath
import FileHandler as fh
import subprocess
import prompt_toolkit as pt
import os, datetime
import PNOPrompt as pno
Log = list()
user = 'HakierGrzonzo'

def log(message):
    global Log
    Log.append(message)

def openFile(fname):
    f = open('temp.txt', 'w+')
    subprocess.Popen(('xdg-open ' + fname).split(), stdout=f, shell=False)
    f.close()
    
folder = None
def getNotebook(name):
    pnoFolder = os.path.expanduser('~/PNO/')
    try:
        root = fh.Folder(os.path.join(pnoFolder, 'Notebooks/' + name))
    except Exception as e:
        raise e
    return root
root = getNotebook('szkoła')

def newPage(name):
    global folder
    global user
    props = fh.properties(name, 'Depracated', fh.today(), user)
    path = os.path.join(folder.dir, sanitize_filepath(name))
    folder.folders.append(fh.Folder(path, MakeNew = True, properties = props, parent = folder))

def makeDirText(folder) -> str:
    menuList = list()
    if len(folder.folders) > 0:
        menuList.append('Folders:\n')
        for x in folder.folders:
            menuList.append(pno.shortText(
                ' ' + str(len(menuList)) + '. ' + x.properties['Title'], 60) + '\n')
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
    def rerender(event):
        global folder 
        event.app.current_buffer.set_document(
                pt.document.Document(text = makeDirText(folder)),
                    bypass_readonly = True)
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
            if not num > len(folder.folders) + 1 and folder.folders != list():
                folder = folder.folders[num - 1]
                rerender(event)
            else:
                num -= len(folder.folders) + 2
                openFile(os.path.join(folder.dir, folder.files[num])) 
    
    @kb.add('h')
    def home(event):
        global folder
        global root
        folder = root
        rerender(event)
    @kb.add('b')
    def back(event):
        global folder
        if not folder.parent == None:
            folder = folder.parent
            rerender(event)
    @kb.add('n')
    def new(event):
        global folder
        name = pt.shortcuts.input_dialog(
                title= 'Name of directory',
                text = 'Enter the name of the new directory')
        if len(str(name)) > 0:
            newPage(name)
            rerender(event)

    text = pt.document.Document(text = makeDirText(root))
    displayer = pt.buffer.Buffer(read_only = True, multiline = True, document = text)

    bottomText1 = pt.layout.controls.FormattedTextControl(
            text = pt.HTML('<ansigreen>c-q -> exit, o -> open, h -> go to home dir, b -> go up a dir </ansigreen>'))
    bottomText2 = pt.layout.controls.FormattedTextControl(
            text = pt.HTML('<ansigreen>n -> new dir, m -> make new note file </ansigreen>'))
    aboveText1 = pt.layout.controls.FormattedTextControl(
            text = pt.HTML('<ansigreen>Python Note Manager v.2</ansigreen>'))

    root_container = pt.layout.containers.HSplit([
        pt.layout.containers.Window(content = aboveText1, height = 1),
        pt.layout.containers.Window(
            content = pt.layout.controls.BufferControl(displayer)),
        pt.layout.containers.Window(content = bottomText1, height = 1),
        pt.layout.containers.Window(content = bottomText2, height = 1)
        ])

    layout = pt.layout.Layout(root_container)
    app = pt.Application(key_bindings = kb, layout = layout, full_screen = True)
    app.run()


if __name__ == '__main__':
    pno.initialize()
    main()
    for x in Log:
        print(x)
