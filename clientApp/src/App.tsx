import { useState, } from 'react'
import './App.css'
import HtmlContent from './components/HtmlContent'
import SearchStock from './components/SearchStock';
import Sources from './components/Sources';

interface StockInfoInterface {
  fullName: string,
  stId: string
}

interface ReportUrlInterface {
  link: string,
  source: string,
}

function App() {
  const [htmlContent, setHtmlContent] = useState({
        "cashflow_VI": "",
        "balance": "",
        "profit": "",
        "keyfinratio": ""
    });

  const [stockInfo, setStockInfo]= useState<StockInfoInterface>();
  const [loading, setLoading] = useState(false);
  const [reportUrl, setReportUrl] = useState<ReportUrlInterface>();


  return (
    <>
        <SearchStock setReportUrl={setReportUrl} setStockInfo={setStockInfo} setHtmlContent={setHtmlContent} setLoading={setLoading} />
        <h3>{stockInfo ? stockInfo.fullName : ""}</h3>
        <Sources reportUrl={reportUrl} />
        {loading ? <p>Loading...</p> : (<>
          <HtmlContent htmlContent={htmlContent.cashflow_VI} tableName='Cashflow statement' />
          <HtmlContent htmlContent={htmlContent.balance} tableName='Balance Sheet' />
          <HtmlContent htmlContent={htmlContent.profit} tableName='Profit and Loss' />
          <HtmlContent htmlContent={htmlContent.keyfinratio} tableName='Financial Ratios' />
        </>)}
    </>
  )
}

export default App
