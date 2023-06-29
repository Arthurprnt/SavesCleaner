import json, os, pygame, shutil


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

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()