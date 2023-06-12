import 'dotenv/config'
import { Configuration, OpenAIApi } from "openai"

const openAiApiKey = process.env.OPEN_AI_SECRET
const config = new Configuration({
    apiKey: openAiApiKey
})

export const openai = new OpenAIApi(config)