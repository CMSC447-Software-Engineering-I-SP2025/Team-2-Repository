import React from 'react';

const Footer = () => {
    return (
        <footer style={footerStyle}>
            <p>&copy; {new Date().getFullYear()} Digital Recipe App. All rights reserved.</p>
        </footer>
    );
};

const footerStyle = {
    textAlign: 'center',
    backgroundColor: '#f8f9fa',
    borderTop: '1px solid #e7e7e7',
    width: '100%',
    // position: 'relative',
    overflowX: 'hidden',
    height: '55px',
    // marginTop: '290px',
    zIndex: 1,
    clear: 'both',
    justifySelf: 'end',
  };
  

export default Footer;
