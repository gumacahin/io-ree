#!/usr/bin/env python
#
# MainHandler
#
# @package 	IOREE
# @author 	Marco Enrico Alviar
# @copyright 	2012 Author
#

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
import os, re, cgi, logging
import time


class MainHandler(webapp.RequestHandler):

    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))


    def post(self):
        validFlags = {'I':re.I, 'L':re.L, 'M':re.M, 'S':re.S, 'U':re.U, 'X':re.X}
        activeFlags = self.request.get('flags')

        pattern = self.request.get('re')
        string = self.request.get('string')

        messages = []
        flags = 0
        result = None
        matches = None
        match = None
        resultAll = None
        groups = []
        try:
            for f in activeFlags:
                flags |= validFlags[f.upper()]
        except (KeyError):
            messages.append('Invalid flag: ' + cgi.escape(f))
        else: 
            try:
                # adding the parens will let us capture the entire match for 
                # the pattern not only the groups
                resultAll = re.findall('(' + pattern + ')', string, flags) # match the entire patten
                
            except re.error, error:
                messages.append(error.message)

        matches = [];
        if resultAll:
            for res in resultAll:
                if type(res) is tuple: # if it's a tuple there are group matches
                    matches.append({'match':res[0], 'groups': res[1:]})
                else:
                    matches.append({'match':res, 'groups': None})

        highlightedString = ''
        tmp = string #cgi.escape(string)
        colors = ['#4978ef', '#f04acc', '#f0c14a', '#4af06e']
        i = 0;
        tmp = cgi.escape(tmp)
        for m in matches:
            start = tmp.find(cgi.escape(m['match']))
            end = start + len(cgi.escape(m['match']))
            highlightedString += tmp[0:start] + '<span style="background:' + colors[i % 4] + '">' + tmp[start:end] + '</span>'
            tmp = tmp[end:]
            i += 1
        if tmp:
            highlightedString += tmp

        highlightedString = highlightedString.replace('  ', '&nbsp;' * 2).replace('\t', '&nbsp;' *4).replace('\n', '&nbsp;<br />')

        # check for groups
        for m in matches: 
            if m['groups']:
                hasGroups = True
                break
        else: hasGroups = False

        hasMatches = True if matches else False
            
        logging.debug(highlightedString);
        path = os.path.join(os.path.dirname(__file__), 'result.html')
        self.response.out.write(template.render(path, dict(pattern=pattern,
                                                           string=highlightedString,
                                                           flags=activeFlags,
                                                           messages='<br />'.join(messages),
                                                           hasGroups=hasGroups,
                                                           hasMatches=hasMatches,
                                                           matches=matches)))


def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
