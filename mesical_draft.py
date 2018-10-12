import glob
import subprocess

DIR = r'/home/runan/Documents/mesical/clips/'
OUTDIR = r'/home/runan/Documents/mesical/outDir/'
MUSIC = ('D-1 CS-1 D-1 D-1 CS-1 A-1 E-1 FS-1 D-1 D-1 CS-1 B-1')
WHOLENOTE = 500 #based on 120 bpm
#MUSIC = ('D1 CS1 D1 D1 CS1 A1 E1 FS1 D1 D1 CS1 B1 CS1 FS1 A1 B1 G1 FS1 E1 G1 FS1 E1 D1 CS1 B1 A1 G1 FS1 E1 G1 FS1 E1 G1 FS1 E1 G1 FS1 E1 D1 E1 FS1 G1 A1 E1 A1 G1 FS1 B1 G1 A1 G1 D1 B1 B1 CS1 D1 CS1 B1 A1 G1 FS1 E1 B1 A1 B1 A1 G1 FS1 FS1 E1 D1 FS1 B1 A1 B1 CS1 D1 D1 CS1 B1 D1 D1 D1' )
#MUSIC = ('C C G G A A G G F F E E D D C C G G F F E E D D G G F F E E D D C C G G A A G G F F E E D D C C')
#MUSIC = ('A1 G1 C1')


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
    mp3filesInDir = [i for i in filesInDir]

    return mp3filesInDir


def mixAllfade(dir = DIR,   ext = '.mp3', fileName = 'mixedOutput'):
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
        #   adds the file path to each note to the code
        chords += '-i %s%s%s '%(DIR, notes[i].split('-')[0], ext)
        #   sets delay of sound, this overlap each sound
        delays += '[%s]adelay=%s|%s[chord%s];' % (i, musicTime, musicTime, i)
        #   last part of the ffmpeg command
        mix += '[chord%s]' % str(i)
        musicTime += int(WHOLENOTE/int(notes[i].split('-')[1]))

    cmd =  'ffmpeg %s -filter_complex "%s %samix=%s" -y %s%s%s' % (chords, delays, mix, lenNotes, OUTDIR, fileName, ext)
    print(cmd)

    #   calling window OS cmd line to run function
    subprocess.call(cmd, shell=True)


