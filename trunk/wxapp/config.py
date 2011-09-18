'''
Copyright 2011 by Chad Redman <chad at zhtoolkit.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
'''

import os, sys, cPickle, locale, types, shutil, time
import errno

class Config(dict):

    configFileName = "config.db"
    configFileFullPath = None
    appDir = None

    dirtyDicts = False
    dirtyFilters = False

    def __init__(self, configPath):
        # TODO platform-independent
        self.configPath = configPath
        self.configFileFullPath = os.path.join(self.configPath, self.configFileName)

#        self.makeWorkingDir()
        self.load()


    def setDefaults(self):
        fields = {
            #'dicts': {"cedict_ts.u8" : "cedict"},
            'filters': [],
            'currentdir': "samples",
            'dictionaries': ['cedict_ts.u8'],
            'charset': 'simplified',
            }

        for (k,v) in fields.items():
            if not self.has_key(k):
                self[k] = v


#    def makeWorkingDir(self):
#        base = self.configPath
#        for x in (base,
#                  os.path.join(base, "plugins"),
#                  os.path.join(base, "backups")):
#            try:
#                os.mkdir(x)
#            except:
#                pass


    def save(self):
        # create directory if it doesn't exist
        try:
            os.mkdir(self.configPath, 0700)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise

        # write to a temp file
        from tempfile import mkstemp
        (fd, tmpname) = mkstemp(dir=self.configPath)
        tmpfile = os.fdopen(fd, 'w')
        cPickle.dump(dict(self), tmpfile)
        tmpfile.close()
        # the write was successful, delete config file (if exists) and rename
        if os.path.exists(self.configFileFullPath):
            os.unlink(self.configFileFullPath)
        os.rename(tmpname, self.configFileFullPath)


    def load(self):
        try:
            f = open(self.configFileFullPath)
            self.update(cPickle.load(f))
        except (IOError, EOFError):
            # Corrupted format
            pass
        self.setDefaults()

    def setDicts(self, dict_ar):
        self["dictionaries"] = dict_ar

    def setFilters(self, filter_ar):
        self["filters"] = filter_ar
