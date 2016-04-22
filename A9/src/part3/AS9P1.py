import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
   
    total_count = 100
    sample_size = 50

    
    parser.add_argument('-p',action='store',dest='predictions',nargs=1,help='Specified the number of blogs you wish to get.')
    parser.add_argument('-c',action='store',dest='category',nargs=1,help='File to save to list.')

    args = parser.parse_args()
    if args.predictions:
        predictions = str(args.predictions[0])
    if args.category:
        category = str(args.category[0])

    

    with open(predictions , "r") as ins1:
        arrayInput = []
        for line in ins1:
            arrayInput.append(line)

    with open(category , "r") as ins2:
        arrayTopic = []
        for line in ins2:
            arrayTopic.append(line)

    #print arrayInput[1]
    #print arrayTopic[1]


    #while i < len(arrayInput):
    #    print arrayInput[i]
    #    i = i + 1
    #print len(arrayInput)

    #while j < len(arrayTopic):
    #     print arrayTopic[j]
    #     j = j + 1
    #print len(arrayTopic)

#Calculate Precision
    
    i = 0

    while i < len(arrayTopic):

  
        j = 0
        nprediction = len(arrayInput) + 1
        pcorrect = 0
        pcorrect =  float(pcorrect)
        precision = 0
        precision = float(precision)
        recall = 0
        recall = float(recall)
        ncategory = 0
        ncategory = float(ncategory)
        fmeasure = 0
        fmeasure = float(fmeasure)
        
        a = arrayTopic[i]

        while j < len(arrayInput):

            #print arrayInput[i]
            b = arrayTopic[i]
            #print b
            
            c = '|' + b 
            c = c.replace('\n', '').replace('\r', '')
            #print c
            if c in arrayInput[j]:
                ncategory = ncategory + 1
            #print 'ncategory' + str(ncategory)

            d = '|' + b + '|' + b
            d = d.replace('\n', '').replace('\r', '')
            #print d
            if d in arrayInput[j]:
                pcorrect = pcorrect + 1
            j = j + 1
        print ''
        
        precision = pcorrect / nprediction
        recall = pcorrect / ncategory
        try:
            fmeasure = (2 * precision * recall) / (precision + recall)
        except:
            ZeroDivisionError

        print arrayTopic[i]
        print 'correct' + str(pcorrect)
        print 'nprediction ' + str(nprediction)
        print 'ncategory ' + str(ncategory)
        print 'precision ' + str(precision)
        print 'recall ' + str(recall)
        print 'fmeasure ' + str(fmeasure)

        i = i + 1
        
        

        
#Calculate Recall



        
        
        
    




