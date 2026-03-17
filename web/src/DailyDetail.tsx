import type { DailyFull, DailyItem, DailySection } from './types'

interface Props {
  daily: DailyFull
  onBack: () => void
}

function ItemBlock({ item }: { item: DailyItem }) {
  return (
    <article className="item-block">
      <h3 className="item-title">{item.title}</h3>
      {item.paragraphs.map((p, idx) => {
        const [rawLabel, rest] = p.split('：', 2)
        const labelCore = rawLabel?.trim() ?? ''
        // 去掉 Markdown 粗体符号 **背景** / *背景*
        const cleanedLabel = labelCore.replace(/^\*+/, '').replace(/\*+$/, '')
        const hasLabel = rest !== undefined && cleanedLabel.length > 0 && cleanedLabel.length <= 20

        if (!hasLabel) {
          return (
            <p key={idx} className="item-paragraph">
              {p}
            </p>
          )
        }

        return (
          <div key={idx} className="item-paragraph-block">
            <div className="item-label-row">
              <span className="item-label-line-short" />
              <span className="item-label">{cleanedLabel}</span>
              <span className="item-label-rule" />
            </div>
            <p className="item-paragraph">{rest}</p>
          </div>
        )
      })}
      {item.link && (
        <p className="item-link">
          <a href={item.link} target="_blank" rel="noreferrer">
            原文链接
          </a>
          {item.source && <span className="item-source">（来源：{item.source}）</span>}
        </p>
      )}
    </article>
  )
}

function Section({ section }: { section: DailySection }) {
  if (!section.items.length) return null

  const renderSectionIcon = (id: string) => {
    if (id === 'products') {
      // 网格 / 应用
      return (
        <span className="section-icon">
          <svg viewBox="0 0 16 16" aria-hidden="true">
            <rect x="2" y="2" width="4" height="4" rx="1" />
            <rect x="10" y="2" width="4" height="4" rx="1" />
            <rect x="2" y="10" width="4" height="4" rx="1" />
            <rect x="10" y="10" width="4" height="4" rx="1" />
          </svg>
        </span>
      )
    }
    if (id === 'models') {
      // 网络 / 图节点
      return (
        <span className="section-icon">
          <svg viewBox="0 0 16 16" aria-hidden="true">
            <circle cx="4" cy="8" r="2" />
            <circle cx="12" cy="4" r="2" />
            <circle cx="12" cy="12" r="2" />
            <path d="M5.6 7.2 10.4 4.8M5.6 8.8l4.8 2.4" />
          </svg>
        </span>
      )
    }
    // events
    return (
      <span className="section-icon">
        <svg viewBox="0 0 16 16" aria-hidden="true">
          <path d="M8 1.5 3.5 9h3v5.5L12.5 7h-3z" />
        </svg>
      </span>
    )
  }

  return (
    <section className="section">
      <div className="section-title-row">
        {renderSectionIcon(section.id)}
        <h2 className="section-title">{section.title}</h2>
      </div>
      <div className="section-divider" />
      <div className={`section-items section-items-${section.id}`}>
        {section.items.map((item) => (
          <ItemBlock key={item.id} item={item} />
        ))}
      </div>
    </section>
  )
}

export function DailyDetail({ daily, onBack }: Props) {
  return (
    <div className="page">
      <header className="page-header">
        <div className="logo">今日 AI 简报 · Daily Briefing</div>
        <button type="button" className="ghost-button" onClick={onBack}>
          返回列表
        </button>
      </header>

      <main className="page-main">
        <article className="detail">
          <header className="detail-header">
            <div className="detail-date">{daily.date}</div>
            <p className="detail-description">{daily.description}</p>
          </header>

          {daily.sections.map((section) => (
            <Section key={section.id} section={section} />
          ))}
        </article>
      </main>
    </div>
  )
}

