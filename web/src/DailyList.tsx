import type { DailyMeta } from './types'

interface Props {
  items: DailyMeta[]
  onOpen: (slug: string) => void
}

export function DailyList({ items, onOpen }: Props) {
  const sorted = [...items].sort((a, b) => (a.date < b.date ? 1 : -1))

  return (
    <div className="page">
      <header className="page-header">
        <div className="page-header-left">今日 AI 简报</div>
        <div className="page-header-right">Daily Briefing</div>
      </header>
      <main className="page-main">
        <section className="intro">
          <p>少而精、可读完。按日期倒序浏览，每天花 10–15 分钟了解 AI 进展。</p>
        </section>

        <section className="list">
          {sorted.map((d) => (
            <article key={d.slug} className="daily-card" onClick={() => onOpen(d.slug)}>
              <div className="daily-card-date">{d.date}</div>
              <div className="daily-card-description">{d.description}</div>
              <button
                type="button"
                className="link-button"
                onClick={(e) => {
                  e.stopPropagation()
                  onOpen(d.slug)
                }}
              >
                阅读全文 →
              </button>
            </article>
          ))}
        </section>
      </main>
    </div>
  )
}

