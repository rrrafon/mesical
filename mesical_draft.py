import glob
import subprocess

DIR = r'/home/runan/Documents/mesical/clips/'
OUTDIR = r'/home/runan/Documents/mesical/outDir/'
#MUSIC = ('FS-1 E-1 D-1 CS-1 B-1 A-1 B-1 CS-1')
MUSIC = ('FS-1 O-4 E-1 O-4 D-1 O-4 CS-1 O-4 B-1 O-4 A-1 O-4 B-1 O-4 A-1 FS-1 O-4 E-1 O-4 D-1 O-4 A-1 O-4 B-1 O-4 A-1 O-4 B-1 O-4 A-1 D-4 CS-4 D-4 D-4 CS-4')

#MUSIC = ('C-1 C-1 G-1 G-1 A-1 A-1 G-1 O-1 F-1 F-1 E-1 E-1 D-1 D-1 C-1 O-1 G-1 G-1 F-1 F-1 E-1 E-1 D-1 O-1 G-1 G-1 F-1 F-1 E-1 E-1 D-1 O-4')
WHOLENOTE = 1000 #based on 120 bpm (1sec)


def musicNoteDir(filePath = DIR, ext = '.ogg'):
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
        #   adds the file path to each note to the code
        chords += '-i %s%s%s '%(dir, notes[i].split('-')[0], ext)
        #   sets delay of sound, this overlap each sound
        delays += '[%s]adelay=%s|%s[chord%s];' % (i, musicTime, musicTime, i)
        #   last part of the ffmpeg command
        mix += '[chord%s]' % str(i)
        musicTime += int(WHOLENOTE/int(notes[i].split('-')[1]))
    #   command line for ffmpeg
    cmd =  'ffmpeg %s -filter_complex "%s %samix=%s" -y %s%s%s' % (chords, delays, mix, lenNotes, OUTDIR, fileName, ext)

    #   calling window OS cmd line to run function
    subprocess.call(cmd, shell=True)

    # amplify sound
    cmd2 = 'ffmpeg -i %s%s%s -af loudnorm=I=-5:TP=0 -y %s%s2%s' % (OUTDIR, fileName, ext, OUTDIR, fileName, ext)
    print(cmd2)
    subprocess.call(cmd2, shell=True)



