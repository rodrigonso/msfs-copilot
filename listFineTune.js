import {openai} from './api.js'

async function listFineTune() {
    try {
        const response = await openai.listFineTunes()
        console.log('data: ', response.data.data)
    } catch (error) {
        console.log("error: ", error)
    }
}

listFineTune()