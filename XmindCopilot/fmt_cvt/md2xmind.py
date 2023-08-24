import re

class MDTextSnippet(object):
    pass


class MDSection(object):
    """Markdown Section Class
    ---
    Mangage the markdown sections identified by `#`
    """
    
    titleLineMatchStr = r"\s{0,3}(#{1,6})\s{1,}(.*)"
    # FIXME: Seems level 1 is not found
    listLineMatchStr = r"(\s{0,})(\d{1,}\.|[+*-])\s{1,}(.*)"
    
    def __init__(self, title: str = "", text: str = ""):
        """
        :param title: Title
        :param text: Text (Should not contain title)
        """
        self.title = title
        self.text = text
        self.textList = text.strip('\n').split('\n')
        self.nonSubSectionText = ''
        self.nonSubSectionTextList = []
        self.SubSection = []
        self.segment()
    
    def _getTitleLevel(self, line):
        """Get the level of the title
        """
        titleMatch = re.match(self.titleLineMatchStr, line)
        if titleMatch:
            return len(titleMatch.groups()[0])
        else:
            return None
    
    def _getListLevel(self, line, indent=2):
        """Get the level of the numbered list
        """
        listmatch = re.match(self.listLineMatchStr, line)
        if listmatch:
            return len(listmatch.groups()[0])//indent
        else:
            return None
    
    def segment(self):
        """Segment the text into sub-sections
        """
        maxLevel = 6  # The maximum level of the title
        lasti = None
        for i in range(len(self.textList)):
            line = self.textList[i]
            if self._getTitleLevel(line) and self._getTitleLevel(line) <= maxLevel:
                maxLevel = self._getTitleLevel(line)
                if lasti is not None:
                    title = re.match(self.titleLineMatchStr, self.textList[lasti]).groups()[1]
                    self.SubSection.append(MDSection(title, '\n'.join(self.textList[lasti+1:i])))
                lasti = i
            if lasti is None:
                self.nonSubSectionTextList.append(line)
            if i == len(self.textList)-1 and lasti is not None:
                title = re.match(self.titleLineMatchStr, self.textList[lasti]).groups()[1]
                self.SubSection.append(MDSection(title, '\n'.join(self.textList[lasti+1:])))
        self.nonSubSectionText = '\n'.join(self.nonSubSectionTextList)

    def elementSplit(self, text):
        """
        Split the markdown text into elements and process textline indentation.
        For example: code block, equation block, multilevel-list, table(not implemented), etc.
        """
        code_match = re.findall(r"(```.*?```)", text, re.S)
        latex_match = re.findall(r"(\$\$.*?\$\$)", text, re.S)
        lines = text.split('\n')
        outputList = []
        while lines:
            if code_match and lines and lines[0] in code_match[0]:  # Code block
                while lines and lines[0] in code_match[0]:
                    lines.pop(0)
                outputList.append(code_match.pop(0))
            elif latex_match and lines and lines[0] in latex_match[0]:  # Latex block
                while lines and lines[0] in latex_match[0]:
                    lines.pop(0)
                outputList.append(latex_match.pop(0))
            elif lines:
                if re.match(r'[\s\t]*$', lines[0]):  # Empty line
                    lines.pop(0)
                else:  # Indent handling
                    line = lines.pop(0)
                    level = self._getListLevel(line)
                    if level is not None:  # Note: Including the case of level 0
                        topictitle = "\t"*level + re.match(self.listLineMatchStr, line).groups()[2]
                    else:
                        topictitle = line
                    outputList.append(topictitle)
        return outputList
    
    def toXmind(self, parentTopic, cvtEquation=False, cvtWebImage=False, cvtHyperLink=False, index=-1):
        """Convert the section to xmind
        """
        if self.title:  # For the non-Root section
            topic = parentTopic.addSubTopicbyTitle(self.title)
        else:  # For the Root section (if title is not given, directly add the subsection to the parent topic)
            topic = parentTopic
        topic.addSubTopicbyIndentedList(self.elementSplit(self.nonSubSectionText), index)
        # FIXME: Maybe it is a better choice to remove these functions from TopicElement
        if cvtEquation:
            topic.convertTitle2Equation(recursive=True)
        if cvtWebImage:
            topic.convertTitle2WebImage(recursive=True)
        if cvtHyperLink:
            topic.convertTitleWithHyperlink(recursive=True)
        for subSection in self.SubSection:
            subSection.toXmind(topic, cvtEquation, cvtWebImage, cvtHyperLink)

    def toXmindText(self, removeHyperlink=True, parentIndent=0):
        """Convert the section to xmindtextlist
        """
        textList = []
        if self.title:
            textList.append("\t"*parentIndent + self.title)
        for line in self.elementSplit(self.nonSubSectionText):
            if removeHyperlink:
                line = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", line)
            textList.append("\t"*(parentIndent+1) + line)
        for subSection in self.SubSection:
            textList = textList + subSection.toXmindText(parentIndent=parentIndent+1)
        return textList
    
    # Debug
    def printSubSections(self, indent=4):
        print(" "*indent, self.title)
        for subSection in self.SubSection:
            subSection.printSubSections(indent+4)

class MarkDown2Xmind(object):
    
    _ws_only_line_re = re.compile(r"^[ \t]+$", re.M)
    tab_width = 4
    
    def __init__(self, topic=None):
        self.topic = topic
    
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
    
    def preProcess(self, text):
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
        return text
    
    def convert2xmind(self, text, cvtEquation=False, cvtWebImage=False, cvtHyperLink=False, index=-1):
        """Convert the given text."""
        if not self.topic:
            print("Please set the topic first")
            return
        text = self.preProcess(text)
        mdSection = MDSection("", text)
        mdSection.toXmind(self.topic, cvtEquation, cvtWebImage, cvtHyperLink, index=index)

    def convert2xmindtext(self, text):
        """Convert the given text."""
        text = self.preProcess(text)
        mdSection = MDSection("", text)
        textList = mdSection.toXmindText()
        for item in textList:
            item.replace("\n", "\r")
        return "\n".join(textList)

    def printSubSections(self, text):
        """Print the sub-sections of the given text."""
        text = self.preProcess(text)
        mdSection = MDSection("", text)
        mdSection.printSubSections()

if __name__ == "__main__":
    pass
  