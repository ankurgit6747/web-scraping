import { useState, } from 'react'
import './App.css'
import HtmlContent from './components/HtmlContent'
import SearchStock from './components/SearchStock';


interface StockInfoInterface {
  fullName: string,
  stId: string
}

function App() {
  const [htmlContent, setHtmlContent] = useState("");
  const [stockInfo, setStockInfo]= useState<StockInfoInterface>();

  return (
    <>
        <SearchStock setStockInfo={setStockInfo} setHtmlContent={setHtmlContent} />
          <h3>{stockInfo ? stockInfo.fullName : ""}</h3>
        <HtmlContent htmlContent={htmlContent} />
    </>
  )
}

export default App
