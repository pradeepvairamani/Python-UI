from Foundation import NSUserNotification, NSUserNotificationCenter, NSObject
from AppKit import NSImage, NSStatusBar, NSMenu, NSMenuItem, NSApplication, NSVariableStatusItemLength
from PyObjCTools import AppHelper


class MyApp(NSApplication):

    def finishLaunching(self):
        # Make statusbar item
        statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        self.icon = NSImage.alloc().initByReferencingFile_('icon.png')
        self.icon.setScalesWhenResized_(True)
        self.icon.setSize_((20, 20))
        self.statusitem.setImage_(self.icon)

        # make the menu
        self.menubarMenu = NSMenu.alloc().init()

        self.menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Test Notification', 'clicked:', '')
        self.menubarMenu.addItem_(self.menuItem)

        self.quit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
        self.menubarMenu.addItem_(self.quit)

        # add menu to statusitem
        self.statusitem.setMenu_(self.menubarMenu)
        self.statusitem.setToolTip_('My App')
        self._notify_obj = Notification.alloc().init()

    def clicked_(self, notification):
        self._notify_obj.notify('Title', 'subtitle', 'description text', 'http://google.com')


class Notification(NSObject):

    def notify(self, title, subtitle, text, url):
        notification = NSUserNotification.alloc().init()
        notification.setTitle_(str(title))
        notification.setSubtitle_(str(subtitle))
        notification.setInformativeText_(str(text))
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
        notification.setUserInfo_({"action": "open_url", "value": url})
        NSUserNotificationCenter.defaultUserNotificationCenter().setDelegate_(self)
        NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)

    def userNotificationCenter_didActivateNotification_(self, center, notification):
        #callback
        userInfo = notification.userInfo()
        print 'came here'
        print userInfo

if __name__ == "__main__":
    app = MyApp.sharedApplication()
    AppHelper.runEventLoop()
