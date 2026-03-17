import { useEffect, useState } from 'react'
import { DailyList } from './DailyList'
import { DailyDetail } from './DailyDetail'
import { dailyList, dailyMap } from './parseDaily'

const getSlugFromHash = (): string | null => {
  const hash = window.location.hash.replace('#', '').trim()
  return hash || null
}

export default function App() {
  const [currentSlug, setCurrentSlug] = useState<string | null>(() =>
    typeof window === 'undefined' ? null : getSlugFromHash()
  )

  useEffect(() => {
    const onHashChange = () => {
      setCurrentSlug(getSlugFromHash())
    }
    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  const handleOpen = (slug: string) => {
    window.location.hash = slug
  }

  const handleBack = () => {
    window.location.hash = ''
  }

  if (currentSlug) {
    const daily = dailyMap[currentSlug]
    if (!daily) {
      return (
        <div className="page">
          <header className="page-header">
            <div className="logo">今日 AI 简报 · Daily Briefing</div>
            <button className="ghost-button" onClick={handleBack}>
              返回列表
            </button>
          </header>
          <main className="page-main">
            <p>未找到对应日期的日报。</p>
          </main>
        </div>
      )
    }
    return <DailyDetail daily={daily} onBack={handleBack} />
  }

  return <DailyList items={dailyList} onOpen={handleOpen} />
}

