import {openai} from './api.js'

async function createCompletion() {
    try {
        const response = await openai.createCompletion({
            model: 'davinci:ft-personal-2023-06-12-06-57-15',
            prompt: 'pre start checklist for king air 350',
            max_tokens: 200
        })

        if (response.data) {
            console.log('choices: ', response.data.choices)
        }

    } catch (error) {
        console.log('error: ', error)
    }
}

createCompletion()
