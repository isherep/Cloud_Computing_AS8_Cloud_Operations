import logging
import time

'''
debug(msg, *args, **kwargs)
There are four keyword arguments in kwargs which are inspected: exc_info, stack_info, stacklevel and extra.
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
# If some execution time takes too long - throw the warning log?

# if somehow trace level was not created - log critical?
# if logger is null - error, critical?

'''

TRACE_LEVEL = 5
# creating custom trace level of logging
def trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LEVEL):
        # Yes, logger takes its '*args' as 'args'.
        self._log(TRACE_LEVEL, message, args, **kws)
logging.addLevelName(TRACE_LEVEL, "TRACE")
#add trace level to a logger
logging.Logger.trace = trace

logging.basicConfig(format='%(asctime)s %(message)s')
#set the format, min level as tracing, file and filemode
logging.basicConfig(format='%(asctime)s %(message)s % level', level=5, filename="consoleapp.log", filemode="write")

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

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


def func(path, functionality, word):
    if path is "":
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
        printWordCountMetrics(timesPresent, nOfLines, word)
        f.close()
        log.debug("File closed")

    elif functionality == "write":
        # When in "write" mode
        # Average time to write a line in the file
        # Average time to find the word "imperdiet" in the line
        log.info("User chosed " + functionality)
        nOfInputWord = 0
        nOfInputSentences = -1
        nOfSentWordOccured = 0
        totalTimeToFindWordInAllLines = 0
        totalTimeToWriteLines = 0
        try:
            f = open(path, "write")
        except Exception as exception:
            log.error("Can not open file." + path, exc_info=True)
            print ("Can not open file: " + path)
        except IOError as e:
            log.error("File not open for writing.")
        while sentence != "Exit":
            log.debug("Entered loop menu asking user to enter sentences.")
            sentence = raw_input(
                "\nPlease kindly enter the message you would like to write to a file. Use quatation marks. \nPlease press Exit to exit and count\n\n")
            start = time.time()
            f.write(sentence)
            end = time.time()
            timeToWriteALine = end - start
            totalTimeToWriteLines += timeToWriteALine
            nOfInputSentences += 1
            # start = time.time()
            nOfInputWord, nOfSentWordOccured, \
                            timeToFindWord = incrementCounts(sentence, nOfSentWordOccured,
                                                                               nOfInputWord, word)
            # end = time.time()

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
        # calculate everage time for all iterations
        evarageTimeToWriteLines = totalTimeToWriteLines /nOfInputSentences
        everageTime = totalTimeToFindWordInAllLines / nOfInputSentences
        print "\nEverage time to find a word in the sentence " + "%.6f" % (everageTime) + "seconds."
        print "Everage time to write a sentence to a file is " + "%.6f" %(evarageTimeToWriteLines) + "seconds."
        log.info("User finished entering input, printing the results.")
        log.debug("Finished input loop, printing the results.")
        print("The user entered " + str(nOfInputSentences) + " sentences")
        printWordCountMetrics(nOfInputWord, nOfSentWordOccured, word)
    else:
        # throw invalid parameter EnvironmentError
        log.error("User entered not existant choice of action with the file instead of read/write: " + functionality)
        log.error("Choice entered : " + functionality + "does not exist")
        raise ValueError("The functionality must be read or write only")


def printWordCountMetrics(nOfInputWord, nOfSentWordOccured, word):
    print("the word 'imperdiet appear " + str(nOfInputWord) + " time(s).")
    print("Word " + word + " appeared in " + str(nOfSentWordOccured) + " sentence(s).")

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



# Testing
func("/Users/student/Dropbox/assignment-8.txt", "write", "imperdiet")
