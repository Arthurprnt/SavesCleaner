import json, os, pygame, shutil
from btpygame import pygameimage, pygamebutton, collide, showtext


home_directory = os.path.expanduser('~')
if os.path.isfile(home_directory + "/.savescleaner/options.json"):
    f = open(home_directory + "/.savescleaner/options.json")
    data = json.load(f)
    multipath = data["multipath"]
    instformat = data["instformat"]
    saveformat = data["saveformat"]
else:
    multipath = home_directory + "/Documents/MultiMC"
    instformat = "RSG_*"
    saveformat = "Random Speedrun #*"


def deletesaves():
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

pygame.init()
screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption('SavesCleaner by DraquoDrass')
clock = pygame.time.Clock()
running = True

background = pygameimage(pygame.image.load("assets/background.png"), (0, 0))
btn_delete = pygamebutton(pygame.transform.scale(pygame.image.load("assets/delete.png"), (200, 60)), pygame.transform.scale(pygame.image.load("assets/delete_t.png"), (200, 60)), (200, 230))

while running:

    screen.blit(background.image, background.pos)

    btn_delete.display(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if collide(btn_delete, event.pos):
                    deletesaves()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()