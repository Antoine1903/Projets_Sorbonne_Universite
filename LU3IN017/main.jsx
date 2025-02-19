import { StrictMode } from'react'
import { createRoot } from'react-dom/client'
import Card from './Card.jsx'
import CardList from './CardList.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
   <CardList/>
  </StrictMode>,
)