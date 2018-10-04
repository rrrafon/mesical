import glob, re
import subprocess


DIR = r'/home/runan/Documents/mesical/clips/'
NOTES = [1, 0.5, .25, 0.125, 0.0625]  # whole nte, half, quarter, 1/8, .0625
TAIL = 0.05 #in seconds

def musicNoteFiles(filePath=DIR, fileName='piano', ext='.mp3'):
    '''
    :param filePath: Input the file directory of published files
    :param fileName: file name of assets, eg. CHAR001_Model_v001
    :param ext: extention of the filename, eg. '.ma' for Maya Ascii file
    '''

    # This will check for the predefines file format
    pattern = r'%s_\B' % (fileName)
    # files that matches proper format will be saved here
    matchingFiles = []

    try:
        # Load all files in Published Dir
        filesInPubDir = glob.glob("%s*%s" % (filePath, ext))
    except TypeError:
        print('please input file path')
        return

    # Check files in directory if filename matches the preffered file format
    # if it matches then append that to the matched file variable
    for allfiles in filesInPubDir:
        match = re.findall(pattern, allfiles)
        if match:
            matchingFiles.append(allfiles)

    return[filesInPubDir, matchingFiles]

def convertWavToMp3():
    musicFiles = musicNoteFiles()
    for i in musicFiles:
        name = i.split('/')[-1].split('.')[0]
        cmd = "ffmpeg -i %s -f mp3 %s.mp3" %(i,name)
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
            cmd = "ffmpeg -i %s -ss 0 -t %s -c copy %s%s.mp3"% (music, sec, name, i)
            #print(cmd)
            subprocess.call(cmd, shell=True)

