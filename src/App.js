import React from "react";
import { Column, Row } from "simple-flexbox";
import { StyleSheet, css } from "aphrodite";
import SidebarComponent from "./components/sidebar/SidebarComponent";
import HeaderComponent from "./components/header/HeaderComponent";
import Service from "./components/content/sevice";
import { BrowserRouter } from "react-router-dom";
import ObjectDetection from "./components/content/objectDetection";
import Classification from "./components/content/classification";
import Routes from "./routes/index";
import "./App.css";

const styles = StyleSheet.create({
  container: {
    height: "100vh",
  },
  content: {
    marginTop: 54,
  },
  mainBlock: {
    backgroundColor: "#F7F8FC",
    padding: 30,
  },
});

class App extends React.Component {
  state = { selectedItem: "Object Detection" };

  componentDidMount() {
    window.addEventListener("resize", this.resize);
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.resize);
  }

  resize = () => this.forceUpdate();

  render() {
    const { selectedItem } = this.state;
    console.log(selectedItem);
    return (
      <Row className={css(styles.container)}>
        <SidebarComponent
          selectedItem={selectedItem}
          onChange={(selectedItem) => this.setState({ selectedItem })}
        />

        <Column flexGrow={1} className={css(styles.mainBlock)}>
          <HeaderComponent title={selectedItem} />
          <div className={css(styles.content)}>
            <BrowserRouter>
              <Routes />
            </BrowserRouter>
          </div>
        </Column>
      </Row>
    );
  }
}

export default App;
