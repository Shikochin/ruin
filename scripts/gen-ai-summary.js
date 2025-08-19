#!/usr/bin/env node
import fs from 'fs'
import matter from 'gray-matter'
import OpenAI from 'openai'
import { glob } from 'glob'

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
    baseURL: process.env.OPENAI_API_BASE || 'https://api.openai.com/v1',
})

async function generateSummary(content) {
    const prompt = `请为以下文章写一个简短的摘要，直接输出摘要，不要给我选择（不超过100字，中文）：\n\n${content}`
    const response = await openai.chat.completions.create({
        model: 'gemini-2.5-pro',
        messages: [{ role: 'user', content: prompt }],
    })
    return response.choices[0].message.content.trim()
}

async function main() {
    const files = glob.sync('source/_posts/**/*.md')

    for (const filePath of files) {
        if (!filePath.endsWith('.md')) continue
        const raw = fs.readFileSync(filePath, 'utf-8')
        const parsed = matter(raw)
        if (parsed.data.summary) {
            console.log(`✅ ${filePath} 已有摘要，跳过`)
            continue
        }
        const text = parsed.content
            .replace(/<[^>]+>/g, '') // 去掉 HTML
            .replace(/```[\s\S]*?```/g, '') // 去掉代码块
            .replace(/!\[.*?\]\(.*?\)/g, '') // 去掉图片
            .slice(0, 1000)
            .trim()
        if (!text) {
            console.log(`⚠️ ${filePath} 内容为空或无可生成文本，跳过`)
            continue
        }

        console.log(`📝 正在为 ${filePath} 生成摘要...`)
        const summary = await generateSummary(parsed.content)
        parsed.data.summary = summary

        fs.writeFileSync(filePath, matter.stringify(parsed), 'utf-8')
        if (!summary) {
            console.log(`⚠️ ${filePath} 模型没有生成摘要`)
            continue
        }
        console.log(`✨ 已生成摘要: ${summary}`)
    }
}

main().catch((err) => {
    console.error(err)
    process.exit(1)
})
