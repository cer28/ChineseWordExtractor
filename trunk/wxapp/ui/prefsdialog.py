'''
Copyright 2011 by Chad Redman <chad at zhtoolkit.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
'''

import wx
import os

class PrefsDialog(wx.Dialog):
    def __init__(self, parent, config):
        
        self.config = config

        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Preferences", size=(250,210))

        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL) 

        label = wx.StaticText(self, -1, "Select dictionary:")
        vbox.Add(label, 0, wx.ALIGN_LEFT|wx.ALL)
        self.dictList = self.GetFileItems( os.path.join(self.config.appDir, 'dict') )
        self.dictListBox = wx.ListBox(self, 60, (100, 50), (200, 120), self.dictList, wx.LB_EXTENDED|wx.LB_HSCROLL)

        # pre-select current options
        for idx, val in enumerate(self.dictList):
            #for dictName in self.config["dictionaries"]:
            #    if dictName == val:
            #        self.dictListBox.SetSelection(idx, True)
            if val in self.config["dictionaries"]:
                self.dictListBox.SetSelection(idx, True)

        vbox.Add(self.dictListBox, 0, wx.ALIGN_LEFT|wx.ALL)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, -1, 'Ok')
        self.Bind(wx.EVT_BUTTON, self.OnOk, okButton)
        hbox.Add(okButton, 1)

        cancelButton = wx.Button(self, -1, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.OnCancel, cancelButton)
        hbox.Add(cancelButton, 1, wx.LEFT, 5)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(vbox)

    def OnCancel(self, event):
        self.Destroy()
        event.Skip()

    def OnOk(self, event):
        dictIdxSelected = self.dictListBox.GetSelections() 
        dictSelected = []
        for idx in dictIdxSelected:
            dictSelected.append(self.dictList[idx])

        if self.config["dictionaries"] != dictSelected:
            #need to reload dictionaries. This should be in an subscribed event
            self.config.dirtyDicts = True
            self.config.setDicts(dictSelected)
            
            #%% Temp for debugging
            import string
            d = wx.MessageDialog(self, "(debug) will reload dictionaries: %s" % string.join(dictSelected, ", "), "", wx.OK)
            d.ShowModal()
            d.Destroy()


        self.config.save()

        self.Destroy()
        

    def GetFileItems(self, directory):
        import stat

        choices = []
        for filename in os.listdir(directory):
            try:
                st = os.stat(os.path.join(directory, filename))
            except os.error:
                continue
            if stat.S_ISREG(st.st_mode):
                choices.append(filename)
        return choices
    