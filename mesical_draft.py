import glob, re
import subprocess

TMPDIR = r'/home/runan/Documents/mesical/temp/'
DIR = r'/home/runan/Documents/mesical/clips/'
MUSIC = ('D1 CS1 D1 D1 CS1 A1 E1 FS1 D1 D1 CS1 B1 CS1 FS1 A1 B1 G1 FS1 E1 G1 FS1 E1 D1 CS1 B1 A1 G1 FS1 E1 G1 FS1 E1 G1 FS1 E1 G1 FS1 E1 D1 E1 FS1 G1 A1 E1 A1 G1 FS1 B1 G1 A1 G1 D1 B1 B1 CS1 D1 CS1 B1 A1 G1 FS1 E1 B1 A1 B1 A1 G1 FS1 FS1 E1 D1 FS1 B1 A1 B1 CS1 D1 D1 CS1 B1 D1 D1 D1' )
#MUSIC = ('C C G G A A G G F F E E D D C C G G F F E E D D G G F F E E D D C C G G A A G G F F E E D D C C')
#MUSIC = ('C1 C1 G2 G1 G2 G2 A1 A1 G1')
#MUSIC = ('A1 B2 C4')
TAIL = .005#in seconds


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
    #test on music playing
    cont = ''

    for i in MUSIC.split(' '):
        cont+=('%s%s%s|'%(dir, i, ext))
        #cont += ('-i %s%s%s '% (dir, i, ext))

    cmd = 'ffmpeg -i "concat:%s" -c copy -y output.mp3' % cont
    #cmd = 'ffmpeg %s -filter_complex acrossfade=d=%s:c1=qua:c2=qua -y output.mp3' % (cont, TAIL)

    #print(cmd)
    subprocess.call(cmd, shell=True)

    #cmd2 = 'ffmpeg -i output.mp3 -filter:a "atempo=2" -vn output2.mp3'
    #subprocess.call(cmd2, shell=True)


def mixAllfade(dir = DIR,   ext = '.mp3', tempDir = TMPDIR, tempName = 'TMP101' ):
    #test on music playing
    notes = MUSIC.split(' ')
    #input1 = ''
    #input2 o= ''
    print(len(notes))
    for i in range(len(notes)):
        input1 = ('%s%s%s ' % (dir, notes[i], ext))
        try:
            input2 = ('%s%s%s ' % (dir, notes[i+1], ext))
        except IndexError:
            pass
        tempOut = '%s%s%s' % (tempDir, tempName, ext)
        if i == 0:
            cmd = 'ffmpeg -i %s -i %s -filter_complex acrossfade=d=%s:c1=qua:c2=qua -y %s' % (input1, input2, TAIL, tempOut )
        elif i == len(notes)-1:
            cmd = 'ffmpeg -i %s -i %s -filter_complex acrossfade=d=%s:c1=qua:c2=qua -y mixed_audio%s' % (tempOut, input1, TAIL, ext)
        else:
            cmd = 'ffmpeg -i %s -i %s -filter_complex acrossfade=d=%s:c1=qua:c2=qua -y %s' % (tempOut, input1, TAIL, tempOut)

        print(cmd)
        #subprocess.call(cmd, shell=True)



