export interface DailyMeta {
  date: string
  slug: string
  title: string
  description: string
}

export interface DailyItem {
  id: string
  title: string
  paragraphs: string[]
  link?: string
  source?: string
}

export interface DailySection {
  id: string
  title: string
  items: DailyItem[]
}

export interface DailyFull extends DailyMeta {
  sections: DailySection[]
}

