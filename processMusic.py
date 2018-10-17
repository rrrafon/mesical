import glob, re
import subprocess


DIR = r'/home/runan/Documents/mesical/clips/'
TAIL = 0.1 #in seconds
WHOLENOTE = 2.0 #length of each note in seconds

def musicNoteFiles(filePath= DIR, ext='.wav'):
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

def trimNotes(fadeOut = 0.4):
    '''
    this script trims the audio in specified length and add a fade out effect
    :param noteLen: length of musical note in seconds
    :param fadeOut: length of fadeout in seconds
    :return: none

    '''
    musicFiles = musicNoteFiles()
    for music in musicFiles:
        cmd = 'ffmpeg -i %s -ss 0 -t %s -af "afade=t=out:st=1:d=%s" %s' % (music, WHOLENOTE, music.split('/')[-1], fadeOut)
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
        cmd = "ffmpeg -i %s -acodec libvorbis %s.%s" % (i, name, format)
        subprocess.call(cmd, shell=True)

def createNotes(ext = 'mp3', bpm = 120):
    suffix = [1, 2, 4]#, 8, 16]
    musicFiles = musicNoteFiles()

    for i in suffix:
        numFrames = (60 / bpm)
        sec = round(numFrames / i, 2) + TAIL

        # print(numFrames)
        for music in musicFiles:
            name = music.split('/')[-1].split('.')[0]
            cmd = "ffmpeg -i %s -ss 0 -t %s -c copy %s%s%s.%s"% (music, sec, DIR, name, i, ext)
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
