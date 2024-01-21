const Sources = ({reportUrl}: any) => {
  return (
    <div style={{textAlign: 'left'}}>
      {reportUrl ? <> 
        <h4>Source: {reportUrl.source}</h4>
        <p>Report Url: <a href={reportUrl && reportUrl?.link} target="_blank" rel="noopener noreferrer">{reportUrl && reportUrl?.link}</a></p>
      </> : null}
    </div>
  )
}

export default Sources;
