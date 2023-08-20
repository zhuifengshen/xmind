def convert_to_indented_list(markdown_text):
    lines = markdown_text.split('\n')
    indented_lines = []
    indentation_level = 0

    for line in lines:
        stripped_line = line.lstrip()

        if stripped_line.startswith(('1.', '*', '-')):
            indented_lines.append('\t' * indentation_level + stripped_line)
            indentation_level += 1
        elif stripped_line == '':
            indentation_level = 0
            indented_lines.append(line)
        else:
            indented_lines.append('\t' * indentation_level + line)

    indented_markdown = '\n'.join(indented_lines)
    return indented_markdown

markdown_input = """
- Item 1
    - Subitem A
        - Subsubitem i
        - Subsubitem ii
    - Subitem B
- Item 2
    1. Nested Numbered Item 1
    1. Nested Numbered Item 2
"""

indented_markdown = convert_to_indented_list(markdown_input)
print(indented_markdown)
