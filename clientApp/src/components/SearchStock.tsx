import { useState } from 'react';
import axios from 'axios';

const SearchStock = ({setReportUrl, setStockInfo, setHtmlContent, setLoading}: any) => {
    const [keyword, setKeyword] = useState("");

    function handleSearch() {
      setLoading(true);
      let companyName = '';

      axios.get(`http://localhost:8000/get_scId/${keyword}`)
        .then((res) => {
          setStockInfo(res.data)
          companyName = res.data.fullName;
          return axios.get(`http://localhost:8000/get_financials/${res.data.scId}`);
        })
        .then((res) => {
          setHtmlContent({
            "cashflow_VI": res.data.cashflow_VI,
            "balance": res.data.balance,
            "profit": res.data.profit,
            "keyfinratio": res.data.keyfinratio
          })
          return axios.get(`http://localhost:8000/get_report_urls?company_name=${encodeURIComponent(companyName)}`)  // Pass the company name to the API
        })
        .then((res) => {
          setReportUrl(res.data.report_urls)
          setLoading(false);
        })
    }

    function handleKeyPress(event: React.KeyboardEvent) {
      if (event.key === 'Enter') {
        handleSearch();
      }
    }


  return (
    <div>
      <h2>Search Stock</h2>
      <input type="text" placeholder='keyword' value={keyword} onChange={(e) => setKeyword(e.target.value)} onKeyDown={handleKeyPress} />
      <button onClick={handleSearch}>Search</button>
    </div>
  )
}

export default SearchStock