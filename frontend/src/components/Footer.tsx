import { motion } from 'framer-motion'
import { GitBranch, Heart } from 'lucide-react'

export function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="border-t border-border bg-background/80 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center">
                <img src="./memora-circuit.svg" alt="NeuraVault MCP" className="w-8 h-8 rounded-lg" />
              </div>
              <div className="flex flex-col">
                <span className="text-lg font-bold text-gradient">NeuraVault MCP</span>
                <span className="text-xs text-muted-foreground -mt-1">Universal Memory Layer</span>
              </div>
            </div>
            <p className="text-sm text-muted-foreground">
              A powerful FastAPI server that provides persistent memory for LLM-powered applications.
            </p>
          </div>

          {/* Product */}
          <div>
            <h3 className="font-semibold mb-4">Product</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <a href="#features" className="hover:text-primary transition-colors">
                  Features
                </a>
              </li>
              <li>
                <a href="/docs" className="hover:text-primary transition-colors">
                  Documentation
                </a>
              </li>
              <li>
                <a href="/docs#api" className="hover:text-primary transition-colors">
                  API Reference
                </a>
              </li>
              <li>
                <a href="/docs#examples" className="hover:text-primary transition-colors">
                  Examples
                </a>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="font-semibold mb-4">Resources</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <a href="/docs#quickstart" className="hover:text-primary transition-colors">
                  Quick Start
                </a>
              </li>
              <li>
                <a href="/docs#integration" className="hover:text-primary transition-colors">
                  Integration Guide
                </a>
              </li>
              <li>
                <a href="https://github.com" className="hover:text-primary transition-colors">
                  GitHub
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-primary transition-colors">
                  Community
                </a>
              </li>
            </ul>
          </div>

          {/* Connect */}
          <div>
            <h3 className="font-semibold mb-4">Connect</h3>
            <div className="flex space-x-2">
              <motion.a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-lg glass-morphism hover:bg-white/10 transition-colors"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <GitBranch className="w-5 h-5" />
              </motion.a>
            </div>
            <div className="mt-4">
              <p className="text-sm text-muted-foreground">
                Open source and community driven
              </p>
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-8 pt-8 border-t border-border">
          <div className="flex flex-col sm:flex-row justify-between items-center">
            <p className="text-sm text-muted-foreground">
              © {currentYear} NeuraVault MCP. Built with{' '}
              <Heart className="inline w-4 h-4 text-red-500" /> for developers.
            </p>
            <div className="flex space-x-6 mt-4 sm:mt-0">
              <a href="#" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                Privacy Policy
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                Terms of Service
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
