import datetime, json, os, pygame, shutil, stat, threading
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
                  '\t"saveformat": "saves name format, ex: Random Speedrun #*",\n',
                  '\t"recordpath": "the path of your records, ex: C:/Users/draqu/Videos",\n',
                  '\t"recordextension": "the extension of your records, ex: mkv",\n',
                  '\t"wallrecordpath": "the path of your wall records, ex: C:/Users/draqu/Videos",\n',
                  '\t"wallrecordextension": "the extension of your wall records, ex: mkv"\n',
                  '}'
    ])
    f.close()
    optionschecked = False
threads = {}

class deleteinst(threading.Thread):
    def __init__(self, thread_name, thread_ID, instance):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.instance = instance
        self.done = False

        # helper function to execute the threads

    def run(self):
        f = open(home_directory + "/.savescleaner/options.json")
        data = json.load(f)
        multipath = data["multipath"]
        instformat = data["instformat"]
        saveformat = data["saveformat"]
        f.close()
        if self.instance.startswith(instformat.replace("*", "")):
            # Find all saves
            print("Deleting saves in instance " + self.instance)
            for (dirpath, dirnames, filenames) in os.walk(multipath + "/instances/" + self.instance + "/.minecraft/saves/"):
                saveslist = []
                for save in dirnames:
                    if save.startswith(saveformat.replace("*", "")):
                        saveslist.append(save)
                for i in range(10):
                    if len(saveslist) > 0:
                        saveslist.pop(-1)
                for subdir in saveslist:
                    savepath = multipath + "/instances/" + self.instance + "/.minecraft/saves/" + subdir
                    shutil.rmtree(savepath)
                break
            print("Saves have been deleted in " + self.instance + " with sucess")
        self.done = True

def deletesaves(threads):
    f = open(home_directory + "/.savescleaner/options.json")
    data = json.load(f)
    multipath = data["multipath"]
    f.close()
    n = 1
    for (dirpath, dirnames, filenames) in os.walk(multipath + "/instances/"):
        # Find all instances
        for d in dirnames:
            threads[str(n)] = deleteinst(d, n, d)
            threads[str(n)].start()
            n += 1
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

def deletelogs():
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
                print("Deleting logs in instance " + d)
                for (dirpath, dirnames, filenames) in os.walk(multipath + "/instances/" + d + "/.minecraft/logs/"):
                    for log in filenames:
                        file_stat = os.stat(multipath + "/instances/" + d + "/.minecraft/logs/" + log)
                        access_timestamp = datetime.datetime.fromtimestamp(file_stat[stat.ST_MTIME])
                        elapsed = datetime.datetime.now() - access_timestamp
                        if elapsed.days > 365:
                            os.remove(multipath + "/instances/" + d + "/.minecraft/logs/" + log)
                print("Logs have been deleted in " + d + " with sucess")
        break

def deletevids():
    f = open(home_directory + "/.savescleaner/options.json")
    data = json.load(f)
    recordpath = data["recordpath"]
    recordextension = data["recordextension"]
    f.close()
    for (dirpath, dirnames, filenames) in os.walk(recordpath + "/"):
        # Find all instances
        vidtodelete = []
        for f in filenames:
            if f.endswith(recordextension):
                vidtodelete.append(f)
        break
    vidtodelete.pop(-1)
    for i in vidtodelete:
        os.remove(recordpath + "/" + i)

def deletewallvids():
    f = open(home_directory + "/.savescleaner/options.json")
    data = json.load(f)
    wallrecordpath = data["wallrecordpath"]
    wallrecordextension = data["wallrecordextension"]
    f.close()
    for (dirpath, dirnames, filenames) in os.walk(wallrecordpath + "/"):
        # Find all instances
        vidtodelete = []
        for f in filenames:
            if f.endswith(wallrecordextension):
                vidtodelete.append(f)
        break
    vidtodelete.pop(-1)
    for i in vidtodelete:
        os.remove(wallrecordpath + "/" + i)

pygame.init()
screen = pygame.display.set_mode((339, 520))
pygame.display.set_caption('SavesCleaner by DraquoDrass')
pygame.display.set_icon(pygame.image.load('assets/brush.png'))
clock = pygame.time.Clock()
running = True
isdeleting = False

background = pygameimage(pygame.image.load("assets/background.png"), (0, 0))
deleting = pygameimage(pygame.image.load("assets/deleting.png"), (0, 0))
btn_clean = pygamebutton(pygame.image.load("assets/clean.png"), pygame.image.load("assets/clean.png"), (50, 10))
btn_saves = pygamebutton(pygame.image.load("assets/saves.png"), pygame.image.load("assets/saves_t.png"), (60, 80))
btn_screens = pygamebutton(pygame.image.load("assets/screens.png"), pygame.image.load("assets/screens_t.png"), (14, 150))
btn_logs = pygamebutton(pygame.image.load("assets/logs.png"), pygame.image.load("assets/logs_t.png"), (85, 220))
btn_records = pygamebutton(pygame.image.load("assets/records.png"), pygame.image.load("assets/records_t.png"), (17, 290))
btn_wall = pygamebutton(pygame.image.load("assets/wall.png"), pygame.image.load("assets/wall_t.png"), (92, 360))
btn_options = pygamebutton(pygame.image.load("assets/options.png"), pygame.image.load("assets/options_t.png"), (25, 450))

while running:

    screen.blit(background.image, background.pos)
    if optionschecked:
        btn_clean.display(screen)
        btn_saves.display(screen)
        btn_screens.display(screen)
        btn_logs.display(screen)
        btn_records.display(screen)
        btn_wall.display(screen)
    btn_options.display(screen)

    if isdeleting:
        screen.blit(deleting.image, deleting.pos)
        finished = True
        for i in threads.keys():
            if threads[i].done == False:
                finished = False
        if finished:
            isdeleting = False
            threads = {}

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if collide(btn_saves, event.pos) and not(isdeleting):
                    isdeleting = True
                    deletesaves(threads)
                elif collide(btn_screens, event.pos):
                    screen.blit(deleting.image, deleting.pos)
                    deletescreens()
                elif collide(btn_logs, event.pos):
                    screen.blit(deleting.image, deleting.pos)
                    deletelogs()
                elif collide(btn_records, event.pos):
                    screen.blit(deleting.image, deleting.pos)
                    deletevids()
                elif collide(btn_wall, event.pos):
                    screen.blit(deleting.image, deleting.pos)
                    deletewallvids()
                elif collide(btn_options, event.pos):
                    os.startfile(home_directory + "/.savescleaner/options.json")
                    optionschecked = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
