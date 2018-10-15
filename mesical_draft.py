import glob
import subprocess

DIR = r'/home/runan/Documents/mesical/clips/'
OUTDIR = r'/home/runan/Documents/mesical/outDir/'
#MUSIC = ('FS-1 E-1 D-1 CS-1 B-1 A-1 B-1 CS-1')
#MUSIC = ('FS-1 O-4 E-1 O-4 D-1 O-4 CS-1 O-4 B-1 O-4 A-1 O-4 B-1 O-4 A-1 FS-1 O-4 E-1 O-4 D-1 O-4 A-1 O-4 B-1 O-4 A-1 O-4 B-1 O-4 A-1 D-4 CS-4 D-4 D-4 CS-4')
#---- twinkle twinkle
MUSIC = ('C-2 C-2 G-2 G-2 A-2 A-2 G-1 O-4 F-2 F-2 E-2 E-2 D-2 D-2 C-1 O-4 G-2 G-2 F-2 F-2 E-2 E-2 D-1 O-4 G-2 G-2 F-2 F-2 E-2 E-2 D-1 O-4')

#MUSIC = ('D1 CS1 D1 D1 CS1 A1 E1 FS1 D1 D1 CS1 B1 CS1 FS1')# A B G FS E G FS E D CS B A G FS E G FS E G FS E G FS E D E FS G A E A G FS B G A G D B B CS D CS B A G FS E B A B A G FS FS E D FS B A B CS D D CS B D D D' )
#MUSIC = ('C C G G A A G G F F E E D D C C G G F F E E D D G G F F E E D D C C G G A A G G F F E E D D C C')
#MUSIC = ('C2 C2 G2 G2 A2 A2 G1 O2 F2 F2 E2 E2 D2 D2 C1 O2 G2 G2 F2 F2 E2 E2 D1 O2 G2 G2 F2 F2 E2 E2 D1 O2')

WHOLENOTE = 1000 # based on 120 bpm (1sec)
DELAY = 0.05 # in seconds

def musicNoteDir(filePath = DIR, ext = '.mp3'):
    '''
    This script returns an array of FILES based on given file format
    from the specified folder

    :param filePath: file path to the musical notes
    :param ext: file format of music or video file
    :return: returns an array of files based on file format
    '''
    try:
        # Load all files in Published Dir
        filesInDir = glob.glob("%s*%s" % (filePath, ext))
    except TypeError:
        # catches an invalid file path
        print('please input file path')
        return
    audioFilesInDir = [i for i in filesInDir]

    return audioFilesInDir

def mixAll(dir = DIR, name = 'music_01',ext = '.mp3' ):
    '''
    this script mix all audio specified in musical chords
    :param dir: file directory where all the musical notes are saved
    :param name: name of the output file
    :param ext: extention of the input and ouput file
    :return: none
    '''

    #---
    cont = ''

    for i in MUSIC.split(' '):
        cont+=('%s%s%s|'%(dir, i, ext))
    cmd = 'ffmpeg -i "concat:%s" -c copy -y %s%s%s' % (cont, OUTDIR, name, ext)
    subprocess.call(cmd, shell=True)


def mixAllfade(dir = DIR,   ext = '.ogg', fileName = 'mixedOutput'):
    '''
    This script mixes the audio/video based on the given musical chord list
    :param dir: file directory of musical chords
    :param ext: file format of the musical chords, either a video or audio
    :return: null
    '''
    #   this var splits the list of MUSIC into individual chords
    notes = MUSIC.split(' ')
    #   count of notes in Music var
    lenNotes = len(notes)
    #   this var will store a list of audio/video file of music
    chords = ''
    #   this vars will store a list of delay filter_complex for ffmpeg
    delays = '' # adds delays to make up for the time
    mix = '' # arbitrary name for index
    #   the start time of music in milliseconds
    musicTime = 5 #initial value must be > zero

    for i in range(lenNotes):
        #   duration of each note
        duration = int(WHOLENOTE // int(notes[i].split('-')[1]))
        #   adds the file path to each note to the code
        chords += '-i %s%s%s -ss 0 -t %s -af "afade=t=out:st=0:d=%s" ' % (dir, notes[i].split('-')[0], ext, duration , duration+DELAY )

        #   sets delay of sound, this overlap each sound
        delays += '[%s]adelay=%s|%s[chord%s];' % (i, musicTime, musicTime, i)
        #   last part of the ffmpeg command
        mix += '[chord%s]' % str(i)
        musicTime += duration
    #   command line for ffmpeg
    cmd =  'ffmpeg %s -filter_complex "%s %samix=%s" -y %s%s%s' % (chords, delays, mix, lenNotes, OUTDIR, fileName, ext)

    #   calling window OS cmd line to run function
    subprocess.call(cmd, shell=True)

    # amplify sound
    cmd2 = 'ffmpeg -i %s%s%s -af loudnorm=I=-5:TP=0 -y %s%s2%s' % (OUTDIR, fileName, ext, OUTDIR, fileName, ext)
    print(cmd2)
    subprocess.call(cmd2, shell=True)
