import datetime, json, os, pygame, shutil, stat
from btpygame import pygameimage, pygamebutton, collide


home_directory = os.path.expanduser('~')
if not(os.path.exists(home_directory + "/.savescleaner/")):
    os.mkdir(home_directory + "/.savescleaner/")
if os.path.isfile(home_directory + "/.savescleaner/options.json"):
    optionschecked = True
else:
    f = open(home_directory + "/.savescleaner/options.json", "w")
    f.writelines(["{\n",
                  '\t"multipath": "your multimc path, ex: C:/MultiMC",\n',
                  '\t"instformat": "instances name format, ex: RSG_*",\n',
                  '\t"saveformat": "saves name format, ex: Random Speedrun #*"\n',
                  '\t"recordpath": "the path of your records, ex: C:/Users/draqu/Videos"\n',
                  '\t"recordextension": "the extension of your records, ex: mkv"\n',
                  '\t"wallrecordpath": "the path of your wall records, ex: C:/Users/draqu/Videos"\n',
                  '\t"wallrecordextension": "the extension of your wall records, ex: mkv"\n',
                  '}'
    ])
    f.close()
    optionschecked = False

def deletesaves():
    f = open(home_directory + "/.savescleaner/options.json")
    data = json.load(f)
    multipath = data["multipath"]
    instformat = data["instformat"]
    saveformat = data["saveformat"]
    f.close()
    for (dirpath, dirnames, filenames) in os.walk(multipath + "/instances/"):
        # Find all instances
        for d in dirnames:
            if d.startswith(instformat.replace("*", "")):
                # Find all saves
                print("Deleting saves in instance " + d)
                for (dirpath, dirnames, filenames) in os.walk(multipath + "/instances/" + d + "/.minecraft/saves/"):
                    saveslist = []
                    for save in dirnames:
                        if save.startswith(saveformat.replace("*", "")):
                            saveslist.append(save)
                    for i in range(10):
                        if len(saveslist) > 0:
                            saveslist.pop(-1)
                    for subdir in saveslist:
                        savepath = multipath + "/instances/" + d + "/.minecraft/saves/" + subdir
                        shutil.rmtree(savepath)
                    break
                print("Saves have been deleted in " + d + " with sucess")
        break

def deletescreens():
    f = open(home_directory + "/.savescleaner/options.json")
    data = json.load(f)
    multipath = data["multipath"]
    instformat = data["instformat"]
    f.close()
    for (dirpath, dirnames, filenames) in os.walk(multipath + "/instances/"):
        # Find all instances
        for d in dirnames:
            if d.startswith(instformat.replace("*", "")):
                # Find all saves
                print("Deleting screens in instance " + d)
                for (dirpath, dirnames, filenames) in os.walk(multipath + "/instances/" + d + "/.minecraft/screenshots/"):
                    for pic in filenames:
                        os.remove(multipath + "/instances/" + d + "/.minecraft/screenshots/" + pic)
                print("Screens have been deleted in " + d + " with sucess")
        break


pygame.init()
screen = pygame.display.set_mode((339, 310))
pygame.display.set_caption('SavesCleaner by DraquoDrass')
pygame.display.set_icon(pygame.image.load('assets/brush.png'))
clock = pygame.time.Clock()
running = True
isdeleting = False
deletingsaves = False
deletingscreens = False

background = pygameimage(pygame.image.load("assets/background.png"), (0, 0))
deleting = pygameimage(pygame.image.load("assets/deleting.png"), (0, 0))
btn_clean = pygamebutton(pygame.image.load("assets/clean.png"), pygame.image.load("assets/clean.png"), (50, 10))
btn_saves = pygamebutton(pygame.image.load("assets/saves.png"), pygame.image.load("assets/saves_t.png"), (60, 80))
btn_screens = pygamebutton(pygame.image.load("assets/screens.png"), pygame.image.load("assets/screens_t.png"), (14, 150))
btn_options = pygamebutton(pygame.image.load("assets/options.png"), pygame.image.load("assets/options_t.png"), (25, 240))

while running:

    if deletingsaves:
        deletingsaves = False
        deletesaves()
    elif deletingscreens:
        deletingscreens = False
        deletescreens()

    screen.blit(background.image, background.pos)
    if optionschecked:
        btn_clean.display(screen)
        btn_saves.display(screen)
        btn_screens.display(screen)
    btn_options.display(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT and not(isdeleting):
                if collide(btn_saves, event.pos):
                    screen.blit(deleting.image, deleting.pos)
                    deletingsaves = True
                elif collide(btn_screens, event.pos):
                    screen.blit(deleting.image, deleting.pos)
                    deletingscreens = True
                elif collide(btn_options, event.pos):
                    os.startfile(home_directory + "/.savescleaner/options.json")
                    optionschecked = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
