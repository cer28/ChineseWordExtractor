'''
Copyright 2011 by Chad Redman <chad at zhtoolkit.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
'''

import segmenter
import os


# The data here gets refreshed when called
class SegmenterHelper:
    #from segmenter import Dictionary, Statistics, Segmenter

    def addMessage(self, text):
        self.messages.append(unicode(text, "utf-8"))

    def getMessages(self):
        return "\n".join(self.messages)
    
    def setText(self, text):
        self.text = text

    def __init__(self, runningDir):
        self.text = ''
        self.results = ''
        self.summary = ''
        self.messages = []
        self.runningDir = runningDir

    def LoadData(self, config):
        self.dicts = []
        #for dictname in ['dict\\cedict_ts.u8', 'dict\\Harry Potter.u8']:
        #for dictname in ['dict\\cedict_ts.u8']:
        for dictname in config['dictionaries']:
            self.addMessage("Loading dictionary %s ..." % dictname)
            dict = segmenter.Dictionary( os.path.join(config.appDir, 'dict', dictname), format='cedict', verbose=True)

            if dict.messages != None:
                for elem in dict.messages:
                    self.addMessage(elem)
                # add a blank line

            self.addMessage("Loaded dictionary %s, %d words" % (dictname, dict.getWordCount()))
            self.addMessage("")

            self.dicts.append(dict)

        self.stats=[]
        self.stats.append(segmenter.Statistics(os.path.join(config.appDir, 'data/HSK Levels.U8'), 'tab', 'hsk_level', 'simplified'))
        self.stats.append(segmenter.Statistics(os.path.join(config.appDir, 'data', 'Freq per Million.U8'), 'tab', 'frequency_per_million', 'simplified'))
        self.stats.append(segmenter.Statistics(os.path.join(config.appDir, 'data', 'simp Chengyu num sources.u8'), 'tab', 'chengyu_num_sources', 'simplified'))

        self.filterwords = []
        #self.LoadKnownWords('filter/simp-Chad Words.u8')
        
        self.seg = segmenter.Segmenter('simplified', self.dicts, self.stats)

    def LoadKnownWords(self, filename):
        fh = open(filename)  #throws IOError
        lineno = 0
        try:
            for line in fh.read().splitlines():
                lineno += 1
                if not re.match('\s*#', unicode(line, "utf-8")):
                    m = re.match('[^\t]+', unicode(line, "utf-8"))
                    if m:
                        self.filterwords.append(m.group(0))
        finally:
            fh.close()
        
        return lineno

    def ReadFiles(self, filelist):
        # Autodetect the encoding, so that the user doesn't need to worry about utf8 vs. utf16, little endian, etc
        # uses the chardet module from:
        # http://chardet.feedparser.org/
        # Universal Encoding Detector: character encoding auto-detection in Python
        import chardet

        text = ''
        filelist.sort()
        for f in filelist:
            try:
                #text += '%s [%s]\n%s' % (segmenter.Segmenter.sectionBreakChar, f, unicode(open(f, 'r').read(), encoding))
                rawdata = open(f, 'rb').read(-1)

                detector = chardet.detect(rawdata)
                self.addMessage("File %s loaded: %i bytes" % (f.encode('utf-8'), len(rawdata)))
                self.addMessage("Detected encoding: %s\n" % detector)
                text += '%s [%s]\n%s' % (segmenter.Segmenter.sectionBreakChar, f, unicode(rawdata, detector["encoding"]))
            except UnicodeDecodeError, e:
                self.addMessage("%s error while loading file %s: failed to decode from encoding '%s'. Filesize was %d" % (type(e), f, detector["encoding"], len(rawdata)))
                
        
        self.text = text
        return self.text

    def SummarizeResults(self):
        self.summary = ''
        self.results = ''

        self.addMessage("Analyzing text ...")

        self.summary += "Length of text = %d" % len(self.text) + "\n"
        results = self.seg.segment(self.text)
        self.summary += "\n\nResults.tokens (%d)" % len(results.tokens) + "\n"

#        for lex in results.tokens:
#            sys.stdout.write(lex.text)

        self.results +=  '\t'.join( ("Word num.", "Running total words", "text", "num. occur.", "1st occur.", "HSK level", "Freq per Mil", "num. chengyu src", "traditional", "simplified", "pinyin", "english", "sample sentence") ) + "\n"

        wordctGross = 0
        wordctNet = 0
        wordUniqueGross = 0
        wordUniqueNet = 0

        for lex in results.lexList:
            word = results.words[lex.text]
            if word == None:
                self.results +=  '\t'.join(
                            (
                             '',
                             '',
                             lex.text,
                             str(len(lex.indexes)),
                             str(lex.indexes[0]),
                             '',
                             '',
                             '',
                             'Unknown',
                             ''
                            )
                        ) + "\n"
            elif word.isSectionBreak():
                self.results +=  "-------------------\t%s" % (lex.text) + "\n"
            else:
                wordctGross += len(lex.indexes)
                wordUniqueGross += 1
                if lex.text not in self.filterwords:
                    #print '\t'.join( (lex.text, str(len(lex.indexes)), str(lex.indexes[0]), word.getStatistic('hsk_level'), word.getStatistic('frequency_per_million'), word.getStatistic('chengyu_num_sources'), str(word.getDefinition()), str(results.findFirstSentence(lex))) )
                    wordUniqueNet += 1
                    wordctNet += len(lex.indexes)
                    self.results +=  '\t'.join(
                            (
                             str(wordUniqueNet),
                             str(wordctNet),
                             lex.text,
                             str(len(lex.indexes)),
                             str(lex.indexes[0]),
                             word.getStatistic('hsk_level'),
                             word.getStatistic('frequency_per_million'),
                             word.getStatistic('chengyu_num_sources'),
                             word.getDefinition(),
                             results.findFirstSentence(lex)
                            )
                        ) + "\n"
                    #self.results +=  '\t'.join( (str(wordUniqueNet), str(wordctNet))) + "\t"
                    #self.results +=  '\t'.join( (str(wordUniqueNet), lex.text)) + "\t"
                    #self.results +=  '\t'.join( (str(wordUniqueNet), str(len(lex.indexes)), str(lex.indexes[0]), word.getStatistic('hsk_level'), word.getStatistic('frequency_per_million'), word.getStatistic('chengyu_num_sources'))) + "\t"
                    #self.results +=  '\t'.join( ( unicode(word.getDefinition(), "utf-8") )) + "\t"
                    #self.results +=  '\t'.join( (results.findFirstSentence(lex))) + "\n"
        
        self.summary += "\n\nTotal count of Chinese words in text: %d" % wordctGross + "\n"
        self.summary += "Total count of filtered Chinese words: %d" % wordctNet + "\n"
        self.summary += "\nTotal count of unique Chinese words: %d" % wordUniqueGross + "\n"
        self.summary += "Total count of unique filtered Chinese words: %d" % wordUniqueNet + "\n"
