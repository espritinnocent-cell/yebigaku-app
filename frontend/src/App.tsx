import { useEffect, useState } from 'react'

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

// JSON文字列を安全に配列に変換するお助け関数
const parseList = (jsonString?: string): string[] => {
  if (!jsonString) return []
  try {
    return JSON.parse(jsonString)
  } catch (e) {
    console.error("データの変換に失敗しました", e)
    return []
  }
}

// ★追加: 音声ファイルのパスをローカル用に変換するお助け関数
// 例: "static/audio/law_日本国憲法_21.mp3" -> "/audio/law_日本国憲法_21.mp3"
const getLocalAudioPath = (originalPath?: string) => {
  if (!originalPath) return undefined;
  const filename = originalPath.split('/').pop();
  return `/audio/${filename}`;
}

function App() {
  const [articles, setArticles] = useState<LawArticle[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // ★変更: APIサーバーではなく、publicフォルダ内の laws.json を直接読み込む
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
      {/* ヘッダー */}
      <header className="bg-blue-700 text-white p-4 shadow-md sticky top-0 z-10 flex justify-between items-center px-6">
        <h1 className="text-xl font-bold tracking-wider">耳学 (Yebigaku)</h1>
        <span className="text-xs bg-blue-800 py-1 px-2 rounded-full">Offline Ready</span>
      </header>

      {/* メインコンテンツ */}
      <main className="p-4 max-w-3xl mx-auto space-y-8 mt-6">
        {articles.length === 0 ? (
          <p className="text-center text-slate-500 bg-white p-8 rounded-2xl shadow-sm">
            条文データが見つかりません。
          </p>
        ) : (
          articles.map((article) => {
            // 文字列データを配列に変換
            const requirements = parseList(article.requirements)
            const effects = parseList(article.effects)
            const mainIssues = parseList(article.main_issues)

            return (
              <article key={article.id} className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                {/* カードヘッダー */}
                <div className="bg-slate-50 p-5 border-b border-slate-200">
                  <h2 className="text-2xl font-extrabold text-blue-900">
                    {article.law_name} 第{article.article_number}条
                  </h2>
                </div>
                
                <div className="p-6">
                  {/* 条文本文 */}
                  <div className="mb-8">
                    <p className="text-slate-700 leading-relaxed font-medium text-lg border-l-4 border-blue-400 pl-4">
                      {article.text}
                    </p>
                  </div>
                  
                  {/* AI解析ブロック */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    {/* 趣旨 */}
                    {article.purpose && (
                      <div className="bg-blue-50/50 p-4 rounded-xl border border-blue-100 md:col-span-2">
                        <h3 className="font-bold text-blue-800 mb-2 flex items-center gap-2">
                          💡 趣旨
                        </h3>
                        <p className="text-sm text-slate-700 leading-relaxed">{article.purpose}</p>
                      </div>
                    )}

                    {/* 要件 */}
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

                    {/* 効果 */}
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

                  {/* 主要論点 */}
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

                  {/* 音声プレイヤー */}
                  {article.audio_file_path && (
                    <div className="mt-6 pt-5 border-t border-slate-100">
                      <h3 className="font-bold text-slate-600 text-sm mb-3">🎧 音声解説を聴く</h3>
                      {/* ★変更: srcをローカルの変換関数に通す */}
                      <audio controls className="w-full h-12 outline-none rounded-full bg-slate-50">
                        <source src={getLocalAudioPath(article.audio_file_path)} type="audio/mpeg" />
                        お使いのブラウザは音声再生に対応していません。
                      </audio>
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