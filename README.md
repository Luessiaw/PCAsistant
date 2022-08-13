# PCAsistant
类似于浏览器插件，只不过放在托盘区。需要新功能的话，写插件就可以了。

这个项目源于Wallpaperchange. 在wpc里使用托盘程序来完成一系列操作。
将其改写成插件的形式，PCAsistant只提供托盘程序，具体的任务交给各个插件程序。

最初的版本为了简便主要使用pystray和easygui. 有点丑，后面会改为pyQt.
