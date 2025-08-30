import { motion } from 'framer-motion'
import { useState } from 'react'
import { Copy, Check, Terminal, Code, Globe } from 'lucide-react'

const examples = [
  {
    id: 'multi-llm',
    title: 'Multi-LLM Memory',
    icon: Globe,
    description: 'Share memories across OpenAI, Claude, Gemini, and Grok',
    language: 'bash',
    code: `# Store memory from OpenAI conversation
curl -X POST "http://localhost:8000/memory" \\
  -H "Content-Type: application/json" \\
  -d '{
    "user_id": "alice",
    "llm": "gpt-4o",
    "content": "Alice prefers concise explanations and code examples"
  }'

# Store memory from Claude conversation  
curl -X POST "http://localhost:8000/memory" \\
  -H "Content-Type: application/json" \\
  -d '{
    "user_id": "alice", 
    "llm": "claude-3-opus",
    "content": "Alice is working on a React project with TypeScript"
  }'

# Retrieve all memories for user (cross-model context)
curl "http://localhost:8000/memory/alice"

# Response - memories from all models
[
  {
    "user_id": "alice",
    "llm": "gpt-4o",
    "content": "Alice prefers concise explanations and code examples",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  {
    "user_id": "alice", 
    "llm": "claude-3-opus",
    "content": "Alice is working on a React project with TypeScript",
    "timestamp": "2024-01-15T10:32:00Z"
  }
]`
  },
  {
    id: 'python-api',
    title: 'Cross-Model Python API',
    icon: Code,
    description: 'Manage memories across multiple LLMs in Python',
    language: 'python',
    code: `from app.memory import MemoryItem, memory_store

# Store memories from different LLMs
models = ["gpt-4o", "claude-3-opus", "gemini-pro", "grok-1"]

for model in models:
    memory_store.add(
        MemoryItem(
            user_id="bob",
            llm=model,
            content=f"Bob's preferences learned via {model}"
        )
    )

# Get all memories regardless of source model
all_memories = memory_store.get("bob")
print(f"Total memories from {len(set(m.llm for m in all_memories))} models")

# Search across all models
results = memory_store.search("bob", "preferences")
for result in results:
    print(f"{result.llm}: {result.content}")

# Get memories by specific model
claude_memories = [m for m in all_memories if m.llm == "claude-3-opus"]
print(f"Claude-specific memories: {len(claude_memories)}")`
  },
  {
    id: 'openai-plugin',
    title: 'OpenAI Plugin Setup',
    icon: Terminal,
    description: 'Configure as a ChatGPT plugin for automatic memory management',
    language: 'json',
    code: `{
  "schema_version": "v1",
  "name_for_model": "mcp_memory",
  "name_for_human": "Memory Storage",
  "description_for_model": "Store and retrieve user context and memories",
  "description_for_human": "Persistent memory for AI conversations",
  "auth": {
    "type": "none"
  },
  "api": {
    "type": "openapi",
    "url": "http://localhost:8000/openapi.json"
  },
  "logo_url": "http://localhost:8000/logo.png",
  "contact_email": "support@mcp.dev",
  "legal_info_url": "http://localhost:8000/legal"
}`
  }
]

export function CodeExamples() {
  const [activeTab, setActiveTab] = useState(examples[0].id)
  const [copiedStates, setCopiedStates] = useState<Record<string, boolean>>({})

  const activeExample = examples.find(ex => ex.id === activeTab) || examples[0]

  const copyToClipboard = async (text: string, id: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedStates(prev => ({ ...prev, [id]: true }))
      setTimeout(() => {
        setCopiedStates(prev => ({ ...prev, [id]: false }))
      }, 2000)
    } catch (err) {
      console.error('Failed to copy text: ', err)
    }
  }

  return (
    <section className="py-24 bg-muted/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold mb-6">
            <span className="text-white">Universal Memory Layer</span>
            <br />
            <span className="text-gray-400 text-3xl font-light">for All AI Models</span>
          </h2>
          <p className="text-lg text-gray-400 max-w-3xl mx-auto">
            One API to connect OpenAI, Claude, Gemini, Grok, and any future LLM. 
            Share context seamlessly across all your AI conversations.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Tabs */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="lg:col-span-3"
          >
            <div className="space-y-2">
              {examples.map((example) => (
                <button
                  key={example.id}
                  onClick={() => setActiveTab(example.id)}
                  className={`w-full text-left p-4 rounded-lg transition-all ${
                    activeTab === example.id
                      ? 'bg-primary/10 border border-primary/20 text-primary'
                      : 'glass-morphism hover:bg-white/5 text-muted-foreground hover:text-foreground'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <example.icon className="w-5 h-5" />
                    <div>
                      <div className="font-medium">{example.title}</div>
                      <div className="text-sm opacity-75">{example.description}</div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </motion.div>

          {/* Code Block */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="lg:col-span-9"
          >
            <div className="glass-morphism rounded-xl border border-white/10 overflow-hidden">
              {/* Header */}
              <div className="flex items-center justify-between p-4 border-b border-white/10">
                <div className="flex items-center space-x-3">
                  <activeExample.icon className="w-5 h-5 text-primary" />
                  <div>
                    <h3 className="font-medium">{activeExample.title}</h3>
                    <p className="text-sm text-muted-foreground">{activeExample.description}</p>
                  </div>
                </div>
                <button
                  onClick={() => copyToClipboard(activeExample.code, activeExample.id)}
                  className="p-2 rounded-lg hover:bg-white/10 transition-colors"
                >
                  {copiedStates[activeExample.id] ? (
                    <Check className="w-4 h-4 text-green-500" />
                  ) : (
                    <Copy className="w-4 h-4" />
                  )}
                </button>
              </div>

              {/* Code */}
              <div className="p-6">
                <pre className="text-sm leading-relaxed overflow-x-auto">
                  <code className="font-mono text-muted-foreground">
                    {activeExample.code}
                  </code>
                </pre>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Quick Start CTA */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center mt-16"
        >
          <div className="inline-flex flex-col sm:flex-row gap-4">
            <motion.button
              className="px-8 py-4 bg-primary text-primary-foreground rounded-xl font-semibold hover:bg-primary/90 transition-all"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Start Building Now
            </motion.button>
            <motion.button
              className="px-8 py-4 glass-morphism hover:bg-white/10 rounded-xl font-semibold transition-all"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              View Full Documentation
            </motion.button>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
