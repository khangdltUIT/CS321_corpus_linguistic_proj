from RDRSegmenter import RDRSegmenter
from Utils import Utils
import sys


class DataPreprocessor:
    def __init__(self):
        self.initialSegmenter = RDRSegmenter()
        self.utils = Utils()

    def getStringInitialSegmentation(self, strs: str):
        sb = []
        line = strs.strip()
        if len(line) == 0:
            return "\n"

        wordtags = self.initialSegmenter.getInitialSegmentation(line)

        size = len(wordtags)
        for i in range(0, size):
            print(wordtags[i].form)
            if wordtags[i].tag == "B":
                #sb.append(wordtags.get(i).form + "/B ");
                sb.append(wordtags[i].form + "/B ")

            else:
                #sb.append(wordtags.get(i).form + "/I ");
                sb.append(wordtags[i].form + "/I ")
        return ''.join(sb).strip()

    def getCorpusInitialSegmentation(self, inFilePath: str):
        with open(inFilePath, 'r', encoding="utf8") as buffer:
            #print(buffer.read())
            with open(inFilePath + ".RAW.Init", 'a', encoding='utf8') as bwInit:
                with open(inFilePath + ".BI", 'a', encoding='utf8') as bw:
                    for line in buffer:
                        if line != "" and line != None and line != '\n':
                            lineStr = line
                            for regex in self.utils.NORMALIZER_KEYS:
                                if regex in lineStr:
                                    lineStr = lineStr.replace(regex, self.utils.NORMALIZER[regex])

                            sb = []

                            words = lineStr.split()
                            #print(words)
                            for word in words:
                                syllabels = word.split("_")
                                bw.write(syllabels[0] + "/B ")
                                sb.append(syllabels[0] + " ")
                                for i in range(1, len(syllabels)):
                                    bw.write(syllabels[i] + "/I ")
                                    sb.append(syllabels[i] + " ")
                            bw.write("\n")
                            #print(sb)
                            bwInit.write(self.getStringInitialSegmentation(''.join(sb) )+"\n")


if __name__ == '__main__':
    segmenter = DataPreprocessor();
    segmenter.getCorpusInitialSegmentation(r'D:\src\rdr\train\Train_gold.txt');
    print('Done')
