import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import DocsPage from './pages/DocsPage'
import { Navigation } from './components/Navigation'
import { Footer } from './components/Footer'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background text-foreground">
        <Navigation />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/docs" element={<DocsPage />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  )
}

export default App
