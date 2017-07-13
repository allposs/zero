#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import markdown2
import codecs
css = '''
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="stylesheet" href="http://blog.allposs.com/theme/css/bootstrap.min.css" type="text/css" />
<style type="text/css">

</style>
'''
def main(argv):
    md_name = '%s.md' % (argv[0])
    
    with codecs.open(md_name, mode='r', encoding='utf-8') as mdfile:
        #with codecs.open("friendly.css", mode='r', encoding='utf-8') as cssfile:
            md_text = mdfile.read()
            #css_text = cssfile.read()
 
            extras = ['code-friendly', 'fenced-code-blocks', 'footnotes']
            html_text = markdown2.markdown(md_text, extras=extras)
            html_name = '%s.html' % (md_name[:-3])
            with codecs.open(html_name, 'w', encoding='utf-8', errors='xmlcharrefreplace') as output_file:
                output_file.write(css+html_text)
#if __name__ == "__main__":
#    if len(sys.argv) == 2:
#        main("1")
#    else:
#        print("Error:please specify markdown file path")
if __name__ == "__main__":
    main("1")