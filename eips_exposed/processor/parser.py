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

    assert lines[0] == '---', 'EIP Appears to be malformed'

    for ln in lines[1:]:
        if ln == '---':
            break
        line_count += 1
        matches = re.fullmatch(RFC_822_HEADER, ln)
        if not matches or len(matches.groups()) != 2:
            log.warning('EIP Header parser error')
            log.debug('Invalid line: {}'.format(ln))
        else:
            headers[matches.group(1)] = matches.group(2)

    return (headers, '\n'.join(lines[line_count:]))
