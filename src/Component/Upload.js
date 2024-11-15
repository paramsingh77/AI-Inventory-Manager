import React from 'react';

const Upload = ({ file, onFileChange, onUpload, error }) => {
  return (
    <>
      <div>Upload</div>
      <input type="file" onChange={onFileChange} />
      <button onClick={onUpload}>Upload</button>
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </>
  );
};

export default Upload;
