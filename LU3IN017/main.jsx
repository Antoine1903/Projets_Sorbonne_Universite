import { StrictMode } from 'react'
import { useState } from "react";
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Test from "./Test.jsx"
import Card from "./Card.jsx"

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Card symbol="+" />
  </StrictMode>,
)