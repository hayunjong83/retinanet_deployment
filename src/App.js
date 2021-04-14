import React from "react";
import "./App.css";
import DropZone from "./component/dropzone/DropZone";

function App() {
  return (
    <div>
      <p className="title">Object Detection using RetinaNet</p>
      <div className="content">
        <DropZone />
      </div>
    </div>
  );
}

export default App;
