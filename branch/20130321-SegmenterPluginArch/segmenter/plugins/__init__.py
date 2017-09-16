class SegmentMethodPlugin(object):
    name = "Base class for Segment Methods"
    description = "Base class for Segment Methods"
    setup_complete = False

    def __init__(self):
        pass

    def setup(self):
        self.setup_complete = True

    def segment(self, segmenter, text, updatefunction=None):
        raise NotImplementedError( "Abstract class is not callable" )
