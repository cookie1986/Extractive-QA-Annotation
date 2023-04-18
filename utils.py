import re
from markdown import Markdown
from io import StringIO
import string


def remove_headers(input_markdown):
    # split markdown into individual lines
    split_lines = input_markdown.splitlines()
    # filter out lines with a header syntax
    no_header_lines = [line for line in split_lines if not line.startswith('#')]
    # re-join lines
    no_headers_markdown = '\n'.join([line for line in no_header_lines])

    return no_headers_markdown


def remove_images(markdown_text):
    # remove images and replace with empty string
    images_removed = re.sub(r'\[([^\]]+)\]\(([^)]+)\)\]\(\/\)', '', markdown_text, flags=re.MULTILINE)
    # remove images: ![image_name.png]()
    images_removed = re.sub(r'\!\[([^\]]*)\]\(([^)]*)\)', '', images_removed, flags=re.MULTILINE)

    return images_removed


def remove_links(text):
    # remove inline links: [link text](URL)
    links_removed = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', '', text)
    # remove reference-style links: [link text][reference]
    links_removed = re.sub(r'\[([^\]]+)\]\[([^\]]+)\]', '', links_removed)
    # remove reference definitions: [reference]: URL
    links_removed = re.sub(r'^\[[^\]]+\]: .+$', '', links_removed, flags=re.MULTILINE)

    return links_removed


# convert markdown file to plain text
def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


def init_unmark():
    # set __md as global variable
    global __md
    # patch Markdown
    Markdown.output_formats["plain"] = unmark_element
    __md = Markdown(output_format="plain")
    __md.stripTopLevelTags = False


# function to convert markdown to plain text
def unmark(text):
    return __md.convert(text)


# remove non-printable characters
def remove_nonprintable_chars(text):
    cleaned_text = ''.join(filter(lambda x: x in string.printable, text))
    
    return cleaned_text