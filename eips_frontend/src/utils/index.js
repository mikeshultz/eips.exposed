import { replace } from 'lodash/string';

import { ADDR_TRUNC_LENGTH, ADDRESS_PATTERN } from '../const';

export function truncateAddress(addr) {
  return `${addr.slice(0, ADDR_TRUNC_LENGTH)}...`;
}

export function truncateAddressInString(s) {
  return replace(s, ADDRESS_PATTERN, truncateAddress);
}

export function truncate(s, len) {
  if (s.length < len) return s
  return `${s.slice(0, len)}...`
}
