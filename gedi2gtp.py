import os, sys, glob, argparse, codecs, ntpath
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
from collections import defaultdict
from xml.dom import minidom

childList = defaultdict(list)

def buildChildList(files,gedi_type):
    for f in files:
        fname = ntpath.basename(os.path.splitext(f)[0])
        print fname
        tree = ET.parse(f)
        root = tree.getroot()
        document=root.find('.//{http://lamp.cfar.umd.edu/media/projects/GEDI/}DL_DOCUMENT')
        page=document.find('.//{http://lamp.cfar.umd.edu/media/projects/GEDI/}DL_PAGE')
        for child in page:
            if child.attrib['gedi_type']==gedi_type:
                childList[fname].append(child)

def createGtp(attribName,outfolder):
    fullText = "";
    for f in childList:
        text = ""
        for c in childList[f]:
            if attribName in c.attrib:
                x1 = c.attrib['col']
                y1 = c.attrib['row']
                x2 = str(int(x1) + int(c.attrib['width']))
                y2 = str(int(y1) + int(c.attrib['height']))
                content = c.attrib[attribName]
                current = x1 + " " + y1 + " " + x2 + " " + y2 + " " + content + "\n"
                text += current
                fullText += f + " " + current
        fname = outfolder + "/" + f + ".gtp"
        file = codecs.open(fname,"w","utf-8")
        file.write(text);
    fname = outfolder+"/full.gtp"
    file = codecs.open(fname,"w", "utf-8")
    file.write(fullText)

def main(xmlFolder, geditype, attribName, outfolder):
        files = glob.glob(xmlFolder+"/*.xml")
        buildChildList(files,geditype)
        createGtp(attribName, outfolder)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert GEDI XML file folder to a single XML in READ format.')
    parser.add_argument('--xmlFolder', '-f', type=str, required=True,
                                   help='Path to the folder containing the gedi xmls')
    parser.add_argument('--geditype', '-g', type=str, required=True,
                                   help='Value of attribute gedi_type to select')
    parser.add_argument('--attribName', '-a', action='store', type=str, required=True,
                                   help='Name of the attribute containing the tag value')
    parser.add_argument('--outfolder', '-o' ,action='store', type=str, required=True,
                                   help='Path to the output XML folder in READ format')
    args = vars(parser.parse_args())
    main(**args)
