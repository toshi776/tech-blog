"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import {
  ArrowRight,
  Search,
  Stethoscope,
  Rocket,
  Heart,
  TrendingUp,
  Clock,
  DollarSign,
  ChevronLeft,
  ChevronRight,
  Mail,
  Phone,
  MapPin,
  Twitter,
  Linkedin,
  Github,
} from "lucide-react"

// Counter animation hook
function useCounter(end: number, duration = 2000) {
  const [count, setCount] = useState(0)
  const [hasStarted, setHasStarted] = useState(false)

  useEffect(() => {
    if (!hasStarted) return

    let startTime: number
    const animate = (currentTime: number) => {
      if (!startTime) startTime = currentTime
      const progress = Math.min((currentTime - startTime) / duration, 1)
      setCount(Math.floor(progress * end))

      if (progress < 1) {
        requestAnimationFrame(animate)
      }
    }

    requestAnimationFrame(animate)
  }, [end, duration, hasStarted])

  return { count, startCounter: () => setHasStarted(true) }
}

// Testimonial slider component
function TestimonialSlider() {
  const [currentIndex, setCurrentIndex] = useState(0)

  const testimonials = [
    {
      quote: "DX診断により業務効率が大幅に改善されました。特に障がい者雇用の環境整備で大きな成果を得られました。",
      author: "田中様",
      company: "地域製造業A社",
      logo: "/placeholder.svg?height=40&width=120",
    },
    {
      quote: "AI導入により売上が15%向上。地方企業でもここまでできるとは思いませんでした。",
      author: "佐藤様",
      company: "小売業B社",
      logo: "/placeholder.svg?height=40&width=120",
    },
    {
      quote: "親身になって相談に乗っていただき、実践的なソリューションを提供してくれました。",
      author: "鈴木様",
      company: "サービス業C社",
      logo: "/placeholder.svg?height=40&width=120",
    },
  ]

  const nextTestimonial = () => {
    setCurrentIndex((prev) => (prev + 1) % testimonials.length)
  }

  const prevTestimonial = () => {
    setCurrentIndex((prev) => (prev - 1 + testimonials.length) % testimonials.length)
  }

  useEffect(() => {
    const interval = setInterval(nextTestimonial, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="relative bg-gray-50 p-8 rounded-lg">
      <div className="text-center">
        <blockquote className="text-lg text-gray-700 mb-4">"{testimonials[currentIndex].quote}"</blockquote>
        <div className="flex items-center justify-center gap-4">
          <img
            src={testimonials[currentIndex].logo || "/placeholder.svg"}
            alt={`${testimonials[currentIndex].company}のロゴ`}
            className="h-8"
          />
          <div>
            <cite className="font-semibold text-gray-900">{testimonials[currentIndex].author}</cite>
            <p className="text-sm text-gray-600">{testimonials[currentIndex].company}</p>
          </div>
        </div>
      </div>

      <div className="flex justify-center gap-2 mt-6">
        {testimonials.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentIndex(index)}
            className={`w-2 h-2 rounded-full transition-colors ${
              index === currentIndex ? "bg-indigo-600" : "bg-gray-300"
            }`}
            aria-label={`証言 ${index + 1}を表示`}
          />
        ))}
      </div>

      <button
        onClick={prevTestimonial}
        className="absolute left-2 top-1/2 -translate-y-1/2 p-2 rounded-full bg-white shadow-md hover:shadow-lg transition-shadow"
        aria-label="前の証言"
      >
        <ChevronLeft className="w-4 h-4" />
      </button>

      <button
        onClick={nextTestimonial}
        className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full bg-white shadow-md hover:shadow-lg transition-shadow"
        aria-label="次の証言"
      >
        <ChevronRight className="w-4 h-4" />
      </button>
    </div>
  )
}

// Impact metrics component with intersection observer
function ImpactMetrics() {
  const [isVisible, setIsVisible] = useState(false)
  const overtimeCounter = useCounter(30, 2000)
  const revenueCounter = useCounter(15, 2000)
  const costCounter = useCounter(40, 2000)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !isVisible) {
          setIsVisible(true)
          overtimeCounter.startCounter()
          revenueCounter.startCounter()
          costCounter.startCounter()
        }
      },
      { threshold: 0.5 },
    )

    const element = document.getElementById("impact-metrics")
    if (element) observer.observe(element)

    return () => observer.disconnect()
  }, [isVisible, overtimeCounter, revenueCounter, costCounter])

  return (
    <div id="impact-metrics" className="grid md:grid-cols-3 gap-8">
      <div className="text-center">
        <div className="flex items-center justify-center w-16 h-16 bg-indigo-100 rounded-full mx-auto mb-4">
          <Clock className="w-8 h-8 text-indigo-600" />
        </div>
        <div className="text-3xl font-bold text-indigo-600 mb-2">-{overtimeCounter.count}%</div>
        <p className="text-gray-600">残業時間削減</p>
      </div>

      <div className="text-center">
        <div className="flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mx-auto mb-4">
          <TrendingUp className="w-8 h-8 text-green-600" />
        </div>
        <div className="text-3xl font-bold text-green-600 mb-2">+{revenueCounter.count}%</div>
        <p className="text-gray-600">売上向上</p>
      </div>

      <div className="text-center">
        <div className="flex items-center justify-center w-16 h-16 bg-orange-100 rounded-full mx-auto mb-4">
          <DollarSign className="w-8 h-8 text-orange-600" />
        </div>
        <div className="text-3xl font-bold text-orange-600 mb-2">-{costCounter.count}%</div>
        <p className="text-gray-600">作業コスト削減</p>
      </div>
    </div>
  )
}

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-indigo-50 to-white py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center max-w-4xl mx-auto">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              AI と DX で、
              <br />
              地域の未来をひらく
            </h1>
            <p className="text-xl text-gray-600 mb-8 leading-relaxed">
              One-on-one consulting that blends technology expertise with lived experience.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3">
                無料診断を予約
                <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
              <Button
                variant="outline"
                size="lg"
                className="border-indigo-600 text-indigo-600 hover:bg-indigo-50 px-8 py-3 bg-transparent"
              >
                実績を見る
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Founder Story Section */}
      <section className="py-20 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <img
                src="/placeholder.svg?height=400&width=400"
                alt="代表者の写真"
                className="rounded-lg shadow-lg w-full max-w-md mx-auto"
              />
            </div>
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">代表者について</h2>
              <div className="space-y-4 text-gray-600">
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-indigo-600 rounded-full mt-2 flex-shrink-0"></div>
                  <p>20年以上のIT・AI エンジニア経験</p>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-indigo-600 rounded-full mt-2 flex-shrink-0"></div>
                  <p>双極性障害と共に生きる当事者として、多様性と包摂性を重視</p>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-indigo-600 rounded-full mt-2 flex-shrink-0"></div>
                  <p>地方創生と中小企業支援に情熱を注ぐ、目的主導型のコンサルタント</p>
                </div>
              </div>
              <p className="mt-6 text-gray-700 leading-relaxed">
                技術的専門知識と実体験に基づく共感力を組み合わせ、
                お客様一人ひとりに寄り添ったコンサルティングを提供します。
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-20 px-4 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">サービス内容</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              地域企業の課題に合わせた、実践的なDX・AI導入支援を提供します
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
                  <Search className="w-6 h-6 text-indigo-600" />
                </div>
                <CardTitle>DX 診断 & ロードマップ</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-600">
                  現状分析から始まり、具体的な改善計画まで。 お客様の業務プロセスを詳細に診断し、
                  実現可能なDXロードマップを策定します。
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                  <Rocket className="w-6 h-6 text-green-600" />
                </div>
                <CardTitle>AI PoC & 自動化</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-600">
                  小規模から始められるAI導入支援。 概念実証（PoC）を通じて効果を確認し、 段階的な自動化を実現します。
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                  <Heart className="w-6 h-6 text-purple-600" />
                </div>
                <CardTitle>障がい者支援テクノロジー</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-600">
                  インクルーシブな職場環境の構築支援。 障がい者の方々が活躍できる テクノロジー活用方法をご提案します。
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Impact Metrics Section */}
      <section className="py-20 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">実績・成果</h2>
            <p className="text-gray-600">お客様企業での具体的な改善実績</p>
          </div>

          <ImpactMetrics />
        </div>
      </section>

      {/* Process Timeline Section */}
      <section className="py-20 px-4 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">コンサルティングプロセス</h2>
            <p className="text-gray-600">4つのステップで確実な成果を実現</p>
          </div>

          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <Search className="w-8 h-8 text-white" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Discover</h3>
              <p className="text-sm text-gray-600">現状把握・課題発見</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <Stethoscope className="w-8 h-8 text-white" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Diagnose</h3>
              <p className="text-sm text-gray-600">詳細分析・解決策立案</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <Rocket className="w-8 h-8 text-white" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Deploy</h3>
              <p className="text-sm text-gray-600">実装・導入支援</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <Heart className="w-8 h-8 text-white" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Delight</h3>
              <p className="text-sm text-gray-600">成果確認・継続改善</p>
            </div>
          </div>
        </div>
      </section>

      {/* Case Studies Section */}
      <section className="py-20 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">導入事例</h2>
            <p className="text-gray-600">実際のプロジェクト成果をご紹介</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex gap-2 mb-2">
                  <Badge variant="secondary">製造業</Badge>
                  <Badge variant="outline">AI導入</Badge>
                </div>
                <CardTitle>品質管理AI導入プロジェクト</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-600 mb-4">
                  画像認識AIを活用した品質検査の自動化により、 検査時間を60%短縮し、検査精度も向上。
                </CardDescription>
                <div className="flex gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-indigo-600">60%</div>
                    <div className="text-xs text-gray-500">時間短縮</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">95%</div>
                    <div className="text-xs text-gray-500">精度向上</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex gap-2 mb-2">
                  <Badge variant="secondary">小売業</Badge>
                  <Badge variant="outline">DX推進</Badge>
                </div>
                <CardTitle>在庫管理システム刷新</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-600 mb-4">
                  クラウドベースの在庫管理システム導入により、 在庫回転率が改善し、売上機会損失を削減。
                </CardDescription>
                <div className="flex gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-indigo-600">25%</div>
                    <div className="text-xs text-gray-500">回転率向上</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">15%</div>
                    <div className="text-xs text-gray-500">売上向上</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 px-4 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">お客様の声</h2>
            <p className="text-gray-600">実際にご利用いただいたお客様からの評価</p>
          </div>

          <TestimonialSlider />
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">よくあるご質問</h2>
            <p className="text-gray-600">お客様からよくいただくご質問にお答えします</p>
          </div>

          <Accordion type="single" collapsible className="space-y-4">
            <AccordionItem value="item-1" className="border rounded-lg px-6">
              <AccordionTrigger className="text-left">小規模企業でもAI導入は可能ですか？</AccordionTrigger>
              <AccordionContent className="text-gray-600">
                はい、可能です。お客様の規模や予算に合わせて、 段階的な導入プランをご提案します。
                まずは小さなPoC（概念実証）から始めて、 効果を確認しながら拡大していくアプローチを取ります。
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-2" className="border rounded-lg px-6">
              <AccordionTrigger className="text-left">コンサルティング期間はどのくらいですか？</AccordionTrigger>
              <AccordionContent className="text-gray-600">
                プロジェクトの規模により異なりますが、 診断フェーズは通常2-4週間、 実装支援は3-6ヶ月程度が目安です。
                お客様のご都合に合わせて柔軟に調整いたします。
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-3" className="border rounded-lg px-6">
              <AccordionTrigger className="text-left">障がい者雇用支援について詳しく教えてください</AccordionTrigger>
              <AccordionContent className="text-gray-600">
                当事者の視点から、実践的な支援テクノロジーの導入をサポートします。
                アクセシビリティ向上、業務支援ツールの選定・カスタマイズ、 インクルーシブな職場環境の構築まで、
                総合的にご支援いたします。
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-4" className="border rounded-lg px-6">
              <AccordionTrigger className="text-left">料金体系について教えてください</AccordionTrigger>
              <AccordionContent className="text-gray-600">
                初回診断は無料で実施いたします。 その後のコンサルティングは、プロジェクトベースまたは
                月額顧問契約からお選びいただけます。 詳細は個別にご相談させていただきます。
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </section>

      {/* CTA Banner Section */}
      <section className="py-20 px-4 bg-indigo-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-white mb-4">地方創生・中小企業 DX の第一歩を、一緒に</h2>
          <p className="text-indigo-100 mb-8 text-lg">まずは無料相談で、あなたの課題をお聞かせください</p>
          <Button size="lg" className="bg-white text-indigo-600 hover:bg-gray-100 px-8 py-3">
            30分無料相談
            <ArrowRight className="ml-2 w-4 h-4" />
          </Button>
        </div>
      </section>

      {/* Contact Form Section */}
      <section className="py-20 px-4 bg-gray-50">
        <div className="max-w-2xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">お問い合わせ</h2>
            <p className="text-gray-600">ご質問やご相談がございましたら、お気軽にお問い合わせください</p>
          </div>

          <Card>
            <CardContent className="p-8">
              <form action="" className="space-y-6">
                <div>
                  <Label htmlFor="name">お名前 *</Label>
                  <Input id="name" name="name" required className="mt-2" placeholder="山田太郎" />
                </div>

                <div>
                  <Label htmlFor="email">メールアドレス *</Label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    required
                    className="mt-2"
                    placeholder="example@company.com"
                  />
                </div>

                <div>
                  <Label htmlFor="message">メッセージ *</Label>
                  <Textarea
                    id="message"
                    name="message"
                    required
                    className="mt-2 min-h-[120px]"
                    placeholder="ご相談内容やご質問をお書きください"
                  />
                </div>

                <Button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-700">
                  送信する
                  <ArrowRight className="ml-2 w-4 h-4" />
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-bold text-lg mb-4">Solo AIDX Consulting</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                AI と DX で地域の未来をひらく、 一人ひとりに寄り添うコンサルティング
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-4">サービス</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    DX診断
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    AI導入支援
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    障がい者支援
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    コンサルティング
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">会社情報</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    代表者について
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    実績・事例
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    お客様の声
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    よくある質問
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">お問い合わせ</h4>
              <div className="space-y-3 text-sm text-gray-400">
                <div className="flex items-center gap-2">
                  <Mail className="w-4 h-4" />
                  <span>info@solo-aidx.com</span>
                </div>
                <div className="flex items-center gap-2">
                  <Phone className="w-4 h-4" />
                  <span>03-1234-5678</span>
                </div>
                <div className="flex items-center gap-2">
                  <MapPin className="w-4 h-4" />
                  <span>東京都渋谷区</span>
                </div>
              </div>

              <div className="flex gap-4 mt-6">
                <a href="#" className="text-gray-400 hover:text-white transition-colors" aria-label="Twitter">
                  <Twitter className="w-5 h-5" />
                </a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors" aria-label="LinkedIn">
                  <Linkedin className="w-5 h-5" />
                </a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors" aria-label="GitHub">
                  <Github className="w-5 h-5" />
                </a>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-sm text-gray-400">
            <p>&copy; 2024 Solo AIDX Consulting. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
