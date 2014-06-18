import os
import subprocess
import shutil

# Dependencies:
# BeautifulSoup4: sudo pip install BeautifulSoup4

from bs4 import BeautifulSoup as Soup

#todo: all the path stuff here is linux / osx friendly.  deal with windows....

def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1:
                shutil.copy2(s, d)


def prepender(filename, content):
    with open(filename,'r+') as f:
        prevContent = f.read()
        f.seek(0,0)
        for line in content: 
        	f.write(line)
        for line in prevContent:
        	f.write(line)
        f.close();

def appender(filename, content):
	with open('log.txt','a') as f:
		for line in content:
			f.write(line)
		f.close();


chapters = open("../chapters/order.txt").read().splitlines()

for chapter in chapters:
	path = "../output/chapters/" + chapter;
	print path
	if not os.path.exists(path):
		os.makedirs(path)
	source = "../chapters/" + chapter + "/chapter.md";
	dest = path + "/index.html"

	subprocess.call(["pandoc", "-o", dest, source, "-s", "--toc", "--toc-depth=4", "-p",
					"--mathjax",	
					"--include-in-header=createWebBookTemplate/IncludeInHeader.html",
					"--include-before-body=createWebBookTemplate/IncludeBeforeBody.html",
					"--include-after-body=createWebBookTemplate/IncludeAfterBody.html"])

	imagesSource = source = "../chapters/" + chapter + "/images";
	imagesDest = path + "/images"
	if os.path.exists(imagesSource):
		copytree(imagesSource, imagesDest)
	
	#now, let's parse the index.html and change some things: 

	if os.path.exists(dest):
		soup = Soup(open(dest).read())
		h1s = soup.find_all("h2")
		pCaption = soup.find_all("p", class_="caption")
		for tag in pCaption:
			tag.name = "span"
		html = soup.encode("utf-8")
		with open(dest, "wb") as file:
			file.write(html)
	#print(soup.prettify())

	#h1s will be super helpful for sidebar and building up a map of content :)
	
