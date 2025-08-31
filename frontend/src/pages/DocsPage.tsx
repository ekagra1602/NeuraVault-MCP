import { motion } from 'framer-motion'
import { Book, Code, Zap, Database, ArrowRight } from 'lucide-react'

const docSections = [
  {
    title: 'Quick Start',
    icon: Zap,
    description: 'Get up and running with NeuraVault MCP in under 5 minutes',
    items: [
      'Installation & Setup',
      'Running the Server',
      'First API Call',
      'Basic Configuration'
    ]
  },
  {
    title: 'API Reference',
    icon: Code,
    description: 'Complete documentation for all REST endpoints',
    items: [
      'POST /memory - Store Memory',
      'GET /memory/{user_id} - Retrieve Memories',
      'GET /health - Health Check',
      'Authentication & Headers'
    ]
  },
  {
    title: 'Python SDK',
    icon: Database,
    description: 'Use NeuraVault MCP directly in your Python applications',
    items: [
      'In-Process Usage',
      'Memory Store API',
      'Custom Backends',
      'Advanced Features'
    ]
  },
  {
    title: 'Integration Guide',
    icon: Book,
    description: 'Integrate NeuraVault MCP with popular AI frameworks',
    items: [
      'OpenAI Plugin Setup',
      'LangChain Integration',
      'Custom Middleware',
      'Production Deployment'
    ]
  }
]

export default function DocsPage() {
  return (
    <main className="pt-24 pb-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h1 className="text-4xl sm:text-5xl font-bold mb-6">
            <span className="text-gradient">Documentation</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Everything you need to know about implementing and using the NeuraVault MCP server.
          </p>
        </motion.div>

        {/* Documentation Sections */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
          {docSections.map((section, index) => (
            <motion.div
              key={section.title}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="group cursor-pointer"
            >
              <div className="h-full p-8 glass-morphism rounded-2xl hover:bg-white/10 transition-all duration-300 border border-white/5">
                <div className="flex items-center mb-6">
                  <div className="p-3 rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 mr-4">
                    <section.icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold">{section.title}</h3>
                </div>
                
                <p className="text-muted-foreground mb-6 leading-relaxed">
                  {section.description}
                </p>
                
                <ul className="space-y-2 mb-6">
                  {section.items.map((item, i) => (
                    <li key={i} className="flex items-center text-sm">
                      <ArrowRight className="w-4 h-4 text-primary mr-2 flex-shrink-0" />
                      <span className="text-muted-foreground hover:text-foreground transition-colors">
                        {item}
                      </span>
                    </li>
                  ))}
                </ul>

                <div className="flex items-center text-primary font-medium group-hover:translate-x-1 transition-transform">
                  Read More
                  <ArrowRight className="w-4 h-4 ml-1" />
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Quick Start Section */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-2xl p-8 border border-white/10"
        >
          <h2 className="text-2xl font-bold mb-6 text-center">Quick Start Guide</h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-4">1. Installation</h3>
              <div className="bg-background/50 rounded-lg p-4 font-mono text-sm">
                <div className="text-muted-foreground"># Clone the repository</div>
                <div>git clone https://github.com/ekagra1602/NeuraVault-MCP.git</div>
                <div className="mt-2 text-muted-foreground"># Install dependencies</div>
                <div>pip install -r requirements.txt</div>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">2. Start Server</h3>
              <div className="bg-background/50 rounded-lg p-4 font-mono text-sm">
                <div className="text-muted-foreground"># Run the development server</div>
                <div>uvicorn app.main:app --reload</div>
                <div className="mt-2 text-muted-foreground"># Server runs on http://localhost:8000</div>
              </div>
            </div>
          </div>

          <div className="mt-8 text-center">
            <motion.button
              className="px-8 py-4 bg-primary text-primary-foreground rounded-xl font-semibold hover:bg-primary/90 transition-all"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              View Complete Guide
            </motion.button>
          </div>
        </motion.div>
      </div>
    </main>
  )
}
