
style = {
    'NORMAL': '\033[0m',
    'BOLD': '\033[1m',
    'FAINT': '\033[2m',
    'ITALICS': '\033[3m',
    'UNDERLINE': '\033[4m',
    'RED': '\033[0;31m',
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'GREY': '\033[37;2m',
    'YELLOW': '\033[33m',
    'YELLOW_BRIGHT_BOLD': '\033[33;1m',
    'YELLOW_BRIGHT_BOLD_UNDERLINED': '\033[33;1;4m',
    'YELLOW_BRIGHT_BOLD_INVERTED': '\033[33;7m',
    'BLUE_UNDERLINED': '\033[94;4m',
}
STYLE_RESET = '\033[0m'

# A mapping of 'find' and 'replace' strings. No regex/wildcards are
# used. In this default configuration, common HTML tags
# (eg: '<b>') are replaced with ANSI style characters to
# add color (and remove the tag).
replace_arr = {
    '<h1>': style['YELLOW_BRIGHT_BOLD'], '</h1>': STYLE_RESET,
    '<h2>': style['YELLOW'], '</h2>': STYLE_RESET,
    '<b>': style['BOLD'], '</b>': STYLE_RESET,
    '<i>': style['GREY'], '</i>': STYLE_RESET,  # 'ITALICS' doesn't show.
    '<u>': style['UNDERLINE'], '</u>': STYLE_RESET,
    '<a>': style['BLUE_UNDERLINED'], '</a>': STYLE_RESET,
    '<red>': style['RED'], '</red>': STYLE_RESET,
    '<green>': style['GREEN'], '</green>': STYLE_RESET,
    '<blue>': style['BLUE'], '</blue>': STYLE_RESET,
    '<grey>': style['GREY'], '</grey>': STYLE_RESET,

    '<title>': style['YELLOW_BRIGHT_BOLD_INVERTED'] + '   ',
    '</title>': '   ' + STYLE_RESET,
    '<hr>': '----------------------------------------',
}

def prettify(text):
    for key in replace_arr:
        text = text.replace(key, replace_arr[key])
    return text

def debug(text): 
    print(prettify("<green>[DEBUG] : \n{}</green>".format(text)))

def error(text): 
    print(prettify("<red>[ERROR] : {}</red>".format(text)))

def ok(text): 
    print(prettify("<green>{}</green>".format(text)))

def title(text):
    print(prettify("<title>{}</title>").format(text))