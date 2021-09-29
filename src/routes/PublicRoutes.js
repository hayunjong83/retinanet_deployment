import React from "react";
import { Redirect, Route, Switch } from "react-router-dom";
import SLUGS from "../resources/slug";
import Home from "../components/content/home";
import Classification from "../components/content/classification";
import ObjectDetection from "../components/content/objectDetection";

function PublicRoutes() {
  return (
    <Switch>
      <Route exact path={SLUGS.home} component={Home} />
      <Route exact path={SLUGS.classification} component={Classification} />
      <Route exact path={SLUGS.objectdetection} component={ObjectDetection} />
      <Redirect to={SLUGS.home} />
    </Switch>
  );
}

export default PublicRoutes;
