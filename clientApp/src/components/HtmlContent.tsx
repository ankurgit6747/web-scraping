import React from 'react';

interface Props {
  htmlContent: string;
}

const HtmlContent: React.FC<Props> = ({ htmlContent }) => (
  <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
);

export default HtmlContent;