import re
from segmenter import CJK, SegmenterResults
from segmenter.plugins import SegmentMethodPlugin

class SegmentMethodSimpleLongest(SegmentMethodPlugin):

    name = "Forward longest match"
    description = "Matches a word to the longest string it can find"

    def __init__(self):
        pass

    def segment(self, segmenter, text, updatefunction=None):
        if segmenter.tokenMatchType == 'cjk':
            tokenPattern = ''.join((CJK.cjkUnifiedIdeographs, CJK.cjkUnifiedIdeographsExtA, CJK.cjkMiddleDot, CJK.cjkKatakanaMiddleDot, CJK.cjkLingZero, CJK.cjkBopomofo, segmenter.sectionBreakChar))
        elif segmenter.tokenMatchType == 'cjk_plus_az':
            tokenPattern = ''.join((CJK.cjkUnifiedIdeographs, CJK.cjkUnifiedIdeographsExtA, CJK.cjkMiddleDot, CJK.cjkKatakanaMiddleDot, CJK.cjkLingZero, CJK.cjkFullwidthLatin, CJK.cjkBopomofo, segmenter.sectionBreakChar))
        else:
            #TODO add a self.messages and display it in the log tab
            #print "Unknown token match type %s" % self.tokenMatchType
            return None

        notTokenPattern = "[^%s]+" % tokenPattern

        results = SegmenterResults(text=text)
        idx = 0
        length = len(text)

        while idx < length:
            if updatefunction:
                updatefunction(idx * 100 / length)
            m = re.match(notTokenPattern, text[idx:])
            if m:
                results.addLexical(m.group(0), idx, isCJK=False)
                idx += len(m.group(0))
                continue
            m = re.match(segmenter.sectionBreakPattern, text[idx:])
            if m:
                results.addLexical(m.group(0), idx, segmenter.getWord(m.group(0)), isCJK = True)
                idx += len(m.group(0))
                
            else:
                j = (length - idx) if (idx + 8 > length) else 8
                while j > 1:
                    tmpword = text[idx:idx+j]
                    if segmenter.getWord(tmpword):
                        results.addLexical(tmpword, idx, segmenter.getWord(tmpword), isCJK=True)
                        ###results.addWord(tmpword, segmenter.getWord(tmpword))
                        idx += j
                        #continue
                        j = -666 # No *&^*@# labeled loops in Python
                        continue
                    j-=1

                if j == 1:
                    'TODO can this be folded with the loop above?'
                    tmpword = text[idx:idx+1]
                    results.addLexical(tmpword, idx, segmenter.getWord(tmpword), isCJK=True)
                    '''this is an unknown word; i.e., a token with no associated dictionary word'''
                    idx += 1
        
        segmenter.segmentBySentence(results, text)
        return results
