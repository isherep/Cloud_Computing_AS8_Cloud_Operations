import logging
import time

'''
This application requires user to specify the read or write mode in the parameter when calling myConsoleApp function
The available parameters are "read" or "write".
'''

TRACE_LEVEL = 5
logFormat = '%(asctime)s - %(levelname)s - %(message)s'
nameOfInput = ""

# creating custom trace level of logging
def trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LEVEL):
        # Yes, logger takes its '*args' as 'args'.
        self._log(TRACE_LEVEL, message, args, **kws)
#adding custom trace level to the logging
logging.addLevelName(TRACE_LEVEL, "TRACE")
# add trace level to a logger
logging.Logger.trace = trace

# create console handler and set level to debug
ch = logging.FileHandler("countoccurences.log", "write")
ch.setLevel(logging.DEBUG)
# set the format, min level as tracing, file and filemode
logging.basicConfig(format=logFormat, level = 5, filename = "countoccurences.log", filemode = "w")
log = logging.getLogger("my-logger")

# check if log object succesfully created
if log is None:
    raise Exception("Logger was not created successfuly")
# check and make sure if trace level was created
if hasattr(log, 'trace'):
    log.debug("Custom trace attribute was created.")
else:
    log.warn("Trace attribute was not created. Create the custom level trace before logging trace levels. "
             "If logging at trace level is present, but no trace attribute created - the application will crash")
    print("Trace attribute was not created. Create the custom level trace before logging trace levels")

# parameters - a file path, a read/write mode, and a word to be searched
def myConsoleApp(path, functionality, word):
    if len(path) is 0:
        log.error("No file path provided, cannot have empty path")
    if functionality is "" or word is "":
        log.info("Functionality or word to search for are blank")
        log.debug("Functionality  or word searched  are empty strings")
    try:
        f = open(path)
        # if file is null
        if f is None:
            log.error("The file is null")
        log.info("Opened file")
    except (SystemExit, KeyboardInterrupt):
        log.debug("Operation was interrupted")
        raise
    except Exception as exception:
        log.error("Can not open file." + path, exc_info=True)
        print ("Can not open file: " + path)
    sentence = ""

    if functionality == "read":
        log.info("Chosen " + functionality)
        nOfLines = 0
        # returns a list of lines in the file
        start = time.time()
        inputString = f.readlines()
        end = time.time()


        print("Time to read all lines from the file: " + "%.6f" % (end - start) + ' seconds')
        if inputString is None:
            log.warn("The output of reading a file is null.")
        elif len(inputString) == 0:
            log.info("File content was empty")
            log.debug("No lines are found in the file. Read successfully.")
        else:
            log.debug("Read all the lines completed successfuly.")
        timesPresent = 0
        # counts each paragraph as a line
        for eachLine in inputString:
            log.trace("The line in the input string read: " + eachLine)
            nOfLines, timesPresent, timeToFindWord = incrementCounts(eachLine, nOfLines, timesPresent, word)

        log.debug("Counting lines and specified words completed")
        printWordCountMetrics(timesPresent, nOfLines, word, functionality)
        f.close()
        log.debug("File closed")

    elif functionality == "write":
        nameOfInput = "sentences"
        # writing to the same file in the append mode, adding new sentences to the end
        log.info("User chosed " + functionality)
        nOfInputWord = 0
        nOfInputSentences = -1
        nOfSentWordOccured = 0
        totalTimeToFindWordInAllLines = 0
        totalTimeToWriteLines = 0
        try:
            f = open(path, "a")
            while sentence != "Exit":
                log.debug("Entered loop menu asking user to enter sentences.")
                sentence = raw_input(
                    "\nPlease kindly enter the message you would like to write to a file. Use quatation marks. \nPlease press Exit to exit and count\n\n")
                start = time.time()
                f.write('\n' + sentence)
                end = time.time()
                timeToWriteALine = end - start
                totalTimeToWriteLines += timeToWriteALine
                nOfInputSentences += 1
                nOfInputWord, nOfSentWordOccured, \
                timeToFindWord = incrementCounts(sentence, nOfSentWordOccured,
                                                 nOfInputWord, word)
                totalTimeToFindWordInAllLines += timeToFindWord
                log.debug("Counting number of sentences and number of time the word occurred completed")
                if sentence == "Exit":
                    log.info("User made choice Exit, exiting")
                    log.debug("User terminated the menu loop")
                    f.close()
                    log.debug("File closed")
                    break
                elif input is ValueError:
                    log.error("User entered incorrect choice, raised ValueError, continuing")
                    continue
        except Exception as exception:
            log.error("Can not open file." + path, exc_info=True)
            print ("Can not open file: " + path)
        except IOError as e:
            log.error("File not open for writing.")

        # calculate everage time for all iterations, only if the divisor is not 0
        if nOfInputSentences != 0:
            log.trace("The total number of sentences entered was " + str(nOfInputSentences))
            evarageTimeToWriteLines = everage(nOfInputSentences, totalTimeToWriteLines)
            everageTime = everage(nOfInputSentences, totalTimeToFindWordInAllLines)
            printPerfomanceMetrics(evarageTimeToWriteLines, everageTime)

        log.info("User finished entering input, printing the results.")
        log.debug("Finished input loop, printing the results.")
        print("The user entered " + str(nOfInputSentences) + " sentences")
        printWordCountMetrics(nOfInputWord, nOfSentWordOccured, word, functionality)
    else:
        # throw invalid parameter Error
        log.error("User entered not existant choice of action with the file instead of read/write: " + functionality)
        log.error("Choice entered : " + functionality + "does not exist")
        raise ValueError("The functionality must be read or write only")




# ----------------HELPER FUNCTIONS------------------------
def everage(nOfInputSentences, totalTimeToWriteLines):
    evarageTimeToWriteLines = totalTimeToWriteLines / nOfInputSentences
    return evarageTimeToWriteLines


def printPerfomanceMetrics(evarageTimeToWriteLines, everageTime):
    print "\nEverage time to find a word in the sentence " + "%.6f" % (everageTime) + " seconds."
    print "Everage time to write a sentence to a file is " + "%.6f" % (evarageTimeToWriteLines) + " seconds."

def printWordCountMetrics(nOfInputWord, nOfSentWordOccured, word, functionality):
    if functionality == "read":
        nameOfInput = " line(s) "
    else:
        nameOfInput = " sentence(s) "
    print("The word '" + word + "' appear " + str(nOfInputWord) + " time(s).")
    print("Word " + word + " appeared in " + str(nOfSentWordOccured) + nameOfInput)

def incrementCounts(eachLine, nOfLines, timesPresent, word):
    start = time.time()
    if word in eachLine:
        # count substring occurence
        log.trace("The word in eachline is : " + word)
        timesPresent += eachLine.count(word)
        log.trace("Times the word present : " + word)
        nOfLines += 1

        log.trace("Number of lines/sentences the word present : " + str(nOfLines))
        log.debug("Counting lines and word occurrences in method incrementCounts completed successfully.")
    end = time.time()
    timeToFindWord = end - start
    return nOfLines, timesPresent, timeToFindWord

# ----------------TESTING------------------------
myConsoleApp("/Users/student/Dropbox/assignment-8.txt", "read", "imperdiet")


#Cookie
