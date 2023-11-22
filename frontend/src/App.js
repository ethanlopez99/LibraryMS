import { useState } from "react";
import "./App.css";

import { LoginScreen, HomeScreen } from "./screens";
function App() {
  const [userToken, setUserToken] = useState();

  return (
    <>
      {userToken ? (
        <HomeScreen userToken={userToken} setUserToken={setUserToken} />
      ) : (
        <LoginScreen setUserToken={setUserToken} />
      )}
    </>
  );
}

export default App;
