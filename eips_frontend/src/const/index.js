/**
 * Useful constants
 */

export const GRAPHQL_URL = process.env.REACT_APP_GRAPHQL_URL ?
  process.env.REACT_APP_GRAPHQL_URL :
  'https://graphql.eips.exposed/graphql';

// Mappings to resolve Enums from graphql
export const EIPS_STATUSES = {
  DRAFT: {
    extraClass: 'has-text-info',
    text: 'Draft'
  },
  LAST_CALL: {
    extraClass: 'has-text-warning',
    text: 'Last Call'
  },
  ACCEPTED: {
    extraClass: 'has-text-success',
    text: 'Accepted'
  },
  ACTIVE: {
    extraClass: 'has-text-success',
    text: 'Active'
  },
  FINAL: {
    extraClass: 'has-text-success',
    text: 'Final'
  },
  DEFERRED: {
    extraClass: 'has-text-grey-light',
    text: 'Deferred'
  },
  SUPERSEDED: {
    extraClass: 'has-text-warning',
    text: 'Superseded'
  },
  REJECTED: {
    extraClass: 'has-text-danger',
    text: 'Rejected'
  },
};

export const EIPS_TYPES = {
  META: {
    text: 'Meta'
  },
  INFORMATIONAL: {
    text: 'Informational'
  },
  STANDARDS: {
    text: 'Standards'
  },
};

export const EIPS_CATEGORIES = {
  ERC: {
    text: 'ERC'
  },
  NETWORKING: {
    text: 'Networking'
  },
  INTERFACE: {
    text: 'Interface'
  },
  CORE: {
    text: 'Core'
  },
};
