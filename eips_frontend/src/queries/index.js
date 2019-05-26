import gql from 'graphql-tag';

export const getAllEIPs = gql`
    query getAllEIPs ($limit: Int, $offset: Int) {
      eips (limit: $limit, offset: $offset) {
        eipId
        eipType
        title
        category
        tags
        status
      }
    }
`

export const getEIPs = gql`
    query getEIPs ($limit: Int, $offset: Int, $tag: String, $search: String) {
      eips (limit: $limit, offset: $offset, tag: $tag, search: $search) {
        eipId
        eipType
        title
        category
        tags
        status
      }
    }
`

export const getEIP = gql`
    query getEIP ($eipId: ID!) {
      eip (eipId: $eipId) {
        eipId
        eipType
        status
        title
        author
        updated
        discussionsTo
        reviewPeriodEnd
        resolution
        category
        tags
        fullText
      }
    }
`

export const getStats = gql`
    query getStats {
      stats {
        eips
        commits
        contributors
        issues
      }
    }
`

export const getTags = gql`
    query getTags ($eipId: ID) {
      tags (eipId: $eipId) {
        tagName
        eipsCount
      }
    }
`
