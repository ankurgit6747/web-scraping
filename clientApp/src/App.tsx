import { useState, } from 'react'
import './App.css'
import HtmlContent from './components/HtmlContent'
import SearchStock from './components/SearchStock';


interface StockInfoInterface {
  fullName: string,
  stId: string
}

function App() {
  const [htmlContent, setHtmlContent] = useState({
        "cashflow_VI": "",
        "balance": "",
        "profit": "",
        "keyfinratio": ""
    });

  const [stockInfo, setStockInfo]= useState<StockInfoInterface>();

  return (
    <>
        <SearchStock setStockInfo={setStockInfo} setHtmlContent={setHtmlContent} />
        <h3>{stockInfo ? stockInfo.fullName : ""}</h3>
        <HtmlContent htmlContent={htmlContent.cashflow_VI} tableName='Cashflow statement' />
        <HtmlContent htmlContent={htmlContent.balance} tableName='Balance Sheet' />
        <HtmlContent htmlContent={htmlContent.profit} tableName='Profit and Loss' />
        <HtmlContent htmlContent={htmlContent.keyfinratio} tableName='Financial Ratios' />
    </>
  )
}

export default App
