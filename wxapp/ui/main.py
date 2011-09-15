'''
Copyright 2011 by Chad Redman <chad at zhtoolkit.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
'''

import wx
import wx.html
from wx.lib.wordwrap import wordwrap
import os

import version

# non-standard menus
ID_REFRESH_RESULTS = 101



#    Method OnInit()    
#        ConnectAny(wxEVT_KEY_DOWN, OnKeyDown)


class MyAboutBox(wx.Dialog):
    text = '''
<html>
<body>
<h1>Chinese Word Extractor</h1>
<p>Version %s</p>

<p>Chinese Word Extractor is licensed under the terms of the
<a href="http://www.gnu.org/copyleft/gpl.html">GPL v.3.0</a><br/>

<p>(c) Copyright 2011 Chad Redman. All rights reserved.</p>

<p>Go to the <a href="http://www.zhtoolkit.com/posts/tools/chinese-word-extractor/">project page</a></p>

<p><wxp module="wx" class="Button">
    <param name="label" value="Okay">
    <param name="id"    value="ID_OK">
</wxp></p>

</body>
</html>
'''

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'About Chinese Word Extractor',)
        html = wx.html.HtmlWindow(self, -1, size=(420, -1))
        if "gtk2" in wx.PlatformInfo:
            html.SetStandardFonts()
        txt = self.text % (version.APP_VERSION)
        html.SetPage(txt)
        btn = html.FindWindowById(wx.ID_OK)
        ir = html.GetInternalRepresentation()
        html.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wx.BOTH)


class EditorPanel1(wx.TextCtrl):
    def __init__(self, parent, *args, **kwargs):
        wx.TextCtrl.__init__(self, parent, *args, **kwargs)
        
class ResultPanel1(wx.TextCtrl):
    def __init__(self, parent, *args, **kwargs):
        wx.TextCtrl.__init__(self, parent, *args, **kwargs)


class SummaryPanel1(wx.TextCtrl):
    def __init__(self, parent, *args, **kwargs):
        wx.TextCtrl.__init__(self, parent, *args, **kwargs)

class MessagePanel1(wx.TextCtrl):
    def __init__(self, parent, *args, **kwargs):
        wx.TextCtrl.__init__(self, parent, *args, **kwargs)



    
class NoteBook1(wx.Notebook):
    def __init__(self, parent, id, *args, **kwargs):
        #wx.Notebook.__init__(self, parent, *args, **kwargs)

        wx.Notebook.__init__(self, parent, id, size=(21,21), style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )

        self.editorPanel = EditorPanel1(self, 1, style=wx.TE_MULTILINE)
        self.AddPage(self.editorPanel, 'Source')

        self.summaryPanel = SummaryPanel1(self, 1, style=wx.TE_MULTILINE |wx.TE_READONLY | wx.TE_DONTWRAP )
        self.AddPage(self.summaryPanel, 'Summary', )

        self.resultPanel = ResultPanel1(self, 1, style=wx.TE_MULTILINE |wx.TE_READONLY | wx.TE_DONTWRAP )
        self.AddPage(self.resultPanel, 'Analysis', )

        self.messagePanel = ResultPanel1(self, 1, style=wx.TE_MULTILINE |wx.TE_READONLY | wx.TE_DONTWRAP )
        self.AddPage(self.messagePanel, 'Messages', )

        #TODO subclass textctl and program in ctrl-A
        wx.EVT_SET_FOCUS(self.resultPanel, self.OnTextSetFocus)

    def OnTextSetFocus(self, evt):
        wx.CallAfter(self.SelectAll)

    def SelectAll(self):
        self.resultPanel.SetSelection(-1, -1)

class MainWindow(wx.Frame):

    config = None
    segHelper = None

    def OnRefreshResults(self, e):
        self.segHelper.setText(self.notebook.editorPanel.GetValue())

        prog = wx.ProgressDialog(parent=self, title="Progress", message="parsing Results", style=wx.PD_AUTO_HIDE|wx.PD_SMOOTH)
        self.segHelper.SummarizeResults(updatefunction=prog.Update)
        prog.Destroy()

        #st = wx.StaticText(self.notebook.resultPanel, -1, self.segHelper.summary, (10, 10))
        self.notebook.summaryPanel.SetValue(self.segHelper.summary)
        self.notebook.resultPanel.SetValue(self.segHelper.results)
        self.notebook.messagePanel.SetValue(self.segHelper.getMessages())


    def OnAbout(self, e):
        # First we create and fill the info object
        info = wx.AboutDialogInfo()
        info.Name = "Chinese Word Extractor"
        info.Version = version.APP_VERSION
        info.Copyright = "(C) 2011 Chad Redman"
        info.Description = wordwrap(
            "This is a tool to extract vocabulary from Chinese text, summarizing "
            "the unique words with word count, pinyin, English definition, and other useful "
            "statistics.",
            500, wx.ClientDC(self))
        info.WebSite = ("http://www.zhtoolkit.com/posts/tools/chinese-word-extractor/", "Project home page")
        #info.Developers = [ "Joe Programmer",
        #                    "Jane Coder",
        #                    "Vippy the Mascot" ]
        info.License = wordwrap(
            "This program is licensed under the terms of the "
            "GPL v.3.0; see http://www.gnu.org/licenses/gpl-3.0.html for details.",
            500, wx.ClientDC(self))

        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)
    def OnOpen(self, e):
        """ Open a file """

        self.dirname = self.config['currentdir']
        #dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "Text Files (*.txt)|*.txt|UTF-8 text files (*.txt, *.u8)|*.u8;*.txt|All files (*)|*.*", style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
        dlg = wx.FileDialog(self, "Choose one or more files", self.dirname, "", "text files (*.txt, *.u8, *.gb)|*.txt;*.u8;*.gb|All files (*)|*.*", style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            #self.filename = dlg.GetFilename()
            #self.dirname = dlg.GetDirectory()
            #f = open(os.path.join(self.dirname, self.filename), 'r')
            #self.notebook.editorPanel.SetValue(f.read())
            #f.close()
            
            self.notebook.editorPanel.SetValue(self.segHelper.ReadFiles(dlg.GetPaths()))
            
            self.notebook.messagePanel.SetValue(self.segHelper.getMessages())

            self.config['currentdir'] = dlg.GetDirectory()
            self.config.save()

        dlg.Destroy()

    def OnExit(self, e):
        self.config.save()
        self.Close(True)
        
    def OnPreferences(self, e):
        import prefsdialog
        d = prefsdialog.PrefsDialog(self, self.config)
        d.ShowModal()
        d.Destroy()
        if self.config.dirtyDicts:
            prog = wx.ProgressDialog(parent=None, title="Progress", message="Loading Dictionary", style=wx.PD_AUTO_HIDE|wx.PD_SMOOTH)
            self.segHelper.LoadData(self.config, updatefunction=prog.Update)
            prog.Destroy()

            #self.segHelper.LoadData(self.config, updatefunction=wx.ProgressDialog(title="Progress", message="Loading Dictionary", style=wx.PD_AUTO_HIDE|wx.PD_SMOOTH).Update)
            self.config.dirtyDicts = False

        self.notebook.messagePanel.SetValue(self.segHelper.getMessages())


    def __init__(self, parent, *args, **kwargs):
        wx.Frame.__init__(self, parent, *args, **kwargs)

        mainmenu = wx.MenuBar()                  # Create menu bar.
        menu = wx.Menu()

        item = menu.Append(wx.ID_ABOUT, '&About', 'Information about this program')
        self.Bind(wx.EVT_MENU, self.OnAbout, item)  # Create and assign a menu event.
        item = menu.Append(wx.ID_OPEN, '&Open', 'Open a file')
        self.Bind(wx.EVT_MENU, self.OnOpen, item)  # Create and assign a menu event.
        item = menu.Append(ID_REFRESH_RESULTS, '&Analyze', 'Analyze Results')
        self.Bind(wx.EVT_MENU, self.OnRefreshResults, item)  # Create and assign a menu event.
        item = menu.Append(wx.ID_PREFERENCES, 'P&references', 'Configure application settings')
        self.Bind(wx.EVT_MENU, self.OnPreferences, item)  # Create and assign a menu event.
        item = menu.Append(wx.ID_EXIT, 'E&xit', 'Terminate the program')
        self.Bind(wx.EVT_MENU, self.OnExit, item)  # Create and assign a menu event.

        mainmenu.Append(menu, '&File')
        self.SetMenuBar(mainmenu)

        self.notebook = NoteBook1(self, 1)        
