import re
from typing import Tuple, Dict

from eips_exposed.common import getLogger

RFC_822_HEADER = r'^([\w\-]+)\: ([\w\s\number\/\:\?\.\,;@&\*<>\(\)\'"`_\-=]*)$'

log = getLogger(__name__)


def pluck_headers(eip_text: str) -> Tuple[dict, str]:
    """ Remove and return the RFC 822 headers from EIP text """

    lines = eip_text.split('\n')
    line_count = 0
    headers: Dict = {}
    found_end = False

    assert lines[0] == '---', 'EIP Appears to be malformed'

    for ln in lines[1:]:
        line_count += 1
        if ln.startswith('---'):
            found_end = True
            break
        matches = re.fullmatch(RFC_822_HEADER, ln)
        if not matches or len(matches.groups()) != 2:
            log.warning('EIP Header parser error')
            log.debug('Invalid line: {}'.format(ln))
        else:
            log.debug('Parsed header {}'.format(matches.group(1)))
            headers[matches.group(1)] = matches.group(2)

    if not found_end:
        raise SyntaxError('EIP Appears to be malformed.  Did not find end of headers')

    return (headers, '\n'.join(lines[line_count + 1:]))
