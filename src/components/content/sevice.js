import React from "react";
import objectDetection from "./objectDetection";
import Classfication from "./classification";

function Service(props) {
  const { icon, title, ...otherProps } = props;
  // let item = "";
  // switch (title) {
  //   case "Object Detection":
  //     return (item = "object_detection");
  //   case "Classification":
  //     return (item = "classification");
  //   case "Settings":
  //     return (item = "seetings");
  //   default:
  //     break;
  // }
  return (
    <div>
      <Classfication />
    </div>
  );
}

export default Service;
