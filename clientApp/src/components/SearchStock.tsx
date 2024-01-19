import { useState } from 'react';
import axios from 'axios';

const SearchStock = ({setStockInfo, setHtmlContent}: any) => {
    const [keyword, setKeyword] = useState("");

    function handleSearch() {
      axios.get(`http://localhost:8000/get_scId/${keyword}`)
        .then((res) => {
          setStockInfo(res.data)
          return axios.get(`http://localhost:8000/get_financials/${res.data.scId}`);
        })
        .then((res) => {
          // setHtmlContent(res.data.content)
          setHtmlContent({
            "cashflow_VI": res.data.cashflow_VI,
            "balance": res.data.balance,
            "profit": res.data.profit,
            "keyfinratio": res.data.keyfinratio
          })
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