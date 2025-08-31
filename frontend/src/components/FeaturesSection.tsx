import { motion } from 'framer-motion'
import { 
  Database, 
  Zap, 
  Code, 
  Globe, 
  Shield, 
  ArrowRight,
  CheckCircle,
  Cpu,
  Clock
} from 'lucide-react'

const features = [
  {
    icon: Globe,
    title: 'Multi-LLM Support',
    description: 'Works seamlessly with OpenAI, Gemini, Claude, Grok, and any LLM that supports context protocols.',
    features: ['Universal compatibility', 'Automatic model detection', 'Cross-platform memory'],
    color: 'from-blue-500 to-cyan-500'
  },
  {
    icon: Database,
    title: 'Persistent Memory',
    description: 'Store and retrieve context data across sessions with efficient memory management.',
    features: ['Cross-session persistence', 'Fast retrieval', 'Automatic timestamping'],
    color: 'from-emerald-500 to-teal-500'
  },
  {
    icon: Zap,
    title: 'Lightning Fast API',
    description: 'Built with FastAPI for high-performance REST operations and real-time context sharing.',
    features: ['Sub-50ms response times', 'Real-time sync', 'Auto-generated docs'],
    color: 'from-yellow-500 to-orange-500'
  },
  {
    icon: Code,
    title: 'Universal Integration',
    description: 'Drop-in support for ChatGPT plugins, API calls, and direct Python integration.',
    features: ['Plugin manifest included', 'REST API', 'Python SDK'],
    color: 'from-purple-500 to-pink-500'
  },
  {
    icon: Shield,
    title: 'Production Ready',
    description: 'Enterprise-grade reliability with robust error handling and monitoring.',
    features: ['Input validation', 'Health monitoring', 'Error recovery'],
    color: 'from-red-500 to-rose-500'
  },
  {
    icon: Cpu,
    title: 'Model Context Protocol',
    description: 'Standards-compliant implementation of NeuraVault MCP for seamless AI tool integration.',
    features: ['NeuraVault MCP standard', 'Tool discovery', 'Context sharing'],
    color: 'from-indigo-500 to-blue-500'
  }
]

const useCases = [
  {
    title: 'Cross-Model Memory',
    description: 'Share conversation context between OpenAI, Claude, Gemini, and Grok seamlessly.',
    icon: '🔄'
  },
  {
    title: 'Multi-Platform AI',
    description: 'Build AI applications that work consistently across all major LLM providers.',
    icon: '🌐'
  },
  {
    title: 'Persistent Context',
    description: 'Maintain long-term memory and context across sessions and model switches.',
    icon: '🧠'
  },
  {
    title: 'Universal Integration',
    description: 'One API to rule them all - integrate with any LLM through standardized protocols.',
    icon: '⚡'
  }
]

export function FeaturesSection() {
  return (
    <section id="features" className="py-24 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center mb-20"
        >
          <h2 className="text-3xl sm:text-4xl font-light mb-6 text-white">
            Upload, Store, Retrieve
            <br />
            <span className="text-gray-400">Develop</span>
          </h2>
          <p className="text-sm text-gray-500 max-w-2xl mx-auto uppercase tracking-wider">
            A Variety Of Tools At Your Disposal
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8 mb-24">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="group"
            >
              <div className="h-full p-8 glass-morphism rounded-xl hover:bg-white/[0.03] transition-all duration-300 border border-white/[0.06] group cursor-pointer">
                <div className="mb-6">
                  <feature.icon className="w-8 h-8 text-gray-400 mb-4" />
                  <h3 className="text-lg font-medium text-white">{feature.title}</h3>
                </div>
                
                <p className="text-gray-400 text-sm leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Use Cases */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h3 className="text-3xl font-bold mb-6 text-gradient-secondary">
            Perfect for Any AI Use Case
          </h3>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            From simple chatbots to complex multi-agent systems, NeuraVault MCP provides the memory layer your AI needs.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {useCases.map((useCase, index) => (
            <motion.div
              key={useCase.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="text-center p-6 glass-morphism rounded-xl hover:bg-white/5 transition-all"
            >
              <div className="text-4xl mb-4">{useCase.icon}</div>
              <h4 className="font-semibold mb-2">{useCase.title}</h4>
              <p className="text-sm text-muted-foreground">{useCase.description}</p>
            </motion.div>
          ))}
        </div>

        {/* Performance Stats */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-2xl p-8 border border-white/10"
        >
          <div className="text-center mb-8">
            <h3 className="text-2xl font-bold mb-4">Built for Performance</h3>
            <p className="text-muted-foreground">Optimized for speed and reliability in production environments</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {[
              { icon: Clock, label: 'Response Time', value: '<50ms', description: 'Average API response' },
              { icon: Database, label: 'Memory Ops', value: '10K+/sec', description: 'Memory operations per second' },
              { icon: Zap, label: 'Uptime', value: '99.9%', description: 'Production uptime SLA' },
              { icon: Code, label: 'Dependencies', value: 'Minimal', description: 'FastAPI + Pydantic only' },
            ].map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="text-center"
              >
                <stat.icon className="w-8 h-8 text-primary mx-auto mb-3" />
                <div className="text-2xl font-bold text-gradient mb-1">{stat.value}</div>
                <div className="font-medium mb-1">{stat.label}</div>
                <div className="text-sm text-muted-foreground">{stat.description}</div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}
