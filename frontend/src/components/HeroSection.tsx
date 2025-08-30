import { motion } from 'framer-motion'
import { ArrowRight, Database, Zap, Code, Globe } from 'lucide-react'
import { useEffect, useState } from 'react'

const floatingIcons = [
  { icon: Database, delay: 0, x: 100, y: 50 },
  { icon: Zap, delay: 0.2, x: -80, y: 80 },
  { icon: Code, delay: 0.4, x: 120, y: -60 },
  { icon: Globe, delay: 0.6, x: -100, y: -40 },
]

export function HeroSection() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({
        x: (e.clientX / window.innerWidth) * 2 - 1,
        y: (e.clientY / window.innerHeight) * 2 - 1,
      })
    }

    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [])

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-radial">
      {/* Background Grid */}
      <div className="absolute inset-0 bg-grid-pattern opacity-20" />
      
      {/* Floating Background Elements */}
      <div className="absolute inset-0">
        {floatingIcons.map((item, index) => (
          <motion.div
            key={index}
            className="absolute"
            initial={{ opacity: 0, scale: 0 }}
            animate={{ 
              opacity: 0.1, 
              scale: 1,
              x: item.x + mousePosition.x * 20,
              y: item.y + mousePosition.y * 20,
            }}
            transition={{ delay: item.delay, duration: 0.8 }}
            style={{
              left: `${50 + (index % 2 === 0 ? 20 : -20)}%`,
              top: `${30 + (index * 15)}%`,
            }}
          >
            <item.icon className="w-24 h-24 text-primary/20" />
          </motion.div>
        ))}
      </div>

      {/* Main Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="space-y-8"
        >
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2, duration: 0.6 }}
            className="inline-flex items-center px-6 py-3 rounded-full glass-morphism text-sm font-medium border border-white/10"
          >
            <span className="text-xs text-muted-foreground mr-2">noun:</span>
            <span className="text-white">a memory layer for AI</span>
          </motion.div>

          {/* Main Heading */}
          <div className="space-y-6">
            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.8 }}
              className="text-5xl sm:text-7xl lg:text-8xl font-bold leading-tight tracking-tight"
            >
              <span className="text-white">Memory Control MCP</span>
            </motion.h1>
            
            <motion.p
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5, duration: 0.8 }}
              className="text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed font-light"
            >
              Universal memory layer for all major AI models. Works seamlessly with 
              OpenAI, Gemini, Claude, Grok, and any LLM that supports context protocols.
            </motion.p>
          </div>

          {/* LLM Logos */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7, duration: 0.8 }}
            className="flex flex-col items-center space-y-4"
          >
            <p className="text-sm text-gray-500 uppercase tracking-wider">
              Compatible with all major AI models
            </p>
            <div className="flex items-center justify-center space-x-8 flex-wrap gap-4">
              {/* OpenAI */}
              <motion.div
                className="flex items-center space-x-2 px-4 py-2 glass-morphism rounded-lg border border-white/5"
                whileHover={{ scale: 1.05, y: -2 }}
                transition={{ duration: 0.2 }}
              >
                <div className="w-6 h-6 bg-white rounded-sm flex items-center justify-center">
                  <span className="text-black font-bold text-xs">AI</span>
                </div>
                <span className="text-gray-300 text-sm font-medium">OpenAI</span>
              </motion.div>

              {/* Gemini */}
              <motion.div
                className="flex items-center space-x-2 px-4 py-2 glass-morphism rounded-lg border border-white/5"
                whileHover={{ scale: 1.05, y: -2 }}
                transition={{ duration: 0.2 }}
              >
                <div className="w-6 h-6 bg-gradient-to-r from-blue-500 to-purple-600 rounded-sm flex items-center justify-center">
                  <span className="text-white font-bold text-xs">G</span>
                </div>
                <span className="text-gray-300 text-sm font-medium">Gemini</span>
              </motion.div>

              {/* Claude */}
              <motion.div
                className="flex items-center space-x-2 px-4 py-2 glass-morphism rounded-lg border border-white/5"
                whileHover={{ scale: 1.05, y: -2 }}
                transition={{ duration: 0.2 }}
              >
                <div className="w-6 h-6 bg-orange-500 rounded-sm flex items-center justify-center">
                  <span className="text-white font-bold text-xs">C</span>
                </div>
                <span className="text-gray-300 text-sm font-medium">Claude</span>
              </motion.div>

              {/* Grok */}
              <motion.div
                className="flex items-center space-x-2 px-4 py-2 glass-morphism rounded-lg border border-white/5"
                whileHover={{ scale: 1.05, y: -2 }}
                transition={{ duration: 0.2 }}
              >
                <div className="w-6 h-6 bg-gray-800 rounded-sm flex items-center justify-center border border-gray-600">
                  <span className="text-white font-bold text-xs">X</span>
                </div>
                <span className="text-gray-300 text-sm font-medium">Grok</span>
              </motion.div>
            </div>
          </motion.div>


        </motion.div>
      </div>

      {/* Scroll Indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5, duration: 0.8 }}
        className="absolute bottom-12 left-1/2 transform -translate-x-1/2"
      >
        <motion.div
          animate={{ y: [0, 8, 0] }}
          transition={{ repeat: Infinity, duration: 2.5, ease: "easeInOut" }}
          className="text-gray-500"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M7 13l5 5 5-5M7 6l5 5 5-5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </motion.div>
      </motion.div>
    </section>
  )
}
