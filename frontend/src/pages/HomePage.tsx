import { HeroSection } from '@/components/HeroSection'
import { FeaturesSection } from '@/components/FeaturesSection'
import { CodeExamples } from '@/components/CodeExamples'

export default function HomePage() {
  return (
    <main className="pt-16">
      <HeroSection />
      <FeaturesSection />
      <CodeExamples />
    </main>
  )
}
