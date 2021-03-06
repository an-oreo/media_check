#! /usr/bin/env python
# vim:fileencoding=utf-8
# -*- coding: utf-8 -*-
"""
vlc_check_audio
metadata.py
Author: Danyal Ahsanullah
Date: 7/30/2017
Copyright (c):  2017 Danyal Ahsanullah
License: N/A
Description: 
"""
import os as _os
import itertools as _it
from copy import deepcopy as _deepcopy

from mutagen.mp3 import EasyMP3 as _MP3
from mutagen.flac import FLAC as _FLAC

_F_TYPES = {'mp3': _MP3,
            'flac': _FLAC,
            }


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = _it.tee(iterable)
    next(b, None)
    return zip(a, b)


class Metadata:
    # list of some possible ID3 tags -- from mutagen's easyid3.py
    possible_tags = {"album",
                     "bpm",
                     "compilation",  # iTunes extension
                     "composer",
                     "copyright",
                     "encodedby",
                     "lyricist",
                     "length",
                     "media",
                     "mood",
                     "title",
                     "version",
                     "artist",
                     "albumartist",
                     "conductor",
                     "arranger",
                     "discnumber",
                     "organization",
                     "tracknumber",
                     "author",
                     "albumartistsort",  # iTunes extension
                     "albumsort",
                     "composersort",  # iTunes extension
                     "artistsort",
                     "titlesort",
                     "isrc",
                     "discsubtitle",
                     "language",
                     }

    def __init__(self, afile=None, f_type='mp3'):
        self.file = _os.path.basename(afile)
        self.audio = _F_TYPES[f_type.lower()](afile)

    @property
    def tags(self):
        return _deepcopy(self.audio)

    @property
    def length(self):
        return self.audio.info.length

    def get_audio_metadata(self, fields=None):
        if fields:
            return [self.audio.get(field, ('',))[0] for field in fields]
        else:
            return self.audio.items()

    def edit_meta_data(self):
        for field in self.audio:
            print('%s: %s' % (field, self.audio[field][0]))
        flag = True
        tmp_dict = self.audio
        while flag:
            new_args = input(self._edit_prompt)
            tmp_args = new_args.strip().lower()
            # if tmp_args == 'cancel':
            if tmp_args == 'c':
                flag = False
            # elif tmp_args == 'quit':
            elif tmp_args == 'q':
                self.audio.update(tmp_dict)
                flag = False
            # elif tmp_args == 'save':
            elif tmp_args == 's':
                self.audio.update(tmp_dict)
                self.audio.save()
            # elif tmp_args == 'view':
            elif tmp_args == 'v':
                for field in tmp_dict:
                    print('%s: %s' % (field, tmp_dict[field][0]))
            else:
                new_args = {key.strip(): value.strip() for
                            pair in new_args.split(',,') for
                            key, value in pairwise(pair.split('::'))}
                tmp_dict.update(new_args)

    def save(self, update_dict):
        self.update(update_dict)
        self.audio.save()

    def update(self, update_dict):
        self.audio.update(self.sanitize(update_dict))

    def sanitize(self, unclean_dict):
        return {k: v for k, v in unclean_dict.items() if k in self.possible_tags}

    @staticmethod
    def parse_update_line(update_string):
        update_dict = {key.strip(): [value.strip()] for
                       pair in update_string.split(',,') for
                       key, value in pairwise(pair.split('::'))}
        return update_dict
