import { useState } from "react";
import "./App.css";

import { LoginScreen, HomeScreen } from "./screens";
function App() {
  // User token is defined
  const [userToken, setUserToken] = useState();

  return (
    <>
    {/* If user token exists, go into home page, otherwise go into login page */}
      {userToken ? (
        <HomeScreen userToken={userToken} setUserToken={setUserToken} />
      ) : (
        <LoginScreen setUserToken={setUserToken} />
      )}
    </>
  );
}

export default App;
