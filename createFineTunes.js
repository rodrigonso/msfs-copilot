import {openai} from './api.js'

async function createFineTunes() {
    try {
        const response = await openai.createFineTune({
            training_file: 'file-YNyPHRlXk3oMXHRV646BTnUm',
            model: 'davinci'
        })
        console.log('response', response)
    } catch (error) {
        console.log('err: ', error.response.data.error)
    }
}

createFineTunes();