#!/usr/bin/env python
import re
import os

NOTEBOOK_PATH = '/home/rrodrigues/.rednotebook/data'

class EmptyDayException(Exception):
    """No info was entered for this date."""
        
class Parser(object):

    """Parses RedNotebook monthly files.
    
    This is a very basic parser used to extract Pomodoro references for each
    day. It has the following limitations:
    
        - Basically assumes there is nothing but the Pomodoro references in the
          day's text.
        - Ignores any Tags. 
        - Ignores any Categories. 
        - In the fancy cases where the text field ends up surrounded by double
          quotes instead of single quotes, it breaks.
    
    """

    def __init__(self, nb_path=NOTEBOOK_PATH):
        self.nb_path = nb_path

    def _get_nb_filename(self, date):
        return os.path.join(self.nb_path, date.strftime('%Y-%m.txt'))

    @staticmethod
    def _parse_day_block(day_block_list):
        day_blocks = {}
        is_content = False
        for index, token in enumerate(day_block_list):
            if token.isdigit() and not is_content:
                day = int(token)
                is_content = True
            elif is_content:
                day_blocks[day] = token
                is_content = False
            else:
                pass
        return day_blocks

    def _get_day(self, date):
        day_filename = self._get_nb_filename(date)
        if not os.path.isfile(day_filename):
            raise EmptyDayException
        with open(day_filename, 'r') as nb_file:
            file_contents = nb_file.read()
        day_blocks_list = re.split('^(\d+):', file_contents, flags=re.MULTILINE)
        day_blocks = self._parse_day_block(day_blocks_list)
        try:
            return day_blocks[date.day]
        except KeyError:
            raise EmptyDayException

    def _get_text(self, block):
        after_text = re.split('\Wtext:', block)[1]
        quote_set = False
        started_text = False
        ended_text = False
        text = [] 
        for token in after_text:
            if token == "'":
                if not started_text:
                    #first quote, text starts
                    started_text = True
                elif quote_set and started_text:
                    #second quote
                    text.append("'")
                    quote_set = False
                elif not quote_set and started_text:
                    # quote in the middle of text, maybe the end or first of an
                    # escape sequence
                    quote_set = True
            else:
                if quote_set:
                    # First character after a quote is not a quote, so this
                    # must be the end
                    break
                elif started_text:
                    # Normal text, add it to the output
                    text.append(token)
                else:
                    # Text hasn't started yet, discard token
                    continue
        return ''.join(text)

    def get_pomodoros(self):
        # TODO
        pass


