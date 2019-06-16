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
    query getEIPs ($limit: Int, $offset: Int, $tag: String, $category: String, $status: String, $search: String) {
      eips (limit: $limit, offset: $offset, tag: $tag, category: $category, status: $status, search: $search) {
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
        errors
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

export const getErrors = gql`
    query getErrors {
      errors {
        eipId
        errorType
        when
        message
      }
    }
`

export const getCommits = gql`
    query getCommits ($limit: Int, $offset: Int, $eipId: Int, $search: String) {
      commits (limit: $limit, offset: $offset, eipId: $eipId, search: $search) {
        commitHash
        author
        committer
        committedDate
        message
      }
    }
`

export const getCategories = gql`
    query getCategories {
      categories {
        category
        eipCount
      }
    }
`

export const getStatuses = gql`
    query getStatuses {
      statuses {
        status
        eipCount
      }
    }
`
