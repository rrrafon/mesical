import glob
import subprocess

DIR = r'/home/runan/Documents/mesical/clips/'
OUTDIR = r'/home/runan/Documents/mesical/outDir/'
EXT = '.ogg'
OUTNAME = 'audio_output'
WHOLENOTE = 1 # based on 120 bpm (1sec), length of each note
DELAY = 0.07 # in seconds, this overlaps music notes

#-------------> twinkle twinkle
MUSIC = ('C-2 C-2 G-2 G-2 A-2 A-2 G-1 O-4 F-2 F-2 E-2 E-2 D-2 D-2 C-1 O-4 G-2 G-2 F-2 F-2 E-2 E-2 D-1 O-4 G-2 G-2 F-2 F-2 E-2 E-2 D-1')


#MUSIC = ('FS-1 E-1 D-1 CS-1 B-1 A-1 B-1 A-1 FS-1 E-1 D-1 A-1 B-1 A-1 B-1 A-1 D-2 CS-2 D-2 D-2 CS-2')

#MUSIC = ('FS-1 E-1 D-1 CS-1 B-1 A-1 B-1 CS-1')

#MUSIC = ('D1 CS1 D1 D1 CS1 A1 E1 FS1 D1 D1 CS1 B1 CS1 FS1')# A B G FS E G FS E D CS B A G FS E G FS E G FS E G FS E D E FS G A E A G FS B G A G D B B CS D CS B A G FS E B A B A G FS FS E D FS B A B CS D D CS B D D D' )
#MUSIC = ('C C G G A A G G F F E E D D C C G G F F E E D D G G F F E E D D C C G G A A G G F F E E D D C C')
#MUSIC = ('C2 C2 G2 G2 A2 A2 G1 O2 F2 F2 E2 E2 D2 D2 C1 O2 G2 G2 F2 F2 E2 E2 D1 O2 G2 G2 F2 F2 E2 E2 D1 O2')


def musicNoteDir(filePath = DIR, ext = EXT):
    '''
    This script returns an array of FILES based on given file format
    from the specified folder

    :param filePath: file path to the musical notes
    :param ext: file format of music or video file
    :return: returns an array of files based on file format
    '''
    try:
        #-------------> Load all files in Published Dir
        filesInDir = glob.glob("%s*%s" % (filePath, ext))
    except TypeError:
        #-------------> catches an invalid file path
        print('please input file path')
        return
    audioFilesInDir = [i for i in filesInDir]

    return audioFilesInDir

def mixAllfade(amplify = True, ampVolume = -5, dir = DIR,   ext = EXT, fileName = OUTNAME):
    '''
    This script mixes the audio/video based on the given musical chord list
    :param dir: file directory of musical chords
    :param ext: file format of the musical chords, either a video or audio
    :return: null
    '''
    #------------->   this var splits the list of MUSIC into individual chords
    notes = MUSIC.split(' ')
    #------------->   count of notes in Music var
    lenNotes = len(notes)
    #------------->   this var will store a list of audio/video file of music
    chords = ''
    #------------->   this vars will store a list of delay filter_complex for ffmpeg
    delays = '' # adds delays to make up for the time
    mix = ''
    #------------->   the start time of music in milliseconds
    musicTime = 5 #initial value must be > zero

    for i in range(lenNotes):
        #------------->   duration of each note
        try:
            duration = round(WHOLENOTE / int(notes[i].split('-')[1]),2)
        except ZeroDivisionError:
            duration = WHOLENOTE
        except ValueError:
            duration = WHOLENOTE
        except TypeError:
            duration =WHOLENOTE

        #------------->   adds the file path to each note to the code
        chords += '-i %s%s%s ' % (dir, notes[i].split('-')[0], ext)

        #------------->   trims, fades and sets delay of sound, this overlap each sound
        fades = 'afade=t=out:st=%s:d=%s' % (duration - DELAY , DELAY * 2)
        trims = 'atrim=0:%s' % str(duration+DELAY)
        delays += '[%s]%s,%s,adelay=%s|%s[chord%s];' % (i,trims, fades, musicTime, musicTime, i)

        #------------->   last part of the ffmpeg command
        mix += '[chord%s]' % str(i)
        musicTime += int((duration - DELAY)*1000) # needed 1000 as multiplier to convert to milliseconds

    #-------------> command line for ffmpeg
    cmd =  'ffmpeg %s -filter_complex "%s %samix=%s" -y %s%s%s' % (chords, delays, mix, lenNotes, OUTDIR, fileName, ext)

    #-------------> calling window OS cmd line to run function
    subprocess.call(cmd, shell=True)


    if amplify:
        #-------------> amplify sound
        #cmd2 = 'ffmpeg -i %s%s%s -filter:a loudnorm -y %s%s2%s'% (OUTDIR, fileName, ext, OUTDIR, fileName, ext)
        cmd2 = 'ffmpeg -i %s%s%s  -af loudnorm=I=%s:TP=0 -y %s%s2%s' % (OUTDIR, fileName, ext, ampVolume ,OUTDIR, fileName, ext)
        subprocess.call(cmd2, shell=True)
