#/usr/bin/python3

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GdkPixbuf as pb
import os
from io import StringIO
import util
#from util import *

class Iv(gtk.Window):
    cwd = os.getcwd()
    dir = cwd + "/"
    len = 0
    visible = True
    def __init__(self):
        gtk.Window.__init__(self, title="Iv")
        self.set_border_width(1)
        
        self.grid=gtk.Grid()
        #        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.grid.set_column_homogeneous(True)
        self.image  = gtk.Image.new_from_file("/ss/dl/copter.jpg")
        self.pixbuf = self.image.get_pixbuf()
        
        #self.image.set_from_file("/ss/dl/copter.jpg")
        self.image.show()
        self.imgbox = gtk.Box()
        self.imgbox.add(self.image)

        self.currentfiles = gtk.ListStore(str)
        self.filltree(self.dir)
        #self.len = len(os.listdir(self.dir))
        #for p in os.listdir(self.dir):
        #    self.currentfiles.append([p])
            
        self.tree = gtk.TreeView(self.currentfiles)
        self.tree.set_enable_search(False)
        
        renderer = gtk.CellRendererText(weight=100)
        renderer.set_fixed_size(200, -1)
        column = gtk.TreeViewColumn("files", renderer, text=0)
        column.set_max_width(200)
        column.set_min_width(50)
        self.tree.append_column(column)

        self.tree.connect("row-activated", self.openfile)
        self.filebox = gtk.ScrolledWindow()
        self.filebox.set_vexpand(True)
        #self.filebox.set_min_width(300)
        self.grid.attach(self.filebox, 0, 0, 1, 1)
        self.grid.attach_next_to(self.imgbox, self.filebox, gtk.PositionType.RIGHT, 10, 1)
        self.filebox.add(self.tree)
        

        self.add(self.grid)
        self.grid.connect("key_press_event", self.keypress)
        self.show_all()

        
        
        
    def filltree(self,path):
        self.currentfiles.clear()
        lst = os.listdir(self.dir)
        files = util.listfiles(path)
        dirs = util.listdirs(path)
        counter = 0
        for p in dirs:
            self.currentfiles.append([p + "/"])
            counter += 1
        for p in files:
            self.currentfiles.append([p])
            counter += 1
        self.len = len(lst)
#        for p in lst:
#            item = p
#            if(os.path.isdir(self.dir + item)):
#               self.currentfiles.append([item + "/"])
#            else:
#               self.currentfiles.append([item])
        #self.tree.clear()

    def inccursor(s, val):
        path, colr = s.tree.get_cursor()
        if(path is None):
            s.tree.set_cursor((0),)
        else:
            pos = path[0]
            posnew = pos + val
            if (posnew < s.len and posnew >= 0):
                s.tree.set_cursor((posnew),)
            elif (posnew < 0):
                s.tree.set_cursor((s.len + posnew),)
            else:
                s.tree.set_cursor((0 + posnew - s.len),)
            
    def visible(s):
        s.filebox.set_visible(False)
            
    def visb(s):
        s.filebox.set_visible(True)
      
    def nextitem(s):
        s.inccursor(1)
        p,c = s.tree.get_cursor()
        s.openimg(s.tree,p,c)
        
    def previtem(s):
        s.inccursor(-1)
        p,c = s.tree.get_cursor()
        s.openimg(s.tree,p,c)
        
    def dirup(s):
        s.dir = os.path.dirname(os.path.dirname(s.dir))
        s.dir += "/"
        s.filltree(s.dir)
    def openitem(s):
        p,c = s.tree.get_cursor()
        s.openfile(s.tree,p,c)

    def imgfit(s):
        rec = s.imgbox.get_allocation()
        w = rec.width
        h = rec.height
        s.pixbuf = pb.Pixbuf.scale_simple(s.pixbuf,w,h,pb.InterpType(2))
        #s.pixbuf.scale_simple(w, h, pb.InterpType(2))
        s.image.set_from_pixbuf(s.pixbuf)
        
    def keyerror(e) : print("key fn not defined")
    def keypress(self, w, event):

        #self.keys.get(gdk.keyval_name(event.keyval), self.keyerror)()
        k = gdk.keyval_name(event.keyval)

        keys = {
	#            'q' : self.visible,
            'e' : self.imgfit,
            'a' : self.dirup,
            'd' : self.openitem,
            'w' : self.previtem,
            's' : self.nextitem}
        keys.get(k,self.keyerror)()
    def openfile(self, tree, path, column):
        model = tree.get_model()
        iter = model.get_iter(path)
        file = self.dir + model.get_value(iter,0)

        if(os.path.isdir(file)):
           self.dir = file
           self.filltree(self.dir)
        else:
            self.image.set_from_file(file)
            self.pixbuf = self.image.get_pixbuf()

        
           
        print(file)
        
    def openimg(self,tree,path,col):
        model = tree.get_model()
        iter = model.get_iter(path)
        file = self.dir + model.get_value(iter,0)
        if not (os.path.isdir(file)):
            self.image.set_from_file(file)
            self.pixbuf = self.image.get_pixbuf()
            
    
        

    




       
        
win = Iv()

#pixbuf = gtk.gdk.pixbuf_new_from_file("/ss/dl/exlosion.jpg")
#image.set_from_pixmap(pixmap, mask)

# a button to contain the image widget
#button = gtk.Button()
#button.add(image)
#win.add(imgbox)
#button.show()
#imgbox.show()

#image = gtk.Image()
#   self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
#self.window.fullscreen()
#self.window.show()
#image.show()




win.connect("delete-event", gtk.main_quit)
win.show()
gtk.main()
