import React, { StrictMode } from "react"; //React 
import { createRoot } from "react-dom/client";  //React's library that allows you to connect with web browsers (React DOM)
import "./styles.css"; // styles for components in app.js

import App from "./App"; //components you created in App.js

const root = createRoot(document.getElementById("root"));
root.render(
  <StrictMode>
    <App />
  </StrictMode>
);