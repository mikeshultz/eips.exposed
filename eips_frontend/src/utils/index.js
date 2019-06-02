import { replace } from 'lodash/string';

import { ADDR_TRUNC_LENGTH, ADDRESS_PATTERN } from '../const';

export function truncateAddress(addr) {
  return `${addr.slice(0, ADDR_TRUNC_LENGTH)}...`;
}

export function truncateAddressInString(s) {
  return replace(s, ADDRESS_PATTERN, truncateAddress);
}

export function truncate(s, len, elipsis=true) {
  if (s.length < len) return s
  let ret = `${s.slice(0, len)}`
  if (elipsis) ret = `${ret}...`
  return ret
}
