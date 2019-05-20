/**
 * Useful constants
 */

// Mapping to resolve Enums from graphql
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
}
