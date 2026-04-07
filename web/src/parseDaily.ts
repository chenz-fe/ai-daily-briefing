import type { DailyMeta, DailyFull, DailySection, DailyItem } from './types'

// 通过 Vite 的 raw 导入，将 ../../daily_news 下的 md 文件作为字符串读入
// src 位于 web/src，daily_news 在 web 的上一级目录，因此需要 ../../
const rawFiles = import.meta.glob('../../daily_news/*.md', { as: 'raw', eager: true }) as Record<
  string,
  string
>

const FRONTMATTER_DELIM = '---'

const sectionIdByIndex = ['products', 'models', 'events', 'trends'] as const

function parseFrontmatterAndBody(raw: string) {
  const parts = raw.split(FRONTMATTER_DELIM)
  if (parts.length < 3) {
    return { frontmatter: {}, body: raw }
  }
  const fmText = parts[1]
  const body = parts.slice(2).join(FRONTMATTER_DELIM).trim()
  const frontmatter: Record<string, string> = {}
  fmText
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .forEach((line) => {
      const idx = line.indexOf(':')
      if (idx === -1) return
      const key = line.slice(0, idx).trim()
      let value = line.slice(idx + 1).trim()
      if (value.startsWith('"') && value.endsWith('"')) {
        value = value.slice(1, -1)
      }
      frontmatter[key] = value
    })
  return { frontmatter, body }
}

function ensureDescription(frontmatter: Record<string, string>, body: string) {
  if (frontmatter.description && frontmatter.description.trim()) return frontmatter.description
  const firstLine = body.split('\n')[0].trim()
  if (firstLine.startsWith('摘要：')) {
    return firstLine.replace('摘要：', '').trim()
  }
  return ''
}

function splitSections(body: string): { title: string; content: string }[] {
  const lines = body.split('\n')
  const sections: { title: string; content: string }[] = []
  let currentTitle = ''
  let buffer: string[] = []

  const flush = () => {
    // 仅当有明确章节标题时才生成 section，丢弃开头的摘要等无标题内容
    if (currentTitle.trim() && buffer.some((l) => l.trim())) {
      sections.push({ title: currentTitle, content: buffer.join('\n').trim() })
    }
    buffer = []
  }

  for (const line of lines) {
    const m = line.match(/^##\s+(?:\d\.\s*)?(.*)$/)
    if (m) {
      flush()
      currentTitle = m[1].trim()
    } else {
      buffer.push(line)
    }
  }
  flush()
  return sections
}

function splitItems(section: { title: string; content: string }): DailySection {
  const { content, title } = section
  const lines = content.split('\n')
  const items: DailyItem[] = []
  let current: DailyItem | null = null

  const isModelsSection = title.includes('头部模型') || title.includes('头部玩家')

  const flush = () => {
    if (current && current.paragraphs.length) {
      items.push(current)
    }
  }

  for (const line of lines) {
    const h = line.match(/^###\s+(.*)$/)
    if (h) {
      flush()
      current = {
        id: h[1].trim(),
        title: h[1].trim(),
        paragraphs: []
      }
      continue
    }
    if (!current) {
      // 没有 ### 时，把整段当作一个条目
      if (line.trim()) {
        current = {
          id: 'entry-0',
          title: section.title,
          paragraphs: [line.trim()]
        }
      }
      continue
    }
    const trimmed = line.trim()
    if (!trimmed) continue

    // 各场景下的头部模型与玩家：解析形如 "- **ServiceNow**：一句话" 的玩家条目
    if (isModelsSection) {
      const playerMatch = trimmed.match(/^-+\s*\*\*(.+?)\*\*\s*[:：]?(.*)$/)
      if (playerMatch) {
        flush()
        const name = playerMatch[1].trim()
        let summary = playerMatch[2].trim()

        // 提前从 summary 中抽出 [原文链接](URL)（来源：XXX），避免原样出现在正文里
        let link: string | undefined
        let source: string | undefined
        const linkMatchInSummary = summary.match(/\[(.+?)\]\((.+?)\)\s*[（(]来源[：:](.+?)[）)]/)
        if (linkMatchInSummary) {
          const before = summary.slice(0, linkMatchInSummary.index).trim()
          if (before) {
            summary = before
          } else {
            summary = ''
          }
          link = linkMatchInSummary[2].trim()
          source = linkMatchInSummary[3].trim()
        }

        current = {
          id: name,
          title: name,
          paragraphs: summary ? [summary] : []
        }
        if (link) {
          current.link = link
        }
        if (source) {
          current.source = source
        }
        continue
      }
    }

    // 匹配行中出现的 [原文链接](URL)（来源：XXX），可能在句子末尾
    const linkMatch = trimmed.match(/\[(.+?)\]\((.+?)\)\s*[（(]来源[：:](.+?)[）)]/)
    if (linkMatch) {
      const before = trimmed.slice(0, linkMatch.index).trim()
      if (before) {
        current.paragraphs.push(before)
      }
      current.link = linkMatch[2].trim()
      current.source = linkMatch[3].trim()
      continue
    }

    current.paragraphs.push(trimmed)
  }
  flush()

  return {
    id: '',
    title,
    items
  }
}

function buildDailyFromRaw(raw: string): DailyFull | null {
  const { frontmatter, body } = parseFrontmatterAndBody(raw)
  const title = frontmatter.title || ''
  const date = frontmatter.date || ''
  const slug = frontmatter.slug || ''
  if (!date) return null

  const description = ensureDescription(frontmatter, body)
  const sectionBlocks = splitSections(body)
  const sections: DailySection[] = sectionBlocks.map((s, idx) => {
    const base = splitItems(s)
    const id = sectionIdByIndex[idx] ?? `sec-${idx}`
    return { ...base, id }
  })

  return {
    date,
    slug: slug || `weekly-${date}`,
    title: title || `AI 周报 ${date}`,
    description,
    sections
  }
}

export const dailyMap: Record<string, DailyFull> = {}
export const dailyList: DailyMeta[] = []

Object.entries(rawFiles).forEach(([_, raw]) => {
  const daily = buildDailyFromRaw(raw)
  if (!daily) return
  dailyMap[daily.slug] = daily
  dailyList.push({
    date: daily.date,
    slug: daily.slug,
    title: daily.title,
    description: daily.description
  })
})

dailyList.sort((a, b) => (a.date < b.date ? 1 : -1))

