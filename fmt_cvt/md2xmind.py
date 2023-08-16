import os
import re
from XmindCopilot import xmind
from XmindCopilot.xmind.core.topic import TopicElement

class MDTextSnippet(object):
    pass


class MDSection(object):
    """Markdown Section Class
    ---
    Mangage the markdown sections identified by `#`
    """
    
    titleLineMatchStr = r"\s{0,3}(#{1,6})\s{1,}(.*)"
    
    def __init__(self, title: str, text: str):
        """
        :param title: Title
        :param text: Text (Should not contain title)
        """
        self.title = title
        self.text = text
        self.textList = text.split('\n')
        self.nonSubSectionTextList = []
        self.SubSection = []
        self.segment()
    
    def segment(self):
        """Segment the text into sub-sections
        """
        titleLines = []  # Title Line are stored as (Level, index)
        for index in range(len(self.textList)):
            line = self.textList[index]
            titleMatch = re.match(self.titleLineMatchStr, line)
            if titleMatch:
                # (Level, index)
                titleLines.append((len(titleMatch.groups()[0]), index))
        if titleLines:
            self.nonSubSectionTextList = self.textList[:titleLines[0][1]]
        else:
            self.nonSubSectionTextList = self.textList
            return
        maxLevel = min([level for level, _ in titleLines])
        lastMaxLevelLine = None
        for titleLine in titleLines:
            if titleLine[0] == maxLevel:
                if lastMaxLevelLine:
                    title = re.match(self.titleLineMatchStr, self.textList[lastMaxLevelLine[1]]).groups()[1]
                    self.SubSection.append(MDSection(title, '\n'.join(self.textList[lastMaxLevelLine[1]+1:titleLine[1]])))
                lastMaxLevelLine = titleLine
            if titleLine == titleLines[-1] and lastMaxLevelLine:
                title = re.match(self.titleLineMatchStr, self.textList[lastMaxLevelLine[1]]).groups()[1]
                self.SubSection.append(MDSection(title, '\n'.join(self.textList[lastMaxLevelLine[1]+1:])))
    
    def printSubSections(self, indent=4):
        print(" "*indent, self.title)
        for subSection in self.SubSection:
            subSection.printSubSections(indent+4)
    
    def toXmind(self, parentTopic: TopicElement):
        """Convert the section to xmind
        """
        topic = parentTopic.addSubTopicbyTitle(self.title)
        for line in self.nonSubSectionTextList:
            topic.addSubTopicbyTitle(line)
        for subSection in self.SubSection:
            subSection.toXmind(topic)
  

class MarkDown2Xmind(object):
    
    _ws_only_line_re = re.compile(r"^[ \t]+$", re.M)
    tab_width = 4
    
    def __init__(self, topic=None):
        self.topic = topic
        self.reset()
    
    def _detab_line(self, line):
        r"""Recusively convert tabs to spaces in a single line.

        Called from _detab()."""
        if '\t' not in line:
            return line
        chunk1, chunk2 = line.split('\t', 1)
        chunk1 += (' ' * (self.tab_width - len(chunk1) % self.tab_width))
        output = chunk1 + chunk2
        return self._detab_line(output)
    
    def _detab(self, text):
        r"""Iterate text line by line and convert tabs to spaces.
        >>> m = Markdown()
        >>> m._detab("\tfoo")
        '    foo'
        >>> m._detab("  \tfoo")
        '    foo'
        >>> m._detab("\t  foo")
        '      foo'
        >>> m._detab("  foo")
        '  foo'
        >>> m._detab("  foo\n\tbar\tblam")
        '  foo\n    bar blam'
        """
        if '\t' not in text:
            return text
        output = []
        for line in text.splitlines():
            output.append(self._detab_line(line))
        return '\n'.join(output)
    
    def reset(self):
        self.titleptr = []
    
    def convert2xmind(self, text):
        """Convert the given text."""
        if not self.topic:
            print("Please set the topic first")
            return
        self.reset()

        if not isinstance(text, str):
            # TODO: perhaps shouldn't presume UTF-8 for string input?
            text = str(text, 'utf-8')

        # Standardize line endings:
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Make sure $text ends with a couple of newlines:
        text += "\n\n"

        # Convert all tabs to spaces.
        text = self._detab(text)

        # Strip any lines consisting only of spaces and tabs.
        # This makes subsequent regexen easier to write, because we can
        # match consecutive blank lines with /\n+/ instead of something
        # contorted like /[ \t]*\n+/ .
        text = self._ws_only_line_re.sub("", text)
        # Remove multiple empty lines
        text = re.sub(r"[\n]+", "\n", text)
        mdSection = MDSection("test", text)
        mdSection.toXmind(self.topic)
    

if __name__ == "__main__":
    pass
  