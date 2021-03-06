import React, { useEffect } from "react";
import { useLocation } from "react-router-dom";
import useWindowSize from "../hooks/useWindowSize";
// import PrivateSection from 'routes/PrivateSection'
import PublicRoutes from "./PublicRoutes";

function Routes() {
  const { pathname } = useLocation();

  const [width, height] = useWindowSize();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  //   const isUserLoggedIn= true
  //   return isUserLoggedIn ? <PrivateSection /> : <PublicRoutes />
  return <PublicRoutes />;
}

export default Routes;
