import logo from "./logo.svg";
import "./App.css";

function App() {
  const shouldAuthenticate = true;
  useEffect(() => {
    if (shouldAuthenticate) {
      //check url
      const urlParams = new URLSearchParams(location?.search);
      const code = urlParams?.get("code");

      if (!localStorage.getItem("isLoggedIn")) {
        localStorage.setItem("isLoggedIn", "false");
        //redirect to url for login
        if (window) {
          window.location.href = `${process.env.REACT_APP_IDP_ENDPOINT}/authorize?response_type=code&identity_provider=${process.env.REACT_APP_IDENTITY_PROVIDER}&client_id=${process.env.REACT_APP_CLIENT_ID}&redirect_uri=${process.env.REACT_APP_DOMAIN}`;
        }
      } else if (localStorage.getItem("isLoggedIn") === "false" && code) {
        //after redirection and getting code of login
        const base64Cid = btoa(
          `${process.env.REACT_APP_CLIENT_ID}:${process.env.REACT_APP_CLIENT_SECRET}`
        );
        const tokenEndpoint =
          (process.env.REACT_APP_IDP_ENDPOINT ?? "") + "/oauth2/token";
        const clientId = process.env.REACT_APP_CLIENT_ID ?? "";
        const redirectUri = process.env.REACT_APP_DOMAIN ?? "";
        const authorizationHeader = "Basic " + base64Cid;

        const requestBody = new URLSearchParams({
          grant_type: "authorization_code",
          client_id: clientId,
          code: code,
          redirect_uri: redirectUri,
        });

        const requestOptions = {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            Authorization: authorizationHeader,
          },
          body: requestBody.toString(),
        };

        fetch(tokenEndpoint, requestOptions)
          .then((response) => response?.json())
          .then((data) => {
            localStorage.setItem("bearerToken", data?.id_token);
            localStorage.setItem("isLoggedIn", "true");

            const parsedToken = parseJwt(data?.id_token ?? "");
            const userDetails = {
              email: parsedToken?.email ?? "",
              userId: parsedToken?.identities?.find((i) => i)?.userId ?? "",
              name: parsedToken?.name ?? "",
              firstName: parsedToken?.given_name ?? "",
              lastName: parsedToken?.family_name ?? "",
            };

            localStorage.setItem("userDetails", JSON?.stringify(userDetails));

            CognitoIDP().then((res) => {
              if (res) {
                setLoginLoaded(true);
              }
            });
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      } else if (localStorage.getItem("isLoggedIn") === "false" && !code) {
        localStorage.removeItem("isLoggedIn");
        if (window) {
          window.location.reload();
        }
      }
    }
  }, []);
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
