import theGame

for i in range(0, 11):
    try:
        theGame.TheGame()
    except ValueError:
        print "Game {0} finished. ".format(i)
