import glob, re
import subprocess


DIR = r'/home/runan/Documents/mesical/clips/'
#MUSIC = ('D CS D D CS A E FS D D CS B CS FS A B G FS E G FS E D CS B A G FS E G FS E G FS E G FS E D E FS G A E A G FS B G A G D B B CS D CS B A G FS E B A B A G FS FS E D FS B A B CS D D CS B D D D' )
MUSIC = ('C C G G A A G G F F E E D D C C G G F F E E D D G G F F E E D D C C G G A A G G F F E E D D C C')
def musicNoteDir(filePath = DIR, ext = '.mp3'):

    try:
        # Load all files in Published Dir
        filesInDir = glob.glob("%s*%s" % (filePath, ext))
    except TypeError:
        print('please input file path')
        return
    mp3filesInDir = [i for i in filesInDir]
    return mp3filesInDir

def test_All():
    cmdFile = ''
    musicFiles = musicNoteDir()
    for i in musicFiles:
        cmdFile += '%s|' % i
    #command line for joining audio/video as one file
    cmd = 'ffmpeg -i "concat:%s" -c copy output.mp3'%cmdFile
    #calling window OS cmd line to run function
    #subprocess.call(cmd, shell=True)
    print(cmdFile)
def mixAll(dir = DIR, ext = '.mp3' ):
    cont = ''

    for i in MUSIC.split(' '):
        cont+=('%s%s%s|'%(dir, i, ext))
    cmd = 'ffmpeg -i "concat:%s" -c copy output.mp3' % cont
    subprocess.call(cmd, shell=True)
    cmd2 = 'ffmpeg -i output.mp3 -filter:a "atempo=1.5" -vn output2.mp3'
    subprocess.call(cmd2, shell=True)

mixAll()
