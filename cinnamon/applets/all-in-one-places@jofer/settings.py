#!/usr/bin/python

'''
Settings Application for the All-in-one Places applet for Cinnamon
http://jferrao.github.com/gtk

Requires Python 2.7


@author jferrao <jferrao@ymail.com>
@version 1.0

'''





from optparse import OptionParser
from gi.repository import Gtk
import os
import json
import collections

from gettext import gettext as _



default_config = {
    'SHOW_PANEL_ICON': True, 
    'USE_FULL_COLOR_ICON': False, 
    'SHOW_PANEL_TEXT': False, 
    'PANEL_TEXT': None, 
    'SHOW_DESKTOP': True, 
    'AUTO_HIDE_TRASH': False, 
    'SHOW_BOOKMARKS': True, 
    'COLLAPSE_BOOKMARKS': False, 
    'SHOW_FILE_SYSTEM': False, 
    'SHOW_DEVICES': True, 
    'COLLAPSE_DEVICES': False, 
    'SHOW_NETWORK': True, 
    'COLLAPSE_NETWORK': False, 
    'SHOW_SEARCH': True, 
    'SHOW_RECENT_DOCUMENTS': True, 
    'ICON_SIZE': 22, 
    'RECENT_ITEMS': 10
}

config = None
config_file = os.path.dirname(os.path.abspath(__file__)) + "/config.json"



def load_config():
    global config
    f = open(config_file, 'r')
    config = json.loads(f.read(), object_pairs_hook=collections.OrderedDict)
    f.close()
    if (opts.verbose):
        print "config file loaded"

def save_config(data):
    f = open(config_file, 'w')
    f.write(json.dumps(data, sort_keys=False, indent=4))
    f.close()
    if (opts.verbose):
        print "config file saved"





class MyWindow(Gtk.Window):

    restart = False

    def __init__(self):
        
        Gtk.Window.__init__(self, title="All-in-one Places Applet Settings")

        window_icon = self.render_icon(Gtk.STOCK_PREFERENCES, 6)
        self.set_icon(window_icon)

        self.set_position(3)
        self.set_border_width(15)
        
        box_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)
        box_container.set_homogeneous(False)

        # Left options column
        vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_left.set_homogeneous(False)

        # Righ options column
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_right.set_homogeneous(False)

        # Columns options container box
        box_options = Gtk.HBox(spacing=15)
        box_options.set_homogeneous(False)
        box_options.pack_start(vbox_left, False, False, 0)
        box_options.pack_start(Gtk.VSeparator(), False, False, 0)
        box_options.pack_start(vbox_right, False, False, 0)

        # Bottom options box
        #box_extra = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        #box_extra.set_homogeneous(False)

        # Buttons box
        box_buttons = Gtk.HBox(spacing=10)
        box_buttons.set_homogeneous(False)
        
        box_container.pack_start(box_options, True, True, 0)
        #box_container.pack_start(box_extra, True, True, 0)
        box_container.pack_start(box_buttons, True, True, 0)


        # Build options for left column
        if (config.has_key('SHOW_PANEL_ICON')):
            switch_show_icon = switch_option()
            switch_show_icon.create(vbox_left, 'SHOW_PANEL_ICON', config['SHOW_PANEL_ICON'], "Show panel icon")

        if (config.has_key('USE_FULL_COLOR_ICON')):
            switch_color_icon = switch_option()
            switch_color_icon.create(vbox_left, 'USE_FULL_COLOR_ICON', config['USE_FULL_COLOR_ICON'], "Use full color icon")

        if (config.has_key('SHOW_PANEL_TEXT')):
            switch_show_text = switch_option()
            switch_show_text.create(vbox_left, 'SHOW_PANEL_TEXT', config['SHOW_PANEL_TEXT'], "Show panel text")

        if (config.has_key('PANEL_TEXT')):
            use_custom_panel_text = False if (config['PANEL_TEXT'] == None) else True
            # Custom text option
            check_custom_text = Gtk.CheckButton("Use custom panel text")
            check_custom_text.set_active(use_custom_panel_text)
            vbox_left.pack_start(check_custom_text, False, False, 0)        
            
            # Custom text entry
            entry_panel_text = Gtk.Entry()
            if (use_custom_panel_text):
                if (config['PANEL_TEXT'] != None):
                    entry_panel_text.set_text(config['PANEL_TEXT'])
            else:
                entry_panel_text.set_sensitive(False)
            vbox_left.pack_start(entry_panel_text, False, False, 0) 
            
            # Connect events
            check_custom_text.connect('toggled', self.on_check_custom_text_change, entry_panel_text)
            entry_panel_text.connect('changed', self.on_custom_text_change)
            
        vbox_left.pack_start(Gtk.HSeparator(), False, False, 0)

        if (config.has_key('SHOW_DESKTOP')):
            switch_show_desktop = switch_option()
            switch_show_desktop.create(vbox_left, 'SHOW_DESKTOP', config['SHOW_DESKTOP'], "Show desktop")

        if (config.has_key('AUTO_HIDE_TRASH')):
            switch_hide_trash = switch_option()
            switch_hide_trash.create(vbox_left, 'AUTO_HIDE_TRASH', config['AUTO_HIDE_TRASH'], "Auto hide trash")

        if (config.has_key('SHOW_FILE_SYSTEM')):
            switch_show_filesystem = switch_option()
            switch_show_filesystem.create(vbox_left, 'SHOW_FILE_SYSTEM', config['SHOW_FILE_SYSTEM'], "Show file system")

        # Build options for right column
        if (config.has_key('SHOW_BOOKMARKS')):
            switch_show_bookmarks = switch_option()
            switch_show_bookmarks.create(vbox_right, 'SHOW_BOOKMARKS', config['SHOW_BOOKMARKS'], "Show bookmarks section")

        if (config.has_key('COLLAPSE_BOOKMARKS')):
            switch_drop_bookmarks = switch_option()
            switch_drop_bookmarks.create(vbox_right, 'COLLAPSE_BOOKMARKS', config['COLLAPSE_BOOKMARKS'], "Drop-down bookmarks")

        if (config.has_key('SHOW_DEVICES')):
            switch_show_devices = switch_option()
            switch_show_devices.create(vbox_right, 'SHOW_DEVICES', config['SHOW_DEVICES'], "Show devices section")

        if (config.has_key('COLLAPSE_DEVICES')):
            switch_drop_devices = switch_option()
            switch_drop_devices.create(vbox_right, 'COLLAPSE_DEVICES', config['COLLAPSE_DEVICES'], "Drop-down devices")

        if (config.has_key('SHOW_NETWORK')):
            switch_show_network = switch_option()
            switch_show_network.create(vbox_right, 'SHOW_NETWORK', config['SHOW_NETWORK'], "Show network section")

        if (config.has_key('COLLAPSE_NETWORK')):
            switch_drop_network = switch_option()
            switch_drop_network.create(vbox_right, 'COLLAPSE_NETWORK', config['COLLAPSE_NETWORK'], "Drop-down network")

        if (config.has_key('SHOW_SEARCH')):
            switch_show_search = switch_option()
            switch_show_search.create(vbox_right, 'SHOW_SEARCH', config['SHOW_SEARCH'], "Show search")

        if (config.has_key('SHOW_RECENT_DOCUMENTS')):
            switch_show_documents = switch_option()
            switch_show_documents.create(vbox_right, 'SHOW_RECENT_DOCUMENTS', config['SHOW_RECENT_DOCUMENTS'], "Show recent documents section")
        
        vbox_right.pack_start(Gtk.HSeparator(), False, False, 0)
        
        # Icon size slider
        box_icon_size = Gtk.VBox(0)
       
        adjust_icon_size = Gtk.Adjustment(config['ICON_SIZE'], 16, 46, 6, 6, 0)
        adjust_icon_size.connect("value_changed", self.on_slider_change, 'ICON_SIZE')
        slider_icon_size = Gtk.HScale()
        slider_icon_size.set_adjustment(adjust_icon_size)
        slider_icon_size.set_digits(0)

        box_icon_size.pack_start(Gtk.Label(_("Icon size")), False, False, 0)
        box_icon_size.pack_start(slider_icon_size, False, False, 0)        

        vbox_right.pack_start(box_icon_size, False, False, 0)

        # Number of recent documents slider
        box_documents = Gtk.VBox(0)
        
        adjust_documents = Gtk.Adjustment(config['RECENT_ITEMS'], 5, 25, 1, 5, 0)
        adjust_documents.connect("value_changed", self.on_slider_change, 'RECENT_ITEMS')
        slider_documents = Gtk.HScale()
        slider_documents.set_adjustment(adjust_documents)
        slider_documents.set_digits(0)

        box_documents.pack_start(Gtk.Label(_("Number of recent documents")), False, False, 0)
        box_documents.pack_start(slider_documents, False, False, 0)        

        vbox_right.pack_start(box_documents, False, False, 0)
        
        # Build extra options
        #self.restart = False
        #self.check_restart = Gtk.CheckButton("Restart Cinnamon on close")
        #self.check_restart.connect('toggled', self.change_restart_status)
        #self.check_restart.set_active(False)
        #box_extra.pack_start(self.check_restart, True, True, 0)        

        # Build buttons
        #img_default = Gtk.Image()
        #img_default.set_from_stock(Gtk.STOCK_PROPERTIES, 3)
        #btn_default = Gtk.Button(_("Default settings"))
        #btn_default.set_property("image", img_default)
        #btn_default.connect('clicked', self.generate_config_file)
        #box_buttons.pack_start(btn_default, False, False, 0)
        
        btn_close = Gtk.Button(stock=Gtk.STOCK_CLOSE)
        btn_close.connect('clicked', self.exit_application)
        box_buttons.pack_end(btn_close, False, False, 0)

        img_restart = Gtk.Image()
        img_restart.set_from_stock(Gtk.STOCK_REFRESH, 3)
        btn_restart = Gtk.Button(_("Restart Cinnamon"))
        btn_restart.set_property("image", img_restart)
        btn_restart.connect('clicked', self.restart_shell)
        box_buttons.pack_end(btn_restart, False, False, 0)

        self.add(box_container)



    def change_restart_status(self, widget):
        if widget.get_active():
            self.restart = True
        else:
            self.restart = False

    def on_check_custom_text_change(self, option_widget, text_widget):
        if option_widget.get_active():
            text_widget.set_sensitive(True)
            text_widget.grab_focus()
        else:
            text_widget.set_sensitive(False)
            config['PANEL_TEXT'] = None
            if (opts.verbose):
                print "changed key 'PANEL_TEXT' => %s" % None
            save_config(config)

    def on_custom_text_change(self, text_widget):
        config['PANEL_TEXT'] = text_widget.get_text()
        if (opts.verbose):
            print "changed key 'PANEL_TEXT' => %s" % text_widget.get_text()
        save_config(config)

    def on_slider_change(self, widget, key):
        config[key] = int(widget.get_value())
        if (opts.verbose):
            print "changed key %s => %s" % (key, int(widget.get_value()))
        save_config(config)

    def generate_config_file(self, widget):
        if (opts.verbose):
            print "new default config file generated"
        save_config(default_config)
    
    def restart_shell(self, widget):
        os.system('cinnamon --replace &')
        self.check_restart.set_active(False)

    def exit_application(self, widget):
        if (self.restart):
            os.system('cinnamon --replace &')
            self.check_restart.set_active(False)
        else:
            Gtk.main_quit()





class switch_option():
    
    def create(self, container, key, value, label):
        box = Gtk.HBox(spacing=20)
        box.set_homogeneous(False)
        label = Gtk.Label(label)
        
        widget = Gtk.Switch()
        widget.set_active(value)
        widget.connect('notify::active', self.change_state, key)

        box.pack_start(label, False, False, 0)
        box.pack_end(widget, False, False, 0)        

        container.add(box)        

    def change_state(self, widget, notice, key):
        global config
        if (config.has_key(key)):
            config[key] = widget.get_active();
            if (opts.verbose):
                print "changed key %s => %s" % (key, widget.get_active())
        save_config(config)





if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="print event and action messages")
    (opts, args) = parser.parse_args()
    
    load_config()

    win = MyWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    
