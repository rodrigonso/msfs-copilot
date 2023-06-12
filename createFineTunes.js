import {openai} from './api.js'

async function createFineTunes() {
    try {
        const response = await openai.createFineTune({
            training_file: 'file-TsX0gEL47jF2U5YdO5MDtVZH',
            model: 'davinci'
        })
        console.log('response', response)
    } catch (error) {
        console.log('err: ', error.response.data.error)
    }
}

createFineTunes();