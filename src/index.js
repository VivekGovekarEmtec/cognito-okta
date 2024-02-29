import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
Amplify.configure({
  Auth: {
    userPoolId: process.env.REACT_APP_USER_POOL_ID ?? "", // Add this line - Amazon Cognito User Pool ID
    userPoolWebClientId: process.env.REACT_APP_CLIENT_ID ?? "", // Add this line - App client ID for the User Pool
    identityPoolId: process.env.REACT_APP_COGNITO_IDENTITY_POOL_ID ?? "", // REQUIRED - Amazon Cognito Identity Pool ID
    region: process.env.REACT_APP_AWS_Region ?? "",
  },
});
const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
