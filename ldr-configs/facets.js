export default {
    facets: {
        'generic': {
            list: [
                'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
            ],
            config: {

            }
        },
        'http://localhost:5820/votes/query': {
            list: [
                'http://localhost:5820/databases/votes/Agent',
                'http://localhost:5820/databases/votes/votesOn',
                'http://localhost:5820/databases/votes/Bill',
                'http://localhost:5820/databases/votes/VotingAssembly'
            ],
            config: {
                'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': {
                    label: ['Type'],
                    hint: ['Type of the resource under investigation.']
                },
                'http://localhost:5820/databases/votes/Bill': {
                    label: ['Bill'],
                    hasLinkedValue: 1
                },
                'http://localhost:5820/databases/votes/VotingAssembly': {
                    label: ['VotingAssembly'],
                    hasLinkedValue: 1
                },
                'http://localhost:5820/databases/votes/votesOn': {
                    label: ['votesOn'],
                    hasLinkedValue: 1
                }
            }
        }
    }
};

