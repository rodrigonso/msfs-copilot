import {openai} from './api.js'

async function createCompletion() {
    try {
        const response = await openai.createCompletion({
            model: '',
            prompt: '',
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
