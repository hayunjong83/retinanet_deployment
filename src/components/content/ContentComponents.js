import React from "react";
import { Column, Row } from "simple-flexbox";
import { StyleSheet, css } from "aphrodite/no-important";
import MiniCardComponent from "./MiniCardComponents";

const styles = StyleSheet.create({
  cardsContainer: {
    marginRight: -30,
    marginTop: -30,
  },
  cardRow: {
    marginTop: 30,
    "@media (max-width: 768px)": {
      marginTop: 0,
    },
  },
  miniCardContainer: {
    flexGrow: 1,
    marginRight: 30,
    "@media (max-width: 768px)": {
      marginTop: 30,
      maxWidth: "none",
    },
  },
});

function ContentComponent() {
  return (
    <Column>
      <Row
        className={css(styles.cardsContainer)}
        wrap
        flexGrow={1}
        horizontal="space-between"
        breakpoints={{ 768: "column" }}
      >
        <Row
          className={css(styles.cardRow)}
          wrap
          flexGrow={1}
          horizontal="space-between"
          breakpoints={{ 384: "column" }}
        >
          <MiniCardComponent
            className={css(styles.miniCardContainer)}
            title="Unresolved"
            value="60"
          />
          <MiniCardComponent
            className={css(styles.miniCardContainer)}
            title="Overdue"
            value="16"
          />
        </Row>
        <Row
          className={css(styles.cardRow)}
          wrap
          flexGrow={1}
          horizontal="space-between"
          breakpoints={{ 384: "column" }}
        >
          <MiniCardComponent
            className={css(styles.miniCardContainer)}
            title="Open"
            value="43"
          />
          <MiniCardComponent
            className={css(styles.miniCardContainer)}
            title="On hold"
            value="64"
          />
        </Row>
      </Row>
    </Column>
  );
}

export default ContentComponent;
