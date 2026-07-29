import { useEffect, useState, useRef } from 'react'

interface LawArticle {
  id: number
  law_name: string
  article_number: string
  text: string
  purpose?: string
  requirements?: string
  effects?: string
  main_issues?: string
  audio_file_path?: string
}

const parseList = (jsonString?: string): string[] => {
  if (!jsonString) return []
  try {
    return JSON.parse(jsonString)
  } catch (e) {
    console.error("データの変換に失敗しました", e)
    return []
  }
}

const getLocalAudioPath = (originalPath?: string) => {
  if (!originalPath) return undefined;
  const filename = originalPath.split('/').pop();
  return `/audio/${filename}`;
}

function App() {
  const [articles, setArticles] = useState<LawArticle[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  const [playingId, setPlayingId] = useState<number | null>(null)
  const audioRef = useRef<HTMLAudioElement | null>(null)

  useEffect(() => {
    if (!audioRef.current) {
      audioRef.current = new Audio()
    }
    const audio = audioRef.current

    const onEnded = () => setPlayingId(null)
    const onPause = () => setPlayingId(null)
    const onPlay = () => {}

    audio.addEventListener('ended', onEnded)
    audio.addEventListener('pause', onPause)
    audio.addEventListener('play', onPlay)

    if ('mediaSession' in navigator) {
      navigator.mediaSession.setActionHandler('play', () => {
        audio.play().catch(e => console.error(e))
      })
      navigator.mediaSession.setActionHandler('pause', () => {
        audio.pause()
      })
    }

    return () => {
      audio.removeEventListener('ended', onEnded)
      audio.removeEventListener('pause', onPause)
      audio.removeEventListener('play', onPlay)
    }
  }, [])

  // ★修正: Linterの警告に従い、ロック画面の表示更新を useEffect に分離しました
  useEffect(() => {
    if (playingId !== null && 'mediaSession' in navigator) {
      const currentArticle = articles.find(a => a.id === playingId)
      if (currentArticle) {
        navigator.mediaSession.metadata = new MediaMetadata({
          title: `${currentArticle.law_name} 第${currentArticle.article_number}条`,
          artist: '耳学 (Yebigaku)',
          album: '法律音声学習',
        })
      }
    }
  }, [playingId, articles])

  const togglePlay = (article: LawArticle) => {
    const audio = audioRef.current
    if (!audio) return

    const path = getLocalAudioPath(article.audio_file_path)
    if (!path) return

    if (playingId === article.id) {
      audio.pause()
      setPlayingId(null)
      return
    }

    if (!audio.src.endsWith(path)) {
      audio.src = path
    }

    audio.play().then(() => {
      setPlayingId(article.id)
    }).catch(err => {
      console.error("音声の再生に失敗しました:", err)
    })
  }

  useEffect(() => {
    fetch('/laws.json') 
      .then(res => {
        if (!res.ok) throw new Error("laws.json の読み込みに失敗しました");
        return res.json();
      })
      .then(data => {
        if (!Array.isArray(data)) {
           throw new Error("データ形式が正しくありません。配列である必要があります。");
        }
        setArticles(data)
        setLoading(false)
      })
      .catch(err => {
        console.error("データの取得に失敗しました", err)
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen bg-slate-50 text-slate-500">
        <p className="animate-pulse font-bold text-lg">データを読み込み中...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-screen bg-slate-50 text-red-500">
        <p className="font-bold text-lg">エラー: {error}</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-100 text-slate-800 font-sans pb-12">
      <header className="bg-blue-700 text-white p-4 shadow-md sticky top-0 z-10 flex justify-between items-center px-6">
        <h1 className="text-xl font-bold tracking-wider">耳学 (Yebigaku)</h1>
        <span className="text-xs bg-blue-800 py-1 px-2 rounded-full">Offline Ready</span>
      </header>

      <main className="p-4 max-w-3xl mx-auto space-y-8 mt-6">
        {articles.length === 0 ? (
          <p className="text-center text-slate-500 bg-white p-8 rounded-2xl shadow-sm">
            条文データが見つかりません。
          </p>
        ) : (
          articles.map((article) => {
            const requirements = parseList(article.requirements)
            const effects = parseList(article.effects)
            const mainIssues = parseList(article.main_issues)

            return (
              <article key={article.id} className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                <div className="bg-slate-50 p-5 border-b border-slate-200">
                  <h2 className="text-2xl font-extrabold text-blue-900">
                    {article.law_name} 第{article.article_number}条
                  </h2>
                </div>
                
                <div className="p-6">
                  <div className="mb-8">
                    <p className="text-slate-700 leading-relaxed font-medium text-lg border-l-4 border-blue-400 pl-4">
                      {article.text}
                    </p>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    {article.purpose && (
                      <div className="bg-blue-50/50 p-4 rounded-xl border border-blue-100 md:col-span-2">
                        <h3 className="font-bold text-blue-800 mb-2 flex items-center gap-2">
                          💡 趣旨
                        </h3>
                        <p className="text-sm text-slate-700 leading-relaxed">{article.purpose}</p>
                      </div>
                    )}

                    {requirements.length > 0 && (
                      <div className="bg-emerald-50/50 p-4 rounded-xl border border-emerald-100">
                        <h3 className="font-bold text-emerald-800 mb-2 flex items-center gap-2">
                          📋 要件
                        </h3>
                        <ul className="list-disc list-inside text-sm text-slate-700 space-y-1">
                          {requirements.map((req, i) => <li key={i}>{req}</li>)}
                        </ul>
                      </div>
                    )}

                    {effects.length > 0 && (
                      <div className="bg-orange-50/50 p-4 rounded-xl border border-orange-100">
                        <h3 className="font-bold text-orange-800 mb-2 flex items-center gap-2">
                          🎯 効果
                        </h3>
                        <ul className="list-disc list-inside text-sm text-slate-700 space-y-1">
                          {effects.map((eff, i) => <li key={i}>{eff}</li>)}
                        </ul>
                      </div>
                    )}
                  </div>

                  {mainIssues.length > 0 && (
                    <div className="bg-purple-50/50 p-4 rounded-xl border border-purple-100 mb-6">
                      <h3 className="font-bold text-purple-800 mb-2 flex items-center gap-2">
                        ⚖️ 主要論点
                      </h3>
                      <ul className="list-disc list-inside text-sm text-slate-700 space-y-1">
                        {mainIssues.map((issue, i) => <li key={i}>{issue}</li>)}
                      </ul>
                    </div>
                  )}

                  {article.audio_file_path && (
                    <div className="mt-6 pt-5 border-t border-slate-100 flex items-center justify-between">
                      <h3 className="font-bold text-slate-600 text-sm">🎧 音声解説を聴く</h3>
                      <button
                        onClick={() => togglePlay(article)}
                        className={`px-6 py-2 rounded-full font-bold text-white transition-colors shadow-sm ${
                          playingId === article.id 
                            ? 'bg-orange-500 hover:bg-orange-600' 
                            : 'bg-blue-600 hover:bg-blue-700'
                        }`}
                      >
                        {playingId === article.id ? '⏸ 一時停止' : '▶️ 再生する'}
                      </button>
                    </div>
                  )}
                </div>
              </article>
            )
          })
        )}
      </main>
    </div>
  )
}

export default App