import { useState } from "react";

function App() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [downloadLink, setDownloadLink] = useState(null);

  const handleFileChange = (e, setFile) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file1 || !file2) {
      alert("両方のファイルを選択してください。");
      return;
    }

    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);

    const response = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (data.success) {
      setDownloadLink(`http://127.0.0.1:5000/download/aligned_output.txt`);
    }
  };

  return (
    <div>
      <h1>Translation Aligner</h1>
      <input type="file" onChange={(e) => handleFileChange(e, setFile1)} />
      <input type="file" onChange={(e) => handleFileChange(e, setFile2)} />
      <button onClick={handleUpload}>Upload and Align</button>
      {downloadLink && <a href={downloadLink} download>Download Result</a>}
    </div>
  );
}

export default App;
