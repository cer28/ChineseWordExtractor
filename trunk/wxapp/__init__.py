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

    # Notes on icon bundles:
    # 1) can't be 256x256 because too big to import within the application
    # 2) the 16x16 object will be the shown in taskbar , Explorer list view, application context menu, etc.
    #     - It will choose the 16-color icon if it exists. I don't know why anyone would want this
    #     - the 256 color works fine. I haven't tried other sizes.

    # pre-load icons; they need to be set for the load dictionary progress, since it happens before the main frame shows
    ib = wx.IconBundle()
    ib.AddIconFromFile("application-icon.ico", wx.BITMAP_TYPE_ANY)

    # configuration
    config = config.Config(
       unicode(os.path.abspath(opts.config), sys.getfilesystemencoding()))
    config.appDir = segHelper.runningDir

    prog = wx.ProgressDialog(parent=None, title="Progress", message="Loading Dictionary", style=wx.PD_AUTO_HIDE|wx.PD_SMOOTH)
    prog.SetIcons(ib)
    segHelper.config = config
    segHelper.LoadData(updatefunction=prog.Update)
    prog.Destroy()

    segHelper.LoadKnownWords()
    segHelper.LoadExtraColumns()

    #loads main window
    ui.importAll()
    frame = ui.main.MainWindow(None, -1, "Chinese Word Extractor", size=(750,500))

    frame.SetIcons(ib)
    
    frame.segHelper = segHelper
    frame.config = config
    frame.notebook.messagePanel.SetValue(frame.segHelper.getMessages())
    frame.Show(True)

    app.MainLoop()


#if __name__ == "__main__":
#    run()
