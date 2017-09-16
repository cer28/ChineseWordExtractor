'''
Copyright 2011 by Chad Redman <chad at zhtoolkit.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
'''

import wx
import os

class PrefsDialog ( wx.Dialog ):
    
    def __init__( self, parent, segHelper ):
        self.segHelper = segHelper
        self.currentCharset = segHelper.config['charset']
        self._init_ctrls(parent)

    def _init_ctrls(self, prnt):
        
        config = self.segHelper.config

        #wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Preferences", pos = wx.DefaultPosition, size = wx.Size( 709,419 ), style = wx.DEFAULT_DIALOG_STYLE )
        wx.Dialog.__init__(self, id=wx.ID_ANY, name='', parent=prnt,
              pos=wx.Point(457, 156), size=wx.Size(707, 418),
              style=wx.DEFAULT_DIALOG_STYLE, title=u'Preferences')
        self.SetClientSize(wx.Size(699, 391))


        self.m_staticText1 = wx.StaticText(parent=self, id=wx.ID_ANY, label=u'Dictionaries',
              pos=wx.Point(8, 8),
              size=wx.DefaultSize, style=0) #size=wx.Size(56, 14), style=0)
        
        self.m_staticText3 = wx.StaticText(parent=self, id=wx.ID_ANY, label=u'Filtered Words',
              pos=wx.Point(256, 8),
              size=wx.DefaultSize, style=0)  #size=wx.Size(71, 14), style=0)


        # dictionary ListBox
        dictList = self.GetFileItems( os.path.join(config.appDir, 'dict') )

        self.dictListBox = wx.ListBox(parent=self, id=wx.ID_ANY, choices=dictList, 
              pos=wx.Point(8, 32), size=wx.Size(200, 88),
              style=wx.LB_EXTENDED|wx.LB_HSCROLL)

        # pre-select current options
        for idx, val in enumerate(dictList):
            #for dictName in self.config["dictionaries"]:
            #    if dictName == val:
            #        self.dictListBox.SetSelection(idx, True)
            if val in config["dictionaries"]:
                self.dictListBox.SetSelection(idx)


        # Filtered Words file ListBox
        filterList = self.GetFileItems( os.path.join(config.appDir, 'filter') )

        self.filterListBox = wx.ListBox(parent=self, id=wx.ID_ANY, choices=filterList,
              pos=wx.Point(256, 32), size=wx.Size(200, 88),
              style=wx.LB_MULTIPLE | wx.LB_HSCROLL)

        # pre-select current options
        for idx, val in enumerate(filterList):
            if val in config["filters"]:
                self.filterListBox.SetSelection(idx)
        

        self.extraColLabel = wx.StaticText(parent=self, id=wx.ID_ANY, label=u'Extra Column(s)',
              pos=wx.Point(8, 152),
              size=wx.DefaultSize, style=0)  #size=wx.Size(78, 14), style=0)

        #todo DRY - this is only needed so the selected option can be set. Can it be moved to GetFileItems?
        extraColList = self.GetFileItems( os.path.join(config.appDir, 'data', self.currentCharset) )
        self.extraColListBox = wx.ListBox(parent=self, id=wx.ID_ANY, choices=[],
              pos=wx.Point(8, 176),
              size=wx.Size(200, 88), style=wx.LB_MULTIPLE | wx.LB_HSCROLL)

        self._RefreshExtraColumnListBox(self.currentCharset)

        # pre-select current options
        for idx, val in enumerate(extraColList):
            if val in config["extracolumns"]:
                self.extraColListBox.SetSelection(idx)


        self.segMethodLabel = wx.StaticText(parent=self, id=wx.ID_ANY, label=u'Segmentation Method',
              pos=wx.Point(256, 152),
              size=wx.DefaultSize, style=0)  #size=wx.Size(106, 14), style=0)

        segMethods = self.segHelper.GetSegmentMethodNames()
        self.segMethodListBox = wx.ListBox(parent=self, id=wx.ID_ANY, choices=segMethods,
              pos=wx.Point(256, 176), size=wx.Size(200, 104), style=wx.LB_HSCROLL)

        # pre-select current options
        for idx, val in enumerate(segMethods):
            if val in config["segmentmethod"]:
                self.segMethodListBox.SetSelection(idx)


        self.charsetRadioBox = wx.RadioBox(parent=self, id=wx.ID_ANY, label=u'Character Set',
              choices=['simplified', 'traditional'],
              majorDimension=1, name='radioBox1', pos=wx.Point(8, 304),
              size=wx.Size(192, 44), style=wx.RA_SPECIFY_ROWS)

        self.Bind(wx.EVT_RADIOBOX, self.OnCharsetChanged, self.charsetRadioBox)

        # TODO be paranoid and verify the config value is an actual radio option
        self.charsetRadioBox.SetStringSelection(config['charset'])

        
        okButton = wx.Button(parent=self, id=wx.ID_ANY, label=u'Ok',
              pos=wx.Point(168, 360),
              size=wx.Size(75, 23), style=0)
        self.Bind(wx.EVT_BUTTON, self.OnOk, okButton)

        cancelButton = wx.Button(parent=self, id=wx.ID_ANY, label=u'Cancel',
              pos=wx.Point(256, 360), size=wx.Size(75, 23), style=0)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, cancelButton)
        

    def OnCharsetChanged(self, event):
        newcharset = self.charsetRadioBox.GetStringSelection()
        if self.currentCharset != newcharset:
            self.currentCharset = newcharset
            self._RefreshExtraColumnListBox(newcharset)

    def _RefreshExtraColumnListBox(self, charset):
        extraColList = self.GetFileItems(os.path.join(self.segHelper.config.appDir, 'data', charset))
        self.extraColListBox.SetItems(extraColList)

    def OnCancel(self, event):
        self.Destroy()
        event.Skip()

    def OnOk(self, event):
        
        config = self.segHelper.config
        
        # Check for dictionary changes and set reload if necessary
        dictSelected = []
        dictItems = self.dictListBox.GetItems()
        dictIdxSelected = self.dictListBox.GetSelections() 
        for idx in dictIdxSelected:
            dictSelected.append(dictItems[idx])
        
        if config["dictionaries"] != dictSelected:
            #need to reload dictionaries. This should be in an subscribed event
            #todo dirtyDicts to move to segHelper. No need to save it in config
            config.dirtyDicts = True
            config.setDicts(dictSelected)

        # Check for filter file changes and set reload if necessary
        filterSelected = []
        filterItems = self.filterListBox.GetItems()
        filterIdxSelected = self.filterListBox.GetSelections() 
        for idx in filterIdxSelected:
            filterSelected.append(filterItems[idx])

        if config["filters"] != filterSelected:
            #need to reload dictionaries. This should be in an subscribed event
            config.dirtyFilters = True
            config.setFilters(filterSelected)

        # Check for extra column changes and set reload if necessary
        extracolSelected = []
        extracolItems = self.extraColListBox.GetItems()
        extracolIdxSelected = self.extraColListBox.GetSelections() 
        for idx in extracolIdxSelected:
            extracolSelected.append(extracolItems[idx])

        if config["extracolumns"] != extracolSelected:
            #need to reload dictionaries. This should be in an subscribed event
            config.dirtyExtraCols = True
            config.setExtraColumns(extracolSelected)

        newcharset = self.charsetRadioBox.GetStringSelection().encode('iso-8859-1')  # without the encode, converting to unicode yields "decoding Unicode is not supported"
        if config["charset"] != newcharset:
            config["charset"] = newcharset
            config.dirtyDicts = True
            config.dirtyExtraCols = True   # The data needs to be reloaded from the new files, even if the filenames have not changed
            config.setExtraColumns(extracolSelected)

        newSegMethodIdx = self.segMethodListBox.GetSelection()
        newSegMethod = self.segMethodListBox.GetItems()[ newSegMethodIdx ]
        if newSegMethod != config['segmentmethod']:
            self.segHelper.SetSegmentMethodByName(newSegMethod)

        (saveStatus, ex) = config.save()
        if not saveStatus:
            #print "Error in prefsDialog.OnOk calling config.save: %s" % ex
            dlg = wx.MessageDialog(self, 'Unable to save configuration file. Error was (%s)' % ex, 'Error', wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            


        self.Destroy()
        

    def GetFileItems(self, directory):
        import stat

        choices = []
        filenames = []
        try:
            filenames = os.listdir(directory)
        except Exception, e:
            print "Error in GetFileItems: %s" % e
            dlg = wx.MessageDialog(self, 'Unable to read files in directory %s (%s)' % (directory, e), 'Error', wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return choices
        
        for filename in filenames:
            if filename[0] != "_":
                try:
                    st = os.stat(os.path.join(directory, filename))
                except os.error:
                    continue
                if stat.S_ISREG(st.st_mode):
                    choices.append(filename)
        return choices

