import React from "react";
import { Column } from "simple-flexbox";
import { StyleSheet, css } from "aphrodite";
import LogoComponent from "./LogoComponent";
import MenuItemComponent from "./MenuItemComponent";
import IconObjectDetection from "../../assets/icon-objectDetection";
import IconClassification from "../../assets/icon-classification";
import IconSettings from "../../assets/icon-settings";

const styles = StyleSheet.create({
  container: {
    backgroundColor: "#363740",
    width: 255,
    paddingTop: 32,
  },
  menuItemList: {
    marginTop: 52,
  },
  separator: {
    borderTop: "1px solid #DFE0EB",
    marginTop: 16,
    marginBottom: 16,
    opacity: 0.06,
  },
});

function SidebarComponent(props) {
  return (
    <Column className={css(styles.container)}>
      <LogoComponent />
      <Column className={css(styles.menuItemList)}>
        <MenuItemComponent
          title="Object Detection"
          icon={IconObjectDetection}
          onClick={() => props.onChange("Object Detection")}
          active={props.selectedItem === "Object Detection"}
        />
        <MenuItemComponent
          title="Classification"
          icon={IconClassification}
          onClick={() => props.onChange("Classification")}
          active={props.selectedItem === "Classification"}
        />
        <div className={css(styles.separator)}></div>
        <MenuItemComponent
          title="Settings"
          icon={IconSettings}
          onClick={() => props.onChange("Settings")}
          active={props.selectedItem === "Settings"}
        />
      </Column>
    </Column>
  );
}

export default SidebarComponent;
