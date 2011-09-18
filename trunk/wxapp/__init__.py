'''
Copyright 2011 by Chad Redman <chad at zhtoolkit.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
'''

import wx

config = None

def run(segHelper):
    import os, sys, optparse
    #import config
    import ui, config

    # parse args
    parser = optparse.OptionParser()
    parser.usage = "%prog"
    parser.add_option("-c", "--config", help="path to config dir",
                      default=os.path.expanduser("~/Chinese Word Extractor"))
    (opts, args) = parser.parse_args(sys.argv[1:])

    app = wx.PySimpleApp()

    # configuration
    config = config.Config(
       unicode(os.path.abspath(opts.config), sys.getfilesystemencoding()))
    config.appDir = segHelper.runningDir

    prog = wx.ProgressDialog(parent=None, title="Progress", message="Loading Dictionary", style=wx.PD_AUTO_HIDE|wx.PD_SMOOTH)
    segHelper.LoadData(config, updatefunction=prog.Update)
    prog.Destroy()

    segHelper.LoadKnownWords(config)

    #loads main window
    ui.importAll()
    frame = ui.main.MainWindow(None, -1, "Chinese Word Extractor", size=(750,500))
    frame.segHelper = segHelper
    frame.config = config
    frame.notebook.messagePanel.SetValue(frame.segHelper.getMessages())
    frame.Show(True)

    app.MainLoop()


#if __name__ == "__main__":
#    run()
