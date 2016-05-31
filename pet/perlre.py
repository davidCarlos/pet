# vim:ts=2:sw=2:et:ai:sts=2
# Copyright 2011, Ansgar Burchardt <ansgar@debian.org>
#
# Released under the same terms as the original software, see below.
#
# Based on quoted_regex_parse from uscan which has the following copyright
# notice:
#
# Originally written by Christoph Lameter <clameter@debian.org> (I believe)
#
# Modified by Julian Gilbey <jdg@debian.org>
#
# HTTP support added by Piotr Roszatycki <dexter@debian.org>
#
# Rewritten in Perl, Copyright 2002-2006, Julian Gilbey
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from pet.exceptions import RegexpError

import re

_re_op = re.compile(r'^(s|tr|y)(.*)$')
_markers = {'{': '}', '(': ')', '[': ']'}

_pattern_rules = [
    # POSIX character classes
    (re.compile(r'\[:alpha:\]'), r'A-Za-z'),
    (re.compile(r'\[:alnum:\]'), r'A-Za-z0-9'),
    # missing: [:ascii:]
    (re.compile(r'\[:blank:\]'), r' \t'),
    # missing: [:cntrl:]
    (re.compile(r'\[:digit:\]'), r'\d'),
    # missing: [:graph:]
    (re.compile(r'\[:lower:\]'), r'a-z'),
    # missing: [:print:], [:punct:]
    (re.compile(r'\[:space:\]'), r'\s'),  # missing: + vertical tab
    (re.compile(r'\[:upper:\]'), r'A-Z'),
    (re.compile(r'\[:word:\]'), r'\w'),
    (re.compile(r'\[:xdigit:\]'), r'0-9a-fA-F'),
]

_replacement_rules = [
    # backrefs
    (re.compile(r'\$&'), r'\\g<0>'),
    (re.compile(r'\$\{?(\d)\}?'), r'\\g<\1>'),
]

PATTERN = 0
REPLACEMENT_MARKER = 1
REPLACEMENT = 2
FLAGS = 3
RE_IGNORECASE = 2


def compile(pattern):
    """Compile a regular expression pattern into a regular expression object,
    which can be used for matching using its match() and search() methods."""
    for regex, sub in _pattern_rules:
        pattern = regex.subn(sub, pattern)[0]
    return re.compile(pattern)


def not_null_regex(regexp, string):
    """Verify if the regex is not null; if False, return string."""
    regexp = regexp.strip()
    if regexp == "":
        regex_is_not_null = False
    else:
        regex_is_not_null = True

    return regex_is_not_null


def operator_matching(regexp, string):
    """Verify if the regex is valid, if not, raise regexp RegexpError."""
    match_op = _re_op.match(regexp)
    if not match_op:
        raise RegexpError(
            "Unknown operator in regular expression '{0}'.".format(regexp)
        )
    op = match_op.group(1)

    if op != 's':
        raise NotImplemented("Operator '{0}' not implemented.".format(op))

    return match_op


def initial_decoding(regexp, string):
    """State machine."""
    match_op = operator_matching(regexp, string)
    arguments = match_op.group(2)
    marker = arguments[0]
    end_marker = _markers.get(marker, marker)
    last_was_escape = False

    stage = PATTERN
    pattern = replacement = flags = ""
    for char in arguments[1:]:
        if stage == REPLACEMENT_MARKER:
            end_marker = _markers.get(char, char)
            stage = REPLACEMENT
            continue
        if last_was_escape:
            last_was_escape = False
            if stage == PATTERN:
                pattern += char
            elif stage == REPLACEMENT_MARKER:
                raise RegexpError("Invalid regular expression.")
            elif stage == REPLACEMENT:
                replacement += char
            else:
                flags += char
        elif char == end_marker:
            if stage == PATTERN:
                if marker != end_marker:
                    stage = REPLACEMENT_MARKER
                else:
                    stage = REPLACEMENT
            else:
                stage = FLAGS
        else:
            if char == "\\":
                last_was_escape = True
            if stage == PATTERN:
                pattern += char
            elif stage == REPLACEMENT:
                replacement += char
            else:
                flags += char

    if stage != FLAGS:
        raise RegexpError("Invalid regular expression.")

    return pattern, replacement, flags


def flag_decoding(regexp, string):
    """Defines the count variable."""
    flags = initial_decoding(regexp, string)[2]
    count = 1
    py_flags = 0
    for flag in flags:
        if flag == 'i':
            py_flags |= RE_IGNORECASE
        elif flag == 'g':
            count = 0
        else:
            raise RegexpError(
                "Unknown flag '{0}' used in regular expression.".format(flags))
    return count, py_flags


def regex_in_rules(regexp, string):
    """Defines the pattern and replacement / replace with replacement after
    every occurrence of pattern."""
    pattern = initial_decoding(regexp, string)[0]
    replacement = initial_decoding(regexp, string)[1]
    for regex, sub in _pattern_rules:
        pattern = regex.subn(sub, pattern)[0]
    for regex, sub in _replacement_rules:
        replacement = regex.subn(sub, replacement)[0]

    return pattern, replacement


def get_python_version():
    import sys
    tuple_python_version = sys.version_info
    major_version = tuple_python_version[0]
    return major_version


def apply_substitute_regex(regex_rules, string, flags_decode):
    """Apply pattern and replacement on the string and return."""
    count = flags_decode[0]
    flags = flags_decode[1]

    pattern = regex_rules[0]
    replacement = regex_rules[1]
    try:
        python_version = get_python_version()
        if python_version >= 3:
            regex_applied = re.subn(
                pattern, replacement, string, count=count, flags=flags
            )
        else:
            regex_applied = re.subn(
                pattern, replacement, string, count=count
            )
        string_regex_applied = regex_applied[0]
    except:
        string_regex_applied = string

    return string_regex_applied


def apply_perlre(regexp, string):
    """Method to call all other methods."""
    empty_regex = not_null_regex(regexp, string)
    if empty_regex:
        operator_matching(regexp, string)
        regex_rules = regex_in_rules(regexp, string)
        flags = flag_decoding(regexp, string)
        string_regex_applied = apply_substitute_regex(
            regex_rules, string, flags
        )
    else:
        string_regex_applied = string

    return string_regex_applied
