import React from 'react';

interface Props {
  htmlContent: string;
  tableName: string;
}

const HtmlContent: React.FC<Props> = ({ htmlContent, tableName }) => (
  <>
    {htmlContent !== "" ? <h4 style={{textAlign: 'left'}}>{tableName}</h4> : null}
    <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
  </>
);

export default HtmlContent;