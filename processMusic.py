import glob, re
import subprocess


DIR = r'/home/runan/Documents/mesical/clips/'
NOTES = [1, 0.5, .25, 0.125, 0.0625]  # whole nte, half, quarter, 1/8, .0625
TAIL = 0.1 #in seconds

def musicNoteFiles(filePath= DIR, ext='.ogg'):
    '''
    :param filePath: Input the file directory of published files
    :param fileName: file name of assets, eg. CHAR001_Model_v001
    :param ext: extention of the filename, eg. '.ma' for Maya Ascii file
    '''

    try:
        # Load all files in Published Dir
        filesInPubDir = glob.glob("%s*%s" % (filePath, ext))
    except TypeError:
        print('please input file path')
        return

    return(filesInPubDir)#, matchingFiles]

def trimNotes(noteLen = 1.4, fadeOut = 0.4):
    '''
    this script trims the audio in specified length and add a fade out effect
    :param noteLen: length of musical note in seconds
    :param fadeOut: length of fadeout in seconds
    :return: none

    '''
    musicFiles = musicNoteFiles()
    for music in musicFiles:
        cmd = 'ffmpeg -i %s -ss 0 -t %s -af "afade=t=out:st=1:d=%s" %s' % (music, noteLen, music.split('/')[-1], fadeOut)
        subprocess.call(cmd, shell=True)

def convertAudio(format = 'ogg'):
    '''
    This script converts the audio files in the DIR folder to specified format
    :param format: format the audio will be converted to
    :return: none
    '''
    musicFiles = musicNoteFiles()
    for i in musicFiles:
        name = i.split('/')[-1].split('.')[0]
        cmd = "ffmpeg -i %s -f mp3 %s.%s" % (i, name, format)
        subprocess.call(cmd, shell=True)


def createNotes(bpm = 120):
    suffix = [1, 2, 4]#, 8, 16]
    musicFiles = musicNoteFiles()[0]

    for i in suffix:
        numFrames = (60 / bpm)
        sec = round(numFrames / i, 2) + TAIL

        # print(numFrames)
        for music in musicFiles:
            name = music.split('/')[-1].split('.')[0]
            cmd = "ffmpeg -i %s -ss 0 -t %s -c copy %s%s%s.mp3"% (music, sec, DIR, name, i)
            #print(cmd)
            subprocess.call(cmd, shell=True)

def createSilence(name = 'O'):
    '''
    This script creates a silent sound and saves it
    :param name: file name of silent sound
    :return: none
    '''
    cmd = 'ffmpeg -f lavfi -i anullsrc -t 5 -c:a libvorbis %s.ogg' % name
    subprocess.call(cmd, shell=True)
