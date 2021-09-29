import React from "react";
import { createUseStyles, useTheme } from "react-jss";
import { useHistory } from "react-router-dom";
import SLUGS from "../../resources/slug";
import {
  IconObjectDetection,
  IconClassification,
  IconSettings,
  IconBurger,
} from "../../assets/";
import { convertSlugToUrl } from "../../resources/utilities";
import LogoComponent from "./LogoComponent";
import Menu from "./MenuComponent";
import MenuItem from "./MenuItemComponent";

const useStyles = createUseStyles({
  separator: {
    borderTop: ({ theme }) => `1px solid ${theme.color.lightGrayishBlue}`,
    marginTop: 16,
    marginBottom: 16,
    opacity: 0.06,
  },
});

function SidebarComponent() {
  const { push } = useHistory();
  const theme = useTheme();
  const classes = useStyles({ theme });
  const isMobile = window.innerWidth <= 1080;

  async function logout() {
    push(SLUGS.login);
  }

  function onClick(slug, parameters = {}) {
    push(convertSlugToUrl(slug, parameters));
  }

  return (
    <Menu isMobile={isMobile}>
      <div style={{ paddingTop: 30, paddingBottom: 30 }}>
        <LogoComponent />
      </div>

      <MenuItem
        id={SLUGS.home}
        title="Home"
        icon={IconSettings}
        onClick={() => onClick(SLUGS.Home)}
      />
      <MenuItem
        id={SLUGS.classification}
        title="Classification"
        icon={IconClassification}
        onClick={() => onClick(SLUGS.classification)}
      />
      <MenuItem
        id={SLUGS.objdectdetection}
        title="Object Detection"
        icon={IconObjectDetection}
        onClick={() => onClick(SLUGS.objdectdetection)}
      />
    </Menu>
  );
}

export default SidebarComponent;
