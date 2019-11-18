import logging

'''

logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
'''


def func(path, functionality, word):
    f = open(path)
    sentence = ""
    if functionality == "read":
        print("Reading")
        nOfLines = 0
        # returns a list of lines in the file
        inputString = f.readlines()
        timesPresent = 0
        # counts each paragraph as a line
        for x in inputString:
            print("The X is : " + x)
            # counts occurence in paragraph
            # doesn't count multiple oddurences
            if word in x:
                # count substring occurence
                timesPresent += x.count(word)
                nOfLines += 1
                print(timesPresent)
        print(timesPresent)
        print(nOfLines)
        f.close()
    elif functionality == "write":
        # fdsaf print("Writing")
        nOfInputWord = 0
        nOfInputSentences = 0
        nOfSentWordOccured = 0
        x = ""
        while sentence != "Exit":
            sentence = raw_input(
                "Please kindly enter the message you would like to write to a file. Use quatation marks. \nPlease press Exit to exit")
            print(sentence)
            nOfInputSentences += 1
            if x in sentence:
                # count substring occurence
                if (word in sentence):
                    nOfInputWord += sentence.count(x)
                    nOfSentWordOccured += 1
            elif sentence == "Exit":
                break
            elif input is ValueError:
                continue
        print("The user entered ", nOfInputSentences, "sentences")
        print("the word 'imperdiet appear ", nOfSentWordOccured, " times.")
        print("Word ", word, "appeared in ", nOfSentWordOccured, "sentences.")
    else:
        # throw invalid parameter EnvironmentError
        print("functionality is " + functionality)
        raise ValueError("The functionlality must be ")


func("/Users/student/Dropbox/assignment-8.txt", "write", "imperdiet")
