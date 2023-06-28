import {openai} from './api.js'

async function createCompletion() {
    try {
        const response = await openai.createCompletion({
            model: 'davinci:ft-personal-2023-06-27-02-54-53',
            prompt: 'pre start checklist for Boeing 737-800 -> \n',
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
