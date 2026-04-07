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
        <div className="page-header-left">本周 AI 简报</div>
        <div className="page-header-right">Weekly Briefing</div>
      </header>
      <main className="page-main">
        <section className="intro">
          <p>每周一更、信息密度高。按生成日期倒序浏览，适合周末或周一花 30–45 分钟读完本周脉络。</p>
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

